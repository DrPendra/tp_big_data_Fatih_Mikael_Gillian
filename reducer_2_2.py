import sys
import happybase
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

current_commande=None
current_count=0
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
    ville , timbrecde, nbcolis, codcde, count = line.split(';')
    if codcde == current_commande:
        current_count += int(count)
    else:
        max_compte+=1
        current_count += int(count)
        liste_tempo.append({'ville':ville,'nbcolis':nbcolis, 'compte':current_count})
        current_count = 0
        current_commande = codcde

liste = sorted(liste_tempo, key=lambda liste: liste["compte"], reverse=True)

for i in range(0,int(round(len(liste_tempo)*0.05))):
    current_word = liste[i]['ville']+";"+liste[i]['nbcolis']+";"+str(liste[i]['compte'])
    ville, nbcolis, compte = current_word.split(";")
    print('%s' % (current_word))
    table.put(b'%i' % index, {b'cf_info:Ville': '%s' % ville,b'cf_info:Nombre_de_colis': '%s' % nbcolis,b'cf_info:Moyenne_compte': '%s' % "{0:.2f}".format(float(max_compte)/float(compte))})
    file.write(current_word+'\n')
    index += 1
connection.close()


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
