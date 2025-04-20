#!/bin/bash
echo "This script will include commands to search for documents given the query using Spark RDD"

if [ -z "$1" ]; then
    echo "Usage: search.sh <query>"
    exit 1
fi

source .venv/bin/activate

export PYSPARK_DRIVER_PYTHON=$(which python) 

export PYSPARK_PYTHON=./.venv/bin/python

export SPARK_HOME=/usr/local/spark
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip:$PYTHONPATH

spark-submit \
    --master yarn \
    --deploy-mode client \
    --archives /app/.venv.tar.gz#.venv \
    --conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=./.venv/bin/python \
    --conf spark.executorEnv.PYSPARK_PYTHON=./.venv/bin/python \
    query.py "$1"