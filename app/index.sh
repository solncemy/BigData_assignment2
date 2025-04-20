#!/bin/bash
echo "This script include commands to run mapreduce jobs using hadoop streaming to index documents"

INPUT_PATH=${1:-/index/data}
echo "Input path is: $INPUT_PATH"

python3 -c "
from cassandra.cluster import Cluster
cluster = Cluster(['cassandra-server'])
session = cluster.connect()
session.execute('CREATE KEYSPACE IF NOT EXISTS search_engine WITH replication = {\'class\': \'SimpleStrategy\', \'replication_factor\': 1}')
session.execute('USE search_engine')
session.execute('CREATE TABLE IF NOT EXISTS vocabulary (term text PRIMARY KEY, doc_freq int, docs text)')
session.execute('CREATE TABLE IF NOT EXISTS documents (doc_id text PRIMARY KEY, title text, avg_length float)')
"

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -input $INPUT_PATH \
    -output /tmp/index/output \
    -mapper "python3 /app/mapreduce/mapper1.py" \
    -reducer "python3 /app/mapreduce/reducer1.py" \
    -file /app/mapreduce/mapper1.py \
    -file /app/mapreduce/reducer1.py

hadoop fs -cat /tmp/index/output/part-* | python3 -c "
import sys
from cassandra.cluster import Cluster
cluster = Cluster(['cassandra-server'])
session = cluster.connect('search_engine')

for line in sys.stdin:
    term, doc_freq, docs = line.strip().split('\t')
    session.execute('INSERT INTO vocabulary (term, doc_freq, docs) VALUES (%s, %s, %s)', 
                   (term, int(doc_freq), docs))
"

hadoop fs -cat $INPUT_PATH/* | python3 -c "
import sys
from cassandra.cluster import Cluster
cluster = Cluster(['cassandra-server'])
session = cluster.connect('search_engine')

for line in sys.stdin:
    doc_id, title, text = line.strip().split('\t')
    words = text.split()
    avg_length = len(words)
    session.execute('INSERT INTO documents (doc_id, title, avg_length) VALUES (%s, %s, %s)',
                   (doc_id, title, float(avg_length)))
"

echo "Indexing completed successfully!"
