stop-hbase.sh
./start-hadoop.sh
start-hbase.sh
hbase-daemon.sh stop thrift
hbase-daemon.sh start rest -p 9090
# le user pour l'ODBC est root

