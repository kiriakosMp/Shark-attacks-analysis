import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import numpy as np
import os


# Εισάγω το αρχείο που έχω δημιουργήσει, στο οποίο όλες οι δραστητιότητες είναι
# ομαδοποιημένες ανά χώρα

path=os.getcwd()

df_nz = pd.read_excel(path+'\\files_for_plots\\groupby_country.xlsx')

# Διαλέγω τις σειρές της New Zealand

df_nz=df_nz.loc[df_nz['Country']=='New Zealand']

# τις αποθηκεύω σε ένα xlsx αρχείο για να τις επεξεργαστώ/καθαρίσω

df_nz.to_excel(path+'\\files_for_plots\\activities_nz.xlsx')

# εισάγω το νέο αρχείο 

nz_acti=pd.read_excel(path+'\\files_for_plots\\activities_nz_categorized.xlsx')

# Αθροίζω όλα τα περιστατικά για κάθε δραστηριότητα

nz_counts=DataFrame(nz_acti.groupby(['Activity_clean'])['Counts'].sum())

nz_counts.reset_index(inplace=True)
nz_counts.rename(columns={'Activity_clean':'Activity'},inplace=True)

# Επιλέγω να κρατήσω τις δραστηριότητες κατα τις οποίες σημειώνονται οι
# περισσότερες επιθέσεις ώστε να είναι ευανάγνωστα τα pie plots. Έτσι, τις
# κατηγορίες κατά τις οποίες σημειώθηκαν λιγότερα από 15 περιστατικά επιθέσεων,
# τις εισάγω στην γενικότερη κατηγορία 'Αλλές δραστηριότητες'.

nz_counts.loc[nz_counts.Counts < 15,'Activity'] = 'Other'

nz_counts=nz_counts.groupby('Activity').sum()


# σχηματίζω το plot

plt.style.use('_mpl-gallery-nogrid')


x=nz_counts
colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.8, len(x)))

# plot
fig, ax = plt.subplots()
ax.pie(#x=activities['Counts'],
       #bels=activities['Activity'],
       labels = nz_counts.index,
       x=nz_counts['Counts'],
       colors=colors, 
       radius=2, 
       center=(0, 0),
       wedgeprops={"linewidth": 1, "edgecolor": "white"}, 
       frame=False,
       shadow=True,
       autopct='%1.1f%%')

plt.title('Activities before attack in the New Zealand',y=1.5,fontdict={'fontsize':17})


plt.show()