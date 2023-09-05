#!/usr/bin/env python
"""mapper.py"""

import sys
import re

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

def nullOrEmpty(e, default):
    if e == 'NULL' or e == '':
        return default
    else:
        return e

next(sys.stdin)
counter = 0
# input comes from STDIN (standard input)
for line in sys.stdin:

    line= line.replace('""', '')
    tupleList = re.findall(r'(?:"([\w\-\+\&\.:\ ,\'\/]+)")|(?:,([\w\ ]*)(?=,))', line)
    words = contructList(tupleList)
    if not checkMandatoryColumn(words):
        continue
    cond = True
    dp = int(float(nullOrEmpty(words[4],0))/1000)
    timbrecli = int(float(nullOrEmpty(words[8],0)))
    date = nullOrEmpty(words[7],"0000-00-00 00:00:00")
    annee = int(date[0:4])
    if words[9] == 'NULL' or words[9] == '':
        cond = False
    if words[10] == 'NULL' or words[10] == '':
        cond = False
    if annee < 2006 or annee > 2016:
        cond = False
    if cond:
        finalStr = words[6]+";"+words[5] + ";" +words[9]+ ";" +words[10] + ";" +str(dp) + ";" +words[8] 
        print('%s;%i' % (finalStr, 1))

'''
hadoop jar hadoop-streaming-2.7.2.jar -file mapper.py -mapper "python3 mapper.py" -file reducer.py -reducer "python3 reducer.py" -input input/word.txt -output output01
'''