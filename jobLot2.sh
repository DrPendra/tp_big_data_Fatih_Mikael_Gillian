cp /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar .
./start-hadoop.sh
start-hbase.sh
hbase-daemon.sh start thrift
hdfs dfs -mkdir -p input
hdfs dfs -put dataw_fro03_sans_accent_normalement.csv input
hdfs dfs -rm -r resultat21
hdfs dfs -rm -r resultat21
hadoop jar hadoop-streaming-2.7.2.jar -file mapper_1_1.py -mapper "python3 mapper_1_1.py" -file reducer_1_1.py -reducer "python3 reducer_1_1.py" -input input/dataw_fro03_sans_accent_normalement.csv -output resultat21
hadoop jar hadoop-streaming-2.7.2.jar -file mapper_1_2.py -mapper "python3 mapper_1_2.py" -file reducer_1_2.py -reducer "python3 reducer_1_2.py" -input input/dataw_fro03_sans_accent_normalement.csv -output resultat21