#!/usr/bin/env python
# coding: utf-8

# In[11]:


import numpy as np
import matplotlib.pyplot as plt

import time
from tqdm import tqdm
start = time.time()

import pandas as pd
import os

# Import the Twython class
from twython import Twython
import json
#save the data from csv to a dataframe
tweets_csv=[]
directory= "data/Hydrated_Tweets/"
iterator = 0
for entry in tqdm(os.scandir(directory), total=len(list(os.scandir(directory)))):
    if not entry.path.endswith(".csv"):
        print(f"skipped {os.path.basename(entry.path)}")


    # Load csv file containing the tweet ID's
    tweets_csv.append(pd.read_csv(entry.path))  # [:5] #only first few rows for testing
    #try:
     #   tweets_csv[iterator].columns = [['ID', 'COUNTRY', 'DAY', 'MONTH', 'TEXT_RAW']]
    #except ValueError as e:
     #   print_log(f"{count_files}. File: {entry.path})\n{e} --------------------")
      #  count_corrupted_files += 1
       # continue
 


# In[16]:


All_Tweets = pd.concat(tweets_csv, axis=0, ignore_index=True)
US_Tweets =All_Tweets.loc[All_Tweets['COUNTRY'] == 'Vereinigte Staaten']
GB_Tweets =All_Tweets.loc[All_Tweets['COUNTRY'] == 'Vereinigtes Königreich']
Ind_Tweets =All_Tweets.loc[All_Tweets['COUNTRY'] == 'Republik Indien']  


# In[17]:

#a
print(np.unique(US_Tweets['MONTH']))
print(US_Tweets.columns)


# In[51]:


temp = US_Tweets.loc[US_Tweets['MONTH'] == 'Jul']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 4)
plt.title("number of tweets USA Jul")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = US_Tweets.loc[US_Tweets['MONTH'] == 'Dec']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 1)
plt.title("number of tweets USA Dec")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = US_Tweets.loc[US_Tweets['MONTH'] == 'Apr']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 2)
plt.title("number of tweets USA April")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = US_Tweets.loc[US_Tweets['MONTH'] == 'Aug']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 3)
plt.title("number of tweets USA Aug")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))

plt.show()

temp = US_Tweets.loc[US_Tweets['MONTH'] == 'Jun']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 4)
plt.title("number of tweets USA Jun")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = US_Tweets.loc[US_Tweets['MONTH'] == 'Mar']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 1)
plt.title("number of tweets USA Mar")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = US_Tweets.loc[US_Tweets['MONTH'] == 'Nov']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 2)
plt.title("number of tweets USA Nov")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = US_Tweets.loc[US_Tweets['MONTH'] == 'Oct']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 3)
plt.title("number of tweets USA Oct")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))

plt.show()


plt.subplot(1, 2, 1)
plt.title("number of tweets USA Oct")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = US_Tweets.loc[US_Tweets['MONTH'] == 'May']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(1, 2, 2)
plt.title("number of tweets USA May")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = US_Tweets.loc[US_Tweets['MONTH'] == 'Sep']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 2)
plt.title("number of tweets USA Sep")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
plt.show()


# In[54]:


temp = GB_Tweets.loc[GB_Tweets['MONTH'] == 'Jul']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 4)
plt.title("number of tweets GB Jul")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = GB_Tweets.loc[GB_Tweets['MONTH'] == 'Dec']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 1)
plt.title("number of tweets GB Dec")
plt.scatter(np.array((GB_Tweets['DAY'])),np.array(temp['freq']))
temp = GB_Tweets.loc[GB_Tweets['MONTH'] == 'Apr']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 2)
plt.title("number of tweets GB April")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = GB_Tweets.loc[GB_Tweets['MONTH'] == 'Aug']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 3)
plt.title("number of tweets GB Aug")
plt.scatter(np.array((GB_Tweets['DAY'])),np.array(temp['freq']))

plt.show()

temp = GB_Tweets.loc[GB_Tweets['MONTH'] == 'Jun']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 4)
plt.title("number of tweets GB Jun")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = GB_Tweets.loc[GB_Tweets['MONTH'] == 'Mar']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 1)
plt.title("number of tweets GB Mar")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = GB_Tweets.loc[GB_Tweets['MONTH'] == 'Nov']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 2)
plt.title("number of tweets GB Nov")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = GB_Tweets.loc[GB_Tweets['MONTH'] == 'Oct']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 3)
plt.title("number of tweets GB Oct")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))

plt.show()


plt.subplot(1, 2, 1)
plt.title("number of tweets GB Oct")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = GB_Tweets.loc[GB_Tweets['MONTH'] == 'May']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(1, 2, 2)
plt.title("number of tweets GB May")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = GB_Tweets.loc[GB_Tweets['MONTH'] == 'Sep']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 2)
plt.title("number of tweets GB Sep")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
plt.show()

#indien
temp = Ind_Tweets.loc[Ind_Tweets['MONTH'] == 'Jul']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 4)
plt.title("number of tweets India Jul")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = Ind_Tweets.loc[Ind_Tweets['MONTH'] == 'Dec']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 1)
plt.title("number of tweets India Dec")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = Ind_Tweets.loc[Ind_Tweets['MONTH'] == 'Apr']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 2)
plt.title("number of tweets India April")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = Ind_Tweets.loc[Ind_Tweets['MONTH'] == 'Aug']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 3)
plt.title("number of tweets India Aug")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))

plt.show()

temp = Ind_Tweets.loc[Ind_Tweets['MONTH'] == 'Jun']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 4)
plt.title("number of tweets India Jun")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = Ind_Tweets.loc[Ind_Tweets['MONTH'] == 'Mar']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 1)
plt.title("number of tweets India Mar")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = Ind_Tweets.loc[Ind_Tweets['MONTH'] == 'Nov']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 2)
plt.title("number of tweets India Nov")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = Ind_Tweets.loc[Ind_Tweets['MONTH'] == 'Oct']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 3)
plt.title("number of tweets India Oct")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))

plt.show()


plt.subplot(1, 2, 1)
plt.title("number of tweets India Oct")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = Ind_Tweets.loc[Ind_Tweets['MONTH'] == 'May']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(1, 2, 2)
plt.title("number of tweets India May")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
temp = Ind_Tweets.loc[Ind_Tweets['MONTH'] == 'Sep']
temp['freq'] = temp.groupby('DAY')['DAY'].transform('count')
temp = temp[['DAY' ,'freq']]
plt.subplot(2, 2, 2)
plt.title("number of tweets India Sep")
plt.scatter(np.array((temp['DAY'])),np.array(temp['freq']))
plt.show()



# In[ ]:





