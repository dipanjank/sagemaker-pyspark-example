import os.path

import pytest
from pyspark.sql.session import SparkSession

from pyspark_sagemaker_example.transform_iris import transform_file


@pytest.fixture(scope="module")
def spark():
    spark = SparkSession.builder.appName("pyspark-tests").getOrCreate()
    yield spark
    spark.stop()


def test_iris_transform(spark, tmpdir):
    output_path = str(tmpdir / "iris-grouped")
    this_dir = os.path.abspath(os.path.dirname(__file__))
    input_file = os.path.join(this_dir, "iris.csv")
    transform_file(spark, input_file, output_path)
    assert os.path.isdir(output_path)
