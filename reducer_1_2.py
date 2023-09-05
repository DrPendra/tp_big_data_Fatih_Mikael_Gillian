import sys
import happybase
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np
from functools import cmp_to_key

current_cli = None
cli = None
index = 0
table = None
'''connection = happybase.Connection('127.0.0.1', 9090)
connection.open()
tableName = b"Statistiques_1_2"
if tableName in set(connection.tables()):
  connection.delete_table(tableName, disable=True)

connection.create_table(tableName, {'cf_info': dict()})

table = connection.table(tableName)'''

fileName = "st_1_2.txt"
file = open(fileName, "w")

clientList = []
current_cli_cmd = []

for line in sys.stdin:

    line = line.strip()
    codeCli,nomCli,prenomCli,dep,city,nbColis = line.split(';')
    #word =  nomCli+";"+prenomCli+";"+dep+";"+city
    cli = codeCli+";"+nomCli+";"+prenomCli
    try:
        nbColis = int(nbColis)
    except ValueError:
        continue

    if current_cli == cli:
        current_cli_cmd.append({'dep':dep,'city':city,'nbColis':nbColis})

    else:
        if current_cli:
            #cur_nomCli,cur_prenomCli,cur_dep,cur_city = word.split(';')
            # write result to STDOUT
            #print('%s\t%s' % (current_word+";"+  str(current_nbColis), current_count))
            #table.put(b'%i' % index, {b'cf_info:nomCli': '%s' % cur_nomCli,b'cf_info:prenomCli': '%s' % cur_prenomCli,b'cf_info:dep': '%s' % cur_dep, b'cf_info:city': '%i' % cur_city, b'cf_info:city': '%i' % cur_city})
            #file.write(current_word + ";"+str(current_count)+"\n")
            clientList.append({'cli':current_cli,'cmd':current_cli_cmd})
        current_cli_cmd = []
        current_cli = cli
        index += 1



# do not forget to output the last word if needed!
if current_cli == cli:
    #nomCli,prenomCli,dep,city = word.split(';')
    #print('%s\t%s' % (current_word+";"+ str(current_nbColis), current_count))
    #table.put(b'%i' % index, {b'cf_info:city': '%s' % cur_city,b'cf_info:obj': '%s' % cur_obj,b'cf_info:annee': '%s' % cur_annee, b'cf_info:count': '%i' % current_count})
    #file.write(current_word + ";"+str(current_count)+"\n")
    clientList.append({'cli':current_cli,'cmd':current_cli_cmd})
#connection.close()

    
def comparator(a, b):
        #print(a)
        if int(len(a["cmd"])) > int(len(b["cmd"])):
            return -1
        if int(len(a["cmd"])) < int(len(b["cmd"])):
            return 1
        if a["cli"] > b["cli"]:
            return -1
        if a["cli"] < b["cli"]:
            return 1
        return 0


data = sorted(clientList, key=cmp_to_key(comparator))

#[print(e["cli"] + " "+ str(len(e["cmd"]))) for e in data[0:10]]
codes = []
noms = []
prenoms = []
deps = []
cities = []
dataNbColis = []

for e in data[0:10]:
    for cmd in e['cmd']:
        code,nom,pre = e["cli"].split(';')
        codes.append(code)
        noms.append(nom)
        prenoms.append(pre)
        deps.append(cmd['dep'])
        cities.append(cmd['city'])
        dataNbColis.append(cmd['nbColis'])




'''for e in data[0:10]:
    nomCli,prenomCli,dep,city,nbColis = e["info"].split(';')
    noms.append(nomCli)
    prenoms.append(prenomCli)
    deps.append(dep)
    cities.append(city)
    dataNbColis.append(int(nbColis))'''

data = {
    'Code': codes,
    'Nom': noms,
    'Prenom': prenoms,
    'Departement': deps,
    'Ville': cities,
    'NbColis': dataNbColis
}

df = pd.DataFrame(data)

distinct_df_ville = df['Ville'].drop_duplicates()
nb_Ville = len(distinct_df_ville)
for j in range(nb_Ville):
    ville = distinct_df_ville.iloc[j]
    output_pdf_file = '/datavolume1/resultat_1_2_' + ville + ".pdf"
    pdf_pages = PdfPages(output_pdf_file)


    filtered_df = df.loc[df['Ville'] == ville, ['Code','Nom','Prenom']]
    distinct_df = filtered_df.drop_duplicates()

    nb_graphes = len(distinct_df)
    fig, a = plt.subplots(1, nb_graphes, figsize=(15, 4))
    plt.title("Ville de " + ville)
    axes = None

    if type(a) is not list:
        axes = [a]
    else:
        axes = a
    titre = pd.DataFrame({'Code': ['Code'], 'Nom': ['Nom'], 'Prenom': ['Prenom'], 'NbColis_x': ['Somme des colis'], 'NbColis_y':['Moyenne des colis'],'NbColis':['Ecart-type des colis']})


    # Boucle pour créer un sous-graphique pour chaque ligne de données
    for i in range(nb_graphes):
        df_cli = df.loc[df['Code'] == distinct_df.iloc[i]['Code']]
        df_cli_sum = df_cli.groupby(['Code','Nom','Prenom'])['NbColis'].sum().reset_index().round(2)
        df_cli_mean = df_cli.groupby(['Code','Nom','Prenom'])['NbColis'].mean().reset_index().round(2)
        df_cli_std = df_cli.groupby(['Code','Nom','Prenom'])['NbColis'].std().reset_index().round(2)

        
     

        merged_df = df_cli_sum.merge(df_cli_mean, on=['Nom', 'Prenom','Code']).merge(df_cli_std, on=['Nom', 'Prenom','Code'])
        #resultat = pd.concat([titre,df_cli_sum, df_cli_mean,df_cli_std], axis=0)
        '''merged_df["NbColis"] = round(merged_df["NbColis"],2)
        merged_df["NbColis_y"] = round(merged_df["NbColis_y"],2)
        merged_df["NbColis_x"] = round(merged_df["NbColis_x"],2)'''

        resultat = pd.concat([titre,merged_df], axis=0)

        '''resultat["NbColis"] = float(resultat["NbColis"]).round(2)
        resultat["NbColis_y"] = float(resultat["NbColis_y"]).round(2)
        resultat["NbColis_x"] = float(resultat["NbColis_x"]).round(2)'''

        print(resultat)
        print()
        
        table = axes[i].table(cellText=resultat.values, loc='center', cellLoc='center', colLabels=None)

        # Personnalisation du tableau
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 1.5)  # Ajuste la taille du tableau

        # Cache les axes du sous-graphique
        axes[i].axis('off')


    pdf_pages.savefig(fig)
    plt.close(fig)

    pdf_pages.close()

