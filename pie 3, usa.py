import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import numpy as np
import os

# Εισάγω το dataframe 

path = os.getcwd()

df = pd.read_csv(path+'\\files_for_plots\\attacks2.csv')

# Παρατήρησα πως υπάρχει 'Shark fishing' και 'Fishing for sharks', οπότε τα 
# ένωσα ως μια δραστηριότητα

df.replace('Shark fishing','Fishing for sharks',inplace=True)

# Αντικαθιστώ όπου δεν υπάρχουν δεδομένα με 'No data'

df['Activity'].fillna('No data',inplace=True)

# φτιάχνω ένα dataframe με τρια columns, στο πρώτο είναι ομαδοποιημένες οι 
# χώρες, στο δεύτερο οι δραστηριότητες και στο τρίτο ο αριθμός των 
# καταγεγραμένων περιστατικών ανά δραστηριότητα.

groupby_country = DataFrame(df.groupby(['Country'])['Activity'].value_counts())

groupby_country.rename(columns={'Activity':'Counts'},inplace=True)
groupby_country.reset_index(level=1,inplace=True)
groupby_country.reset_index(inplace=True)


# Δημιουργώ ένα xlsx αρχείο με την επεξεργασία των δεδομένων που έγινε παραπάνω
# για να το χρησιμοποιήσω στις επόμενες χώρες

groupby_country.to_excel(path+'\\files_for_plots\\groupby_country.xlsx')

# Συγκεντρώνω τις σειρές του dataframe που με ενδια΄φερουν σε κάθε περίπτωση 
# (στη συγκεκριμένη, για τις Ηνωμένες Πολιτείες της Αμερικής).

activities_usa = groupby_country.loc[groupby_country['Country']=='Usa']

# Αποθηκεύω τις δραστηριότητες πριν την επίθεση σου έλαβαν χώρα στην Αυστραλία
# σε xlsx file, ΄ώστε να καθαρ΄ισω τα δεδομένα και να περιγράψω μονολεκτικά 
#όσες δραστηριότητες είναι καταγεγραμμένες περιφραστικά, ώστε να γίνει εφικτή 
# η πλήρης ομαδοποίησή τους.

activities_usa.to_excel(path+'\\files_for_plots\\activities_usa.xlsx')

# Εισάγω το xlsx αρχείο μετά την επεξεργασία

usa_acti=pd.read_excel(path+'\\files_for_plots\\activities_usa_categorized.xlsx')


# Φτιάχνω ένα νεο dataframe όπου είναι ομαδοποιημένες όλλες οι δραστηριότητες

usa_counts=DataFrame(usa_acti.groupby(['Activity_clean'])['Counts'].sum())

# κάνω κάποιες μικροδιορθώσεις στο dataframe

usa_counts.reset_index(inplace=True)
usa_counts.rename(columns={'Activity_clean':'Activity'},inplace=True)

# Επιλέγω να κρατήσω τις δραστηριότητες κατα τις οποίες σημειώνονται οι 
# περισσότερες επιθέσεις ώστε να είναι ευανάγνωστα τα pie plots. Έτσι, τις 
# κατηγορίες κατά τις οποίες σημειώθηκαν λιγότερα από 150 περιστατικά επιθέσεων,
# τις εισάγω στην γενικότερη κατηγορία 'Αλλές δραστηριότητες'.

usa_counts.loc[usa_counts.Counts < 150,'Activity'] = 'Other'


# Μια τελευταία ομαδοποίηση για να συγχωνευτούν όλες οι 'Other' τιμές που
# δημιουργήθηκαν.

usa_counts=usa_counts.groupby('Activity').sum()


# Δημιουργία του pie plot

plt.style.use('_mpl-gallery-nogrid')


x=usa_counts
colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.8, len(x)))

# plot
fig, ax = plt.subplots()
ax.pie(#x=activities['Counts'],
       #bels=activities['Activity'],
       labels = usa_counts.index,
       x=usa_counts['Counts'],
       colors=colors, 
       radius=2, 
       center=(0, 0),
       wedgeprops={"linewidth": 1, "edgecolor": "white"}, 
       frame=False,
       shadow=True,
       autopct='%1.1f%%')

plt.title('Activities before attack in the Usa',y=1.5,fontdict={'fontsize':17})

plt.show()