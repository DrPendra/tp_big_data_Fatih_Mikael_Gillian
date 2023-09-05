import pandas as pd
import matplotlib.pyplot as plt

# Exemple de DataFrame avec des valeurs non arrondies
data = {'Col1': [1.234, 2.567, 3.789],
        'Col2': [4.321, 5.432, 6.123],
        'Col3': [7.654, 8.765, 9.876]}

df = pd.DataFrame(data)

# Arrondir les valeurs dans le DataFrame
df_rounded = df.round(2)  # Arrondir à 2 décimales

# Créer le tableau Matplotlib à partir du DataFrame arrondi
fig, ax = plt.subplots()
table = ax.table(cellText=df_rounded.values, colLabels=df_rounded.columns, loc='center')
ax.axis('off')
plt.show()