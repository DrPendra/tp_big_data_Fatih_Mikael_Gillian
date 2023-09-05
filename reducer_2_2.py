import sys
import happybase
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import pandas as pd
from random import random

current_commande=None
max_compte=0
index=0
word = None
table = None
connection = happybase.Connection('127.0.0.1', 9090)
connection.open()
tableName = b"Statistiques_2_2"
if tableName in set(connection.tables()):
    connection.delete_table(tableName, disable=True)

connection.create_table(tableName, {'cf_info': dict()})

table = connection.table(tableName)

fileName = "st_2_2.txt"
file = open(fileName, "w")
liste_tempo = []
# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper.py
    codcde, ville , timbrecde, nbcolis, dp, timbrecli, count = line.split(';')
    if codcde == current_commande:
            continue
    else:
        liste_tempo.append({'ville':ville,'nbcolis':nbcolis, 'timbrecde': float(timbrecde), 'timbrecli': timbrecli, 'dept':dp})
        current_commande = codcde

liste = sorted(liste_tempo, key=lambda liste: liste["timbrecde"], reverse=True)
liste_100=[]
for i in range(0,100):
    current_word = liste[i]['ville']+";"+liste[i]['nbcolis']+";"+str(liste[i]['timbrecde'])+";"+liste[i]['timbrecli']+";"+liste[i]['dept']
    ville, nbcolis, timbrecde, timbrecli, dp = current_word.split(";")
    liste_100.append({'ville':ville,'nbcolis':nbcolis, 'timbrecde': str(float(timbrecde)), 'timbrecli': timbrecli, 'dept':dp})

liste_trier= []
for i in range(len(liste_100)):
    current_word = liste_100[i]['ville']+";"+liste_100[i]['nbcolis']+";"+liste_100[i]['timbrecde']+";"+liste_100[i]['timbrecli']+";"+liste_100[i]['dept']
    ville, nbcolis, timbrecde, timbrecli, dp = current_word.split(";")
    print(ville, nbcolis, timbrecde, timbrecli, dp)
    if dp == '53' or dp == '61' or dp == '28':
        if timbrecli == '0':
            liste_trier.append({'ville':ville,'timbrecde':timbrecde, 'nbcolis': nbcolis })

liste_cinq_pourcent = []

for j in range(0, round(len(liste_trier)*0.05)):
    i = int(round(random()*len(liste_trier)-1))
    current_word = liste_trier[i]['ville']+";"+liste_trier[i]['nbcolis']+";"+liste_trier[i]['timbrecde']
    ville, nbcolis, timbrecde = current_word.split(";")
    print('%s' % (current_word))
    table.put(b'%i' % index, {b'cf_info:Ville': '%s' % ville,b'cf_info:Nombre_de_colis': '%s' % nbcolis,b'cf_info:Timbre_code': '%s' % timbrecde})
    liste_cinq_pourcent.append({'ville':ville,'timbrecde':float(timbrecde), 'nbcolis': nbcolis })
    file.write(current_word+'\n')
    index += 1


liste = sorted(liste_cinq_pourcent, key=lambda liste: liste["timbrecde"], reverse=True)
df=pd.DataFrame(liste)
df.to_excel("Resultat_2_2.xlsx")
plt.figure(figsize=(16, 12))

#Créer le graphe pie
plt.pie(df['timbrecde'] ,labels=df['ville'], autopct='%1.1f%%', startangle=140)
plt.title("Somme des timbrecodes sans timbreclient par ville entre 2006 et 2016 dans les département 53, 61, 28 selon un tirage de 5% aléatoire")
connection.close()
# Enregistrer le graphe au format PDF

output_pdf_file = '/root/resultat_2_2.pdf'
with PdfPages(output_pdf_file) as pdf:
    pdf.savefig()
