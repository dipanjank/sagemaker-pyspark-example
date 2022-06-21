import argparse
import logging
import os

import boto3
import sagemaker
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.spark.processing import PySparkProcessor
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep

LOCAL_INPUT_PATH = "/opt/ml/processing/input"
LOCAL_OUTPUT_PATH = "/opt/ml/processing/input/iris-summary"


def build_pipeline(args: argparse.Namespace, sagemaker_session: sagemaker.session.Session):
    input_ = ProcessingInput(
        source=args.s3_input_prefix,
        destination=LOCAL_INPUT_PATH,
        input_name="iris-in",
        s3_data_type="S3Prefix",
        s3_input_mode="File",
    )

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

    output_ = ProcessingOutput(
        source=LOCAL_OUTPUT_PATH,
        destination=args.s3_output_prefix,
        output_name="iris-grouped",
        s3_upload_mode="EndOfJob",
        app_managed=False,
    )

    run_args = spark_processor.get_run_args(
        submit_app="./pyspark_sagemaker_example/transform_iris.py",
        inputs=[input_],
        outputs=[output_],
        arguments=[
            "--input-path",
            os.path.join(LOCAL_INPUT_PATH, "iris.csv"),
            "--output-path",
            LOCAL_OUTPUT_PATH,
        ],
        spark_event_logs_s3_uri=s3_event_log_uri,
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
        "--s3-input-prefix",
        type=str,
        required=True,
        help="Path to the IRIS CSV file on S3"
    )
    parser.add_argument(
        "--spark-event-log-bucket",
        type=str,
        required=True,
        help="The Spark Event Log Bucket"
    )
    parser.add_argument(
        "--spark-event-log-prefix",
        type=str,
        required=True,
        help="The Spark Event Log Prefix"
    )
    parser.add_argument(
        "--sagemaker-role",
        type=str,
        required=True,
        help="SageMaker Execution Role"
    )
    parser.add_argument(
        "--sagemaker-role",
        type=str,
        required=True,
        help="SageMaker Execution Role"
    )
    parser.add_argument(
        "--s3-output-prefix",
        type=str,
        required=True,
        help="S3 Prefix for Parquet file output"
    )
    parser.add_argument(
        "--default-bucket",
        type=str,
        default="default-sagemaker-bucket",
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
    sagemaker_session = sagemaker.session.Session(
        boto_session=boto3.Session(region_name=args.region_name),
        default_bucket=args.default_bucket,
    )
    pipeline = build_pipeline(args, sagemaker_session)
    logging.info("starting pipeline...")
    exec_ = pipeline.start()
    logging.info("Waiting for pipeline to finish...")
    exec_.wait(max_attempts=1)
    logging.info("Pipeline execution finished.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    main()
