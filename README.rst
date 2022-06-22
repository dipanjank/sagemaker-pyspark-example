=========================
pyspark-sagemaker-example
=========================


.. image:: https://img.shields.io/pypi/v/pyspark_sagemaker_example.svg
        :target: https://pypi.python.org/pypi/pyspark_sagemaker_example

.. image:: https://img.shields.io/travis/dipanjank/pyspark_sagemaker_example.svg
        :target: https://travis-ci.com/dipanjank/pyspark_sagemaker_example

.. image:: https://readthedocs.org/projects/pyspark-sagemaker-example/badge/?version=latest
        :target: https://pyspark-sagemaker-example.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



How to Run Spark History Server
===============================

    $ cd spark-history-server
    $ docker build -t sparkui .
    $ SPARK_EVENTLOG_DIR="s3a://dk-spark-event-logs/spark-logs/spark_event_logs"
    $ docker run -itd -e SPARK_HISTORY_OPTS="$SPARK_HISTORY_OPTS \
        -Dspark.history.fs.logDirectory=$SPARK_EVENTLOG_DIR \
        -Dspark.hadoop.fs.s3a.access.key=$AWS_ACCESS_KEY_ID \
        -Dspark.hadoop.fs.s3a.secret.key=$AWS_SECRET_ACCESS_KEY" \
        -p 18080:18080 sparkui \
        "/opt/spark/bin/spark-class org.apache.spark.deploy.history.HistoryServer"


Running PysparkProcessor in SageMaker Pipelines example


* Free software: MIT license
* Documentation: https://pyspark-sagemaker-example.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
