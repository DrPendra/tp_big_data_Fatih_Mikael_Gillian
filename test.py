import happybase

table = None
connection = happybase.Connection('127.0.0.1', 9090)
connection.open()
tableName = b"Statistiques_1_1"
print(connection.tables())
if tableName in set(connection.tables()):
  print("yoloy")
  connection.disable_table(tableName)
  connection.delete_table(tableName, disable=True)

'''connection.create_table(tableName, {'cf_data': dict()})

table = connection.table(tableName)
table.put(b'%i' % 1, {b'cf_data:name': '%s' % 'Goere'})'''

