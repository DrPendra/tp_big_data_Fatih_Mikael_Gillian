import sys
import happybase
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

current_word = None
current_count = 0
word = None
index = 0
table = None
connection = happybase.Connection('127.0.0.1', 9090)
connection.open()
tableName = "Statistiques_1_1"
if tableName in set(connection.tables()):
  connection.delete_table(tableName, disable=True)
table = connection.table(tableName)

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace

    line = line.strip()

    # parse the input we got from mapper.py
    city,obj,annee,count = line.split(';')
    word = city+";"+obj+";"+annee

    # sotcke dans une dict word et count : maliste

    # Déclenche un tri sur la liste

    # for word, count in maliste
    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word:
        current_count += count
    else:
        if current_word:
            cur_city,cur_obj,cur_annee = word.split(';')
            # write result to STDOUT
            print('%s\t%s' % (current_word, current_count))
            table.put(b'%i' % index, {b'cf_info:city': '%s' % cur_city,b'cf_info:obj': '%s' % cur_obj,b'cf_info:annee': '%s' % cur_annee, b'cf_info:count': '%i' % current_count})

        current_count = count
        current_word = word
        index += 1



# do not forget to output the last word if needed!
if current_word == word:
    cur_city,cur_obj,cur_annee = word.split(';')
    print('%s\t%s' % (current_word, current_count))
    table.put(b'%i' % index, {b'cf_info:city': '%s' % cur_city,b'cf_info:obj': '%s' % cur_obj,b'cf_info:annee': '%s' % cur_annee, b'cf_info:count': '%i' % current_count})

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
