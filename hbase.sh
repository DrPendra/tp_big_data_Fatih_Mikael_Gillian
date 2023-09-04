./start-hadoop.sh
start-hbase.sh
hbase-daemon.sh start thrift

cat <<CMDES | hbase shell
create 'maTable','cf'
list
describe 'maTable'
put 'maTable','1','cf:a','Test'
exit
CMDES

