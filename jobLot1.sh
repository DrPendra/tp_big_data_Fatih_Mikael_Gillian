cp /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar .
./start-hadoop.sh
start-hbase.sh
hbase-daemon.sh start thrift
hdfs dfs -mkdir -p input
hdfs dfs -put dataw_fro03_sans_accent_normalement.csv input
hdfs dfs -rm -r resultat11
hdfs dfs -rm -r resultat12
hdfs dfs -rm -r resultat13
hadoop jar hadoop-streaming-2.7.2.jar -file mapper_1_1.py -mapper "python3 mapper_1_1.py" -file reducer_1_1.py -reducer "python3 reducer_1_1.py" -input input/dataw_fro03_sans_accent_normalement.csv -output resultat11
hadoop jar hadoop-streaming-2.7.2.jar -file mapper_1_2.py -mapper "python3 mapper_1_2.py" -file reducer_1_2.py -reducer "python3 reducer_1_2.py" -input input/dataw_fro03_sans_accent_normalement.csv -output resultat12
hadoop jar hadoop-streaming-2.7.2.jar -file mapper_1_3.py -mapper "python3 mapper_1_3.py" -file reducer_1_3.py -reducer "python3 reducer_1_3.py" -input input/dataw_fro03_sans_accent_normalement.csv -output resultat13