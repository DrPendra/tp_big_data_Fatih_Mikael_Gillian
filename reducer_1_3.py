import sys
import happybase
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import pandas as pd
current_object = None
current_annee = None
qte_max=1
word = None
index = 0
table = None
connection = happybase.Connection('127.0.0.1', 9090)
connection.open()
tableName = b"Statistiques_1_3"
if tableName in set(connection.tables()):
  connection.delete_table(tableName, disable=True)

connection.create_table(tableName, {'cf_info': dict()})

table = connection.table(tableName)

fileName = "st_1_3.txt"
file = open(fileName, "w")
x=[]
y=[]
label=[]
# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace

    line = line.strip()

    # parse the input we got from mapper.py
    libelle_obj,qte, annee = line.split(';')
    word = libelle_obj +';'+qte+';'+annee
    # sotcke dans une dict word et count : maliste

    # Déclenche un tri sur la liste

    # for word, count in maliste
    # convert count (currently a string) to int


    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if libelle_obj == current_object and annee == current_annee:
        qte_max += int(qte)
    else:
        if current_annee:
            cur_city,cur_obj,cur_annee = word.split(';')
            # write result to STDOUT
            print('%s' % (word))
            table.put(b'%i' % index, {b'cf_info:libelle_obj': '%s' % libelle_obj,b'cf_info:qte': '%s' % str(qte_max),b'cf_info:annee': '%s' % annee})
            x.append(int(annee))
            y.append(int(qte_max))
            label.append(libelle_obj)
            file.write(word + "\n")
        index += 1
        qte = 1
        current_annee = annee
        current_object = libelle_obj




# do not forget to output the last word if needed!
print('%s' % (word))
table.put(b'%i' % index, {b'cf_info:libelle_obj': '%s' % libelle_obj,b'cf_info:qte': '%s' % qte,b'cf_info:annee': '%s' % annee})
x.append(int(annee))
y.append(int(qte_max))
label.append(libelle_obj)
file.write(word +'\n')
connection.close()


# Créer une nouvelle figure
plt.figure()

# Créer le graphe pie
plt.plot(x, y,  label=label)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Courbe de croissance de chaque objet")

# Enregistrer le graphe au format PDF

output_pdf_file = '/root/resultat_1_3.pdf'
with PdfPages(output_pdf_file) as pdf:
    pdf.savefig()  # Sauvegarder le graphe dans le fichier PDF'''
