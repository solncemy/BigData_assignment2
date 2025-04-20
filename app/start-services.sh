#!/bin/bash
# This will run only by the master node

export SPARK_HOME=/opt/bitnami/spark
export HADOOP_HOME=/opt/bitnami/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SPARK_HOME/bin:$SPARK_HOME/sbin

mkdir -p $HADOOP_HOME/etc/hadoop
cat > $HADOOP_HOME/etc/hadoop/core-site.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://cluster-master:9000</value>
    </property>
</configuration>
EOF

cat > $HADOOP_HOME/etc/hadoop/hdfs-site.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///opt/bitnami/hadoop/data/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///opt/bitnami/hadoop/data/datanode</value>
    </property>
</configuration>
EOF

hdfs namenode -format

$HADOOP_HOME/sbin/start-dfs.sh

$HADOOP_HOME/sbin/start-yarn.sh



mapred --daemon start historyserver

jps -lm

hdfs dfsadmin -report

hdfs dfsadmin -safemode leave

hdfs dfs -mkdir -p /apps/spark/jars
hdfs dfs -chmod 744 /apps/spark/jars

hdfs dfs -put /usr/local/spark/jars/* /apps/spark/jars/
hdfs dfs -chmod +rx /apps/spark/jars/

scala -version

jps -lm

hdfs dfs -mkdir -p /user/root

