import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import numpy as np
import os

# Εισάγω το αρχείο που έχω δημιουργήσει, στο οποίο όλες οι δραστητιότητες είναι
# ομαδοποιημένες ανά χώρα

path=os.getcwd()

df_sa = pd.read_excel(path+'\\files_for_plots\\groupby_country.xlsx')

# Διαλέγω τις σειρές της South Africa

df_sa=df_sa.loc[df_sa['Country']=='South Africa']

# τις αποθηκεύω σε ένα xlsx αρχείο για να τις επεξεργαστώ/καθαρίσω

df_sa.to_excel(path+'\\files_for_plots\\activities_sa.xlsx')

# εισάγω το νέο αρχείο 

sa_acti=pd.read_excel(path+'\\files_for_plots\\activities_sa_categorized.xlsx')

# Αθροίζω όλα τα περιστατικά για κάθε δραστηριότητα

sa_counts=DataFrame(sa_acti.groupby(['Activity_clean'])['Counts'].sum())

sa_counts.reset_index(inplace=True)
sa_counts.rename(columns={'Activity_clean':'Activity'},inplace=True)

# Επιλέγω να κρατήσω τις δραστηριότητες κατα τις οποίες σημειώνονται οι περισσότερες επιθέσεις ώστε να είναι ευανάγνωστα 
# τα pie plots. Έτσι, τις κατηγορίες κατά τις οποίες σημειώθηκαν λιγότερα από 50 περιστατικά επιθέσεων, τις εισάγω 
# στην γενικότερη κατηγορία 'Αλλές δραστηριότητες'.

sa_counts.loc[sa_counts.Counts < 50,'Activity'] = 'Other'

sa_counts=sa_counts.groupby('Activity').sum()


plt.style.use('_mpl-gallery-nogrid')


# make data
x=sa_counts
colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.8, len(x)))

# plot
fig, ax = plt.subplots()
ax.pie(#x=activities['Counts'],
       #bels=activities['Activity'],
       labels = sa_counts.index,
       x=sa_counts['Counts'],
       colors=colors, 
       radius=2, 
       center=(0, 0),
       wedgeprops={"linewidth": 1, "edgecolor": "white"}, 
       frame=False,
       shadow=True,
       autopct='%1.1f%%')

plt.title('Activities before attack in South Africa',y=1.5,fontdict={'fontsize':17})

plt.show()
