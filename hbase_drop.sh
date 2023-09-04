./start-hadoop.sh
start-hbase.sh
hbase-daemon.sh start thrift

cat <<CMDES | hbase shell
disable 'maTable'
drop 'maTable' 
exit
CMDES

