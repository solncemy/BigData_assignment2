#!/bin/bash
echo "This script will include commands to search for documents given the query using Spark RDD"

spark-submit --master yarn query_router.py $1