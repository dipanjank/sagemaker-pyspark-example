# pyspark-sagemaker-example

This project contains an example of Deployment of a [SageMaker Pipeline](https://aws.amazon.com/sagemaker/pipelines/)
using GitHub Actions.

The Pipeline is defined in [sagemaker_pipeline.py](./sagemaker_pipeline.py). It contains a single
[ProcessingStep](https://docs.aws.amazon.com/sagemaker/latest/dg/build-and-manage-steps.html#step-type-processing) that
defines a [PySparkProcessor](https://sagemaker.readthedocs.io/en/stable/amazon_sagemaker_processing.html#pysparkprocessor).

The PysparkProcessor

* Reads the IRIS dataset from S3 into a Spark DataFrame
* Groups the data by the "variety" column
* Calculates aggregate stats by feature
* Writes the aggregate data as Parquet to S3

When run, the PysparkProcessor forwards event logs to S3. Included also is a Docker Image for SparkHistoryServer and
instructions on how run this.

## How to Run Spark History Server

```bash

$ cd spark-history-server
$ docker build -t sparkui .
$ SPARK_EVENTLOG_DIR="s3a://dk-spark-event-logs/spark-logs/spark_event_logs"
$ docker run -itd -e SPARK_HISTORY_OPTS="$SPARK_HISTORY_OPTS \
    -Dspark.history.fs.logDirectory=$SPARK_EVENTLOG_DIR \
    -Dspark.hadoop.fs.s3a.access.key=$AWS_ACCESS_KEY_ID \
    -Dspark.hadoop.fs.s3a.secret.key=$AWS_SECRET_ACCESS_KEY" \
    -p 18080:18080 sparkui \
    "/opt/spark/bin/spark-class org.apache.spark.deploy.history.HistoryServer"
```

* Free software: MIT license
* Documentation: https://pyspark-sagemaker-example.readthedocs.io.

# Features


# Credits

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
