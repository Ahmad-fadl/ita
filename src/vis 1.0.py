#!/usr/bin/env python
# coding: utf-8

# In[46]:


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
 


# In[47]:


All_Tweets = pd.concat(tweets_csv, axis=0, ignore_index=True)
US_Tweets =All_Tweets.loc[All_Tweets['COUNTRY'] == 'Vereinigte Staaten']
GB_Tweets =All_Tweets.loc[All_Tweets['COUNTRY'] == 'Vereinigtes Königreich']
Ind_Tweets =All_Tweets.loc[All_Tweets['COUNTRY'] == 'Republik Indien']  


# In[48]:


print(np.unique(US_Tweets['MONTH']))
print(US_Tweets.columns)


# In[49]:


print(len(US_Tweets))
print(len(GB_Tweets))
print(len(Ind_Tweets))
x=["USA","GB","IND"]
y= [len(US_Tweets),len(GB_Tweets),len(Ind_Tweets)]
plt.title("Number of tweets in each country")
plt.bar(x,y)
plt.show()  


# In[50]:


Number_Tweets_Each_Month = All_Tweets.groupby(['MONTH']).size().reset_index(name='counts')
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# sort the data by months
Number_Tweets_Each_Month['MONTH'] = pd.Categorical(Number_Tweets_Each_Month['MONTH'], categories=months, ordered=True)
Number_Tweets_Each_Month.sort_values(by='MONTH',inplace=True)
plt.title("Number of tweets in each month")
plt.bar(Number_Tweets_Each_Month['MONTH'],Number_Tweets_Each_Month["counts"])
plt.show()  


# In[51]:


US_Tweets_Each_Month=US_Tweets.groupby(['MONTH']).size().reset_index(name='counts')
# sort the data by months
US_Tweets_Each_Month['MONTH'] = pd.Categorical(US_Tweets_Each_Month['MONTH'], categories=months, ordered=True)
US_Tweets_Each_Month.sort_values(by='MONTH',inplace=True)
GB_Tweets_Each_Month=GB_Tweets.groupby(['MONTH']).size().reset_index(name='counts')
# sort the data by months
GB_Tweets_Each_Month['MONTH'] = pd.Categorical(GB_Tweets_Each_Month['MONTH'], categories=months, ordered=True)
GB_Tweets_Each_Month.sort_values(by='MONTH',inplace=True)
Ind_Tweets_Each_Month=Ind_Tweets.groupby(['MONTH']).size().reset_index(name='counts')
# sort the data by months
Ind_Tweets_Each_Month['MONTH'] = pd.Categorical(Ind_Tweets_Each_Month['MONTH'], categories=months, ordered=True)
Ind_Tweets_Each_Month.sort_values(by='MONTH',inplace=True)


# In[52]:


x = np.arange(len(Ind_Tweets_Each_Month['MONTH']))  # the label locations
width = 0.33  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x + width, US_Tweets_Each_Month['counts'], width, label='USA')
rects2 = ax.bar(x  , GB_Tweets_Each_Month['counts'], width, label='GB')
rects2 = ax.bar(x - width , Ind_Tweets_Each_Month['counts'], width, label='Ind')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('counts')
ax.set_title('Number of tweets in each country and in each month')
ax.set_xticks(x)
ax.set_xticklabels(Ind_Tweets_Each_Month['MONTH'])
ax.legend()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




