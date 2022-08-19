import argparse
import logging
import os

import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    DoubleType,
    StringType,
    StructField,
    StructType,
)
from sagemaker.workflow.execution_variables import ExecutionVariables


def main():
    parser = argparse.ArgumentParser(description="app inputs and outputs")
    parser.add_argument("--input-path", type=str, help="local input path")
    parser.add_argument("--output-path", type=str, help="Local output path")
    args = parser.parse_args()
    spark = SparkSession.builder.appName("TransformIris").getOrCreate()
    transform_file(spark, args.input_path, args.output_path)


def transform_file(spark: SparkSession, input_path: str, output_path: str):
    schema = get_schema()
    # Read data from local file
    iris_df = spark.read.csv(input_path, header=True, schema=schema)
    fn_list = [F.min, F.max, F.mean]
    cols = [
        "sepal_length",
        "petal_length",
        "sepal_width",
        "petal_width",
    ]
    expr = [
        fn(c).alias(str(fn.__name__) + '_' + str(c)) for fn in fn_list for c in cols
    ]
    iris_grouped = iris_df.groupby('variety').agg(*expr)
    iris_grouped.write.parquet(output_path, mode="overwrite")


def get_schema():
    # Define the schema
    schema = StructType(
        [
            StructField("sepal_length", DoubleType(), True),
            StructField("sepal_width", DoubleType(), True),
            StructField("petal_length", DoubleType(), True),
            StructField("petal_width", DoubleType(), True),
            StructField("variety", StringType(), True),
        ]
    )
    return schema


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # logging.info(f"Execution ID: {ExecutionVariables.PIPELINE_EXECUTION_ID.to_string()}")
    for name. value in os.environ.items():
        logging.info("NAME: {name}, VALUE: {value}")
    main()
