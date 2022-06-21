FROM python:3.7-slim
FROM openjdk:11-slim

COPY --from=0 / /

RUN apt-get update -y && apt-get upgrade -y

COPY . /usr/local/pyspark-sagemaker
WORKDIR /usr/local/pyspark-sagemaker

RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

CMD pytest -vs tests/
