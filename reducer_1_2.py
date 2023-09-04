import sys
import happybase
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from functools import cmp_to_key

current_word = None
current_count = 0
current_nbColis = 0
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
        current_nbColis += nbColis
    else:
        if current_word:
            cur_nomCli,cur_prenomCli,cur_dep,cur_city = word.split(';')
            # write result to STDOUT
            print('%s\t%s' % (current_word+";"+  str(current_nbColis), current_count))
            #table.put(b'%i' % index, {b'cf_info:nomCli': '%s' % cur_nomCli,b'cf_info:prenomCli': '%s' % cur_prenomCli,b'cf_info:dep': '%s' % cur_dep, b'cf_info:city': '%i' % cur_city, b'cf_info:city': '%i' % cur_city})
            #file.write(current_word + ";"+str(current_count)+"\n")
            clientList.append({'info':current_word+";"+str(current_nbColis),'qte':current_count})
        current_count = 1
        current_word = word
        current_nbColis = nbColis
        index += 1



# do not forget to output the last word if needed!
if current_word == word:
    nomCli,prenomCli,dep,city = word.split(';')
    print('%s\t%s' % (current_word+";"+ str(current_nbColis), current_count))
    #table.put(b'%i' % index, {b'cf_info:city': '%s' % cur_city,b'cf_info:obj': '%s' % cur_obj,b'cf_info:annee': '%s' % cur_annee, b'cf_info:count': '%i' % current_count})
    #file.write(current_word + ";"+str(current_count)+"\n")
    clientList.append({'info':current_word+";"+str(current_nbColis),'qte':current_count})
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


noms = []
prenoms = []
deps = []
cities = []
dataNbColis = []

for e in data[0:10]:
    nomCli,prenomCli,dep,city,nbColis = e["info"].split(';')
    noms.append(nomCli)
    prenoms.append(prenomCli)
    deps.append(dep)
    cities.append(city)
    dataNbColis.append(int(nbColis))

data = {
    'Nom': noms,
    'Prenom': prenoms,
    'Departement': deps,
    'Ville': cities,
    'NbColis': dataNbColis
}

df = pd.DataFrame(data)
# Créer une nouvelle figure
'''plt.figure()

# Créer le graphe pie
plt.pie(data['NbColis'], labels=data['Ville'], autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Répartition des commandes par département")
# Enregistrer le graphe au format PDF'''

output_pdf_file = '/datavolume1/resultat.pdf'
pdf_pages = PdfPages(output_pdf_file)

df_nbColis_Ville = df.groupby('Ville')['NbColis'].sum().reset_index()
#print(df_nbColis_Ville)
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.bar(df_nbColis_Ville['Ville'], df_nbColis_Ville['NbColis'])
ax1.set_xlabel('Ville')
ax1.set_ylabel('Nombre Colis')
ax1.set_title('Nombre de colis par ville')
ax1.set_xticklabels(df_nbColis_Ville['Ville'], rotation=45)
pdf_pages.savefig(fig1)
plt.close(fig1)

'''df_meanColis_Ville = df.groupby('Ville')['NbColis'].mean().reset_index()
fig2 = plt.figure()
ax2 = fig1.add_subplot(111)
ax2.bar(df_meanColis_Ville['Ville'], df_meanColis_Ville['NbColis'])
ax2.set_xlabel('Ville')
ax2.set_ylabel('Moyenne Nombre Colis')
ax2.set_title('Moyenne de Nombre de colis par ville')
ax2.set_xticklabels(df_meanColis_Ville['Ville'], rotation=45)
pdf_pages.savefig(fig2)
plt.close(fig2)'''

# Fermez l'objet PdfPages pour enregistrer le fichier PDF final
pdf_pages.close()
