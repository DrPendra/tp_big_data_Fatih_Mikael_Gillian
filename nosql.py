#!/usr/bin/env python
"""mapper.py"""
import happybase
import sys
import re


table = None
connection = happybase.Connection('127.0.0.1', 9090)
connection.open()
tableName = b"LOT3"
if tableName in set(connection.tables()):
  connection.delete_table(tableName, disable=True)

connection.create_table(tableName, {'cf_client': dict(),'cf_location': dict(),'cf_cmd': dict()})

table = connection.table(tableName)

def contructList(tupleList):
    words = []
    for e in tupleList:
        if e[0] != '':
            words.append(e[0])
        else:
            words.append(e[1])
    return words

def checkMandatoryColumn(words):
    columnList = [0,2,3,4,6,7,14,17]
    for i in columnList:
        if words[i] == 'NULL' or words[i] == '':
            return False
    
    return True

def prepareQuery(listeData, listeCol):
    query = {}
    for i in range(len(listeCol)):
        if listeData[i] != 'NULL' and listeData[i] != '':
            query[listeCol[i]] = '%s' % listeData[i]
    return query

next(sys.stdin)
counter = 0
# input comes from STDIN (standard input)
for line in sys.stdin:

    line= line.replace('""', '\'')
    tupleList = re.findall(r'(?:"([\w\-\+\&\.:\ ,\'\/]+)")|(?:,([\w\ ]*)(?=,))', line)
    
    words = contructList(tupleList)
    if not checkMandatoryColumn(words):
        continue

    #table.put(b'%i' % counter, {b'cf_client:codeCli': '%s' % words,b'cf_info:prenomCli': '%s' % cur_prenomCli,b'cf_info:dep': '%s' % cur_dep, b'cf_info:city': '%i' % cur_city, b'cf_info:city': '%i' % cur_city})
    listeCol = ['cf_client:codeCli','cf_client:genreCli','cf_client:nomCli','cf_client:prenomCli','cf_location:cpCli','cf_location:villeCli','cf_cmd:codeCmd','cf_cmd:dateCmd','cf_cmd:timbreCli','cf_cmd:timbreCode','cf_cmd:nbColis','cf_cmd:chequeCli','cf_cmd:barchive','cf_cmd:bstock','cf_cmd:codeObj','cf_cmd:qte','cf_cmd:colis','cf_cmd:libObj','cf_cmd:tailleObj','cf_cmd:poidsObj','cf_cmd:points','cf_cmd:indispObj','cf_cmd:libCondi','cf_cmd:prixCond','cf_cmd:puObj']
    query = prepareQuery(words,listeCol)
    table.put(b'%i' % counter, query)
    counter+=1
'''
hadoop jar hadoop-streaming-2.7.2.jar -file mapper.py -mapper "python3 mapper.py" -file reducer.py -reducer "python3 reducer.py" -input input/word.txt -output output01
'''