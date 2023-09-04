import sys
import happybase
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from functools import cmp_to_key

current_word = None
current_count = 0
word = None
index = 0
table = None
connection = happybase.Connection('127.0.0.1', 9090)
connection.open()
tableName = b"Statistiques_1_2"
if tableName in set(connection.tables()):
  connection.delete_table(tableName, disable=True)

connection.create_table(tableName, {'cf_info': dict()})

table = connection.table(tableName)

fileName = "st_1_2.txt"
file = open(fileName, "w")

clientList = []

for line in sys.stdin:

    line = line.strip()
    nomCli,prenomCli,dep,city,nbColis = line.split(';')
    word =  nomCli+";"+prenomCli+";"+dep+";"+city
    try:
        nbColis = int(nbColis)
    except ValueError:
        continue

    if current_word == word:
        current_count += 1
    else:
        if current_word:
            cur_nomCli,cur_prenomCli,cur_dep,cur_city = word.split(';')
            # write result to STDOUT
            print('%s\t%s' % (current_word, current_count))
            #table.put(b'%i' % index, {b'cf_info:nomCli': '%s' % cur_nomCli,b'cf_info:prenomCli': '%s' % cur_prenomCli,b'cf_info:dep': '%s' % cur_dep, b'cf_info:city': '%i' % cur_city, b'cf_info:city': '%i' % cur_city})
            #file.write(current_word + ";"+str(current_count)+"\n")
            clientList.append({'info':current_word,'qte':current_count})
        current_count = 1
        current_word = word
        index += 1



# do not forget to output the last word if needed!
if current_word == word:
    nomCli,prenomCli,dep,city = word.split(';')
    print('%s\t%s' % (current_word, current_count))
    #table.put(b'%i' % index, {b'cf_info:city': '%s' % cur_city,b'cf_info:obj': '%s' % cur_obj,b'cf_info:annee': '%s' % cur_annee, b'cf_info:count': '%i' % current_count})
    #file.write(current_word + ";"+str(current_count)+"\n")
    clientList.append({'info':current_word,'qte':current_count})
connection.close()

    
def comparator(a, b):
        #print(a)
        if int(a["qte"]) > int(b["qte"]):
            return -1
        if int(a["qte"]) < int(b["qte"]):
            return 1
        if a["info"] > b["info"]:
            return -1
        if a["info"] < b["info"]:
            return 1
        return 0


data = sorted(clientList, key=cmp_to_key(comparator))

[print(e) for e in data[0:10]]


'''data =[12,25,85]
df = pd.DataFrame(data)
# Créer une nouvelle figure
plt.figure()

# Créer le graphe pie
plt.pie(data, labels=data, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Répartition des commandes par département")

# Enregistrer le graphe au format PDF

output_pdf_file = '/datavolume1/resultat.pdf'
with PdfPages(output_pdf_file) as pdf:
    pdf.savefig()  # Sauvegarder le graphe dans le fichier PDF'''
