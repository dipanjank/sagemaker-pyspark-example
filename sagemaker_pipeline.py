import argparse
import json
import logging
from pprint import pformat

import boto3
from botocore.exceptions import WaiterError
from sagemaker import Session
from sagemaker.spark.processing import PySparkProcessor
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep

def build_pipeline(args: argparse.Namespace, sagemaker_session: Session):

    s3_event_log_uri = "s3://{}/{}/spark_event_logs".format(
        args.spark_event_log_bucket,
        args.spark_event_log_prefix
    )
    spark_processor = PySparkProcessor(
        base_job_name="transform-iris",
        framework_version="3.1",
        role=args.sagemaker_role,
        instance_count=2,
        instance_type="ml.m5.large",
        max_runtime_in_seconds=1200,
    )

    run_args = spark_processor.get_run_args(
        submit_app="./pyspark_sagemaker_example/transform_iris.py",
        arguments=[
            "--input-path",
            args.s3_input_path,
            "--output-path",
            args.s3_output_path,
        ],
    )

    step_process = ProcessingStep(
        name="ProcessIris",
        processor=spark_processor,
        inputs=run_args.inputs,
        outputs=run_args.outputs,
        job_arguments=run_args.arguments,
        code=run_args.code
    )

    return Pipeline(
        name="Pyspark-Example",
        steps=[step_process],
        sagemaker_session=sagemaker_session,
    )


def get_parser():
    parser = argparse.ArgumentParser(
        description="Build and run SageMaker Pipeline.")
    parser.add_argument(
        "--s3-input-path",
        type=str,
        default="s3a://dk-sagemaker-example-in/iris.csv",
        required=False,
        help="Path to the IRIS CSV file on S3"
    )
    parser.add_argument(
        "--spark-event-log-bucket",
        type=str,
        default="dk-spark-event-logs",
        required=False,
        help="The Spark Event Log Bucket"
    )
    parser.add_argument(
        "--spark-event-log-prefix",
        default="spark-logs",
        type=str,
        required=False,
        help="The Spark Event Log Prefix"
    )
    parser.add_argument(
        "--sagemaker-role",
        type=str,
        default="arn:aws:iam::381665779871:role/service-role/AmazonSageMaker-ExecutionRole-20220310T143208",
        required=False,
        help="SageMaker Execution Role"
    )
    parser.add_argument(
        "--s3-output-path",
        type=str,
        default="s3a://dk-sagemaker-example-out/iris-grouped",
        required=False,
        help="S3 Prefix for Parquet file output"
    )
    parser.add_argument(
        "--default-bucket",
        type=str,
        default="dk-default-sagemaker-bucket",
        required=False,
        help="Default SageMaker Bucket"
    )
    parser.add_argument(
        "--region-name",
        type=str,
        required=False,
        default="eu-west-1",
        help="AWS Region"
    )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    sagemaker_session = Session(
        boto_session=boto3.Session(region_name=args.region_name),
        default_bucket=args.default_bucket,
    )
    pipeline = build_pipeline(args, sagemaker_session)
    defn = pipeline.definition()
    defn = json.loads(defn)
    logging.info(f"Pipeline definition: {pformat(defn)}")
    logging.info("starting pipeline...")
    upsert_resp = pipeline.upsert(
        args.sagemaker_role,
        description="A SageMaker Pipeline to run Spark Processing Job",
    )
    logging.info(f"Upsert response: {pformat(upsert_resp)}")

    start_resp = pipeline.start()

    logging.info("Waiting for pipeline to finish...")
    try:
        start_resp.wait()
    except WaiterError:
        steps = start_resp.list_steps()
        logging.error("Pipeline execution failed.")
        logging.error(f"Steps: {pformat(steps)}")
        raise
    logging.info("Pipeline execution finished.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    main()
