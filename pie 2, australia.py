import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import numpy as np
import os

path=os.getcwd()

# Εισάγω το dataframe 

df = pd.read_csv(path+'\\files_for_plots\\attacks.csv')


# Παρατήρησα πως υπάρχει 'Shark fishing' και 'Fishing for sharks', 
# οπότε τα ένωσα ως μια δραστηριότητα

df.replace('Shark fishing','Fishing for sharks',inplace=True)


# Αντικαθιστώ όπου δεν υπάρχουν δεδομένα με 'No data'

df['Activity'].fillna('No data',inplace=True)


# φτιάχνω ένα dataframe με τρια columns, στο πρώτο είναι ομαδοποιημένες οι χώρες, 
# στο δεύτερο οι δραστηριότητες και στο τρίτο ο αριθμός των καταγεγραμένων 
# περιστατικών ανά δραστηριότητα.

groupby_country = DataFrame(df.groupby(['Country'])['Activity'].value_counts())


groupby_country.rename(columns={'Activity':'Counts'},inplace=True)
groupby_country.reset_index(level=1,inplace=True)
groupby_country.reset_index(inplace=True)


# Συγκεντρώνω τις σειρές του dataframe που με ενδια΄φερουν σε κάθε 
# περίπτωση (στη συγκεκριμένη, για την Αυστραλία).

activities_australia = groupby_country.loc[groupby_country['Country']=='Australia']


# Αποθηκεύω τις δραστηριότητες πριν την επίθεση σου έλαβαν χώρα στην Αυστραλία
# σε xlsx file, ΄ώστε να καθαρίσω τα δεδομένα και να περιγράψω μονολεκτικά όσες
# δραστηριότητες είναι καταγεγραμμένες περιφραστικά, ώστε να γίνει εφικτή η 
# πλήρης ομαδοποίησή τους.

activities_australia.to_excel(path+'\\files_for_plots\\activities_australia.xlsx')


# Εισάγω το xlsx αρχείο μετά την επεξεργασία

aus_activities=pd.read_excel(path+'\\files_for_plots\\activities_australia_categorized.xlsx')

# Φτιάχνω ένα νεο dataframe όπου είναι ομαδοποιημένες όλλες οι δραστηριότητες

aus_counts=DataFrame(aus_activities.groupby(['Activity_clean'])['Counts'].sum())

# κάνω κάποιες μικροδιορθώσεις στο dataframe

aus_counts.reset_index(inplace=True)
aus_counts.rename(columns={'Activity_clean':'Activity'},inplace=True)


# Επιλέγω να κρατήσω τις δραστηριότητες κατα τις οποίες σημειώνονται οι
# περισσότερες επιθέσεις ώστε να είναι ευανάγνωστα τα pie plots. Έτσι, 
#τις κατηγορίες κατά τις οποίες σημειώθηκαν λιγότερα από 150 περιστατικά 
#επιθέσεων, τις εισάγω στην γενικότερη κατηγορία 'Αλλές δραστηριότητες'.

aus_counts.loc[aus_counts.Counts <= 150,'Activity'] = 'Other'


# Μια τελευταία ομαδοποίηση για να συγχωνευτούν όλες οι 'Other' τιμές που δημιουργήθηκαν.

aus_counts=aus_counts.groupby('Activity').sum()


# Δημιουργία του pie plot

plt.style.use('_mpl-gallery-nogrid')


x=aus_counts
colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.8, len(x)))

# plot
fig, ax = plt.subplots()
ax.pie(labels = aus_counts.index,
       x=aus_counts['Counts'],
       colors=colors, 
       radius=2, 
       center=(0, 0),
       wedgeprops={"linewidth": 1, "edgecolor": "white"}, 
       frame=False,
       shadow=True,
       autopct='%1.1f%%')

plt.title('Activities before attack in Australia',y=1.5,fontdict={'fontsize':17})

plt.show()
