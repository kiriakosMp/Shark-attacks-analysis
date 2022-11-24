# -*- coding: utf-8 -*-


import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import numpy as np
import os


"""
Σε μεγάλο ποσοστό των καταγεγραμμένων περιστατικών η δραστηριότητα του θύματος 
πριν την επίθεση από καρχαρία περιγραφόταν περιφραστικά με αποτέλεσμανα το 
dataset να χρειάζεται περαιτέρω επεξεργασία. Στο παρακάτω csv αρχείο, 
αντικατέστησα τις περιφραστικές περιγραφές με περιγραφές μιας ή δύο λέξεων 
(πχ fishing, swimming), ώστε να μπορέσουν να κατηγοριοποιηθούν όλες οι 
παρόμοιες δραστηριότητες μαζί και να λάβουμε την πλήρη εικόνα.
"""
path=os.getcwd()

df = pd.read_csv(path+'\\files_for_plots\\activities_clean2.csv') 


# συμπληρώνω όσες δραστηριότητες για τις οποίες δεν έχουμε 
# δεδομένα ως 'Άλλη δραστηριότητα'

df['Activity'].fillna('Other',inplace=True) 


# αθροίζω τον αριθμό των καταγεγραμένων περιστατικών 

df=df.groupby('Activity').sum() 

df.reset_index(inplace=True)


# για πιο ευδιάκριτα αποτελέσματα, τις δραστηριότητες για τις οποίες τα 
#καταγεγραμένα περιστατικά είναι λιγότερα από 200, 
# τις κατηγοροποιώ ως 'άλλες δραστηριότητες'

df.loc[df.Counts <= 200,'Activity'] = 'Other'


# κατηγοριοποιώ ξανά τις δραστηριότητες 

df=df.groupby('Activity').sum()

plt.style.use('_mpl-gallery-nogrid')


# make data

colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.8, len(df)))

# plot
fig, ax = plt.subplots()
ax.pie(labels = df.index,
       x=df['Counts'],
       colors=colors, 
       radius=2, 
       center=(0, 0),
       wedgeprops={"linewidth": 1, "edgecolor": "white"}, 
       frame=False,
       shadow=True,
       autopct='%1.1f%%')

plt.title('Activities before shark attack, globally.',y=1.5,fontdict={'fontsize':17})

plt.show()
