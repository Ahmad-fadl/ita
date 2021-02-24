# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
import pandas as pd
import os
# Import the Twython class
from twython import Twython
import json

start = time.time()

tweets_csv = []
directory = "data/Preprocessed_Tweets/"
iterator = 0
for entry in tqdm(os.scandir(directory), total=len(list(os.scandir(directory)))):
    if not entry.path.endswith(".csv"):
        print(f"skipped {os.path.basename(entry.path)}")
        continue

    # Load csv file containing the tweet ID's
    tweets_csv.append(pd.read_csv(entry.path))  # [:5] #only first few rows for testing
    # try:
    #   tweets_csv[iterator].columns = [['ID', 'COUNTRY', 'DAY', 'MONTH', 'TEXT_RAW']]
    # except ValueError as e:
    #   print_log(f"{count_files}. File: {entry.path})\n{e} --------------------")
    #  count_corrupted_files += 1
    # continue

All_Tweets = pd.concat(tweets_csv, axis=0, ignore_index=True)
US_Tweets = All_Tweets.loc[All_Tweets['COUNTRY'] == 'Vereinigte Staaten']
GB_Tweets = All_Tweets.loc[All_Tweets['COUNTRY'] == 'Vereinigtes Königreich']
Ind_Tweets = All_Tweets.loc[All_Tweets['COUNTRY'] == 'Republik Indien']

print(len(US_Tweets))
print(len(GB_Tweets))
print(len(Ind_Tweets))
x = ["USA", "GB", "IND"]
y = [len(US_Tweets), len(GB_Tweets), len(Ind_Tweets)]
fig = plt.figure()
plt.title("Number of tweets in each country")
plt.bar(x, y)
fig.savefig('data/Plots/Number_of_tweets_in_each_country.png')


Number_Tweets_Each_Month = All_Tweets.groupby(['MONTH']).size().reset_index(name='counts')
months = [ "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec","Jan"]
# sort the data by months
Number_Tweets_Each_Month['MONTH'] = pd.Categorical(Number_Tweets_Each_Month['MONTH'], categories=months, ordered=True)
Number_Tweets_Each_Month.sort_values(by='MONTH', inplace=True)
fig = plt.figure()
plt.title("Number of tweets in each month")
plt.bar(Number_Tweets_Each_Month['MONTH'], Number_Tweets_Each_Month["counts"])
fig.savefig('data/Plots/Number_of_tweets_in_each_month.png')


US_Tweets_Each_Month = US_Tweets.groupby(['MONTH']).size().reset_index(name='counts')
# sort the data by months
US_Tweets_Each_Month['MONTH'] = pd.Categorical(US_Tweets_Each_Month['MONTH'], categories=months, ordered=True)
US_Tweets_Each_Month.sort_values(by='MONTH', inplace=True)
GB_Tweets_Each_Month = GB_Tweets.groupby(['MONTH']).size().reset_index(name='counts')
# sort the data by months
GB_Tweets_Each_Month['MONTH'] = pd.Categorical(GB_Tweets_Each_Month['MONTH'], categories=months, ordered=True)
GB_Tweets_Each_Month.sort_values(by='MONTH', inplace=True)
Ind_Tweets_Each_Month = Ind_Tweets.groupby(['MONTH']).size().reset_index(name='counts')
# sort the data by months
Ind_Tweets_Each_Month['MONTH'] = pd.Categorical(Ind_Tweets_Each_Month['MONTH'], categories=months, ordered=True)
Ind_Tweets_Each_Month.sort_values(by='MONTH', inplace=True)

x = np.arange(len(Ind_Tweets_Each_Month['MONTH']))  # the label locations
width = 0.33  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x + width, US_Tweets_Each_Month['counts'], width, label='USA')
rects2 = ax.bar(x, GB_Tweets_Each_Month['counts'], width, label='GB')
rects2 = ax.bar(x - width, Ind_Tweets_Each_Month['counts'], width, label='Ind')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('counts')
ax.set_xticks(x)
ax.set_title('Number of tweets in each country and in each month')
ax.set_xticklabels(Ind_Tweets_Each_Month['MONTH'])
ax.legend()
ax.figure.savefig('data/Plots/Number_of_tweets_in_each_month_and_in_each_country.png')

word_Cloud = All_Tweets["TEXT_RAW"].str.lower().str.split(expand=True).stack().value_counts()[:100]
#word_Cloud = word_Cloud["TEXT_RAW"].str.lower()
word_Cloud = word_Cloud[word_Cloud.index.str.len() > 4]
word_Cloud = word_Cloud[:6]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
word_Cloud.plot.bar(title='most used words in all countries')
ax.tick_params(bottom=False, top=True, left=True, right=True)
ax.tick_params(labelbottom=False, labeltop=True, labelleft=True, labelright=True)
fig.savefig('data/Plots/most_used_words_in_all_countries_country.png')

All_Tweets['char_count'] = All_Tweets['TEXT_RAW'].str.len()

char_count = All_Tweets.groupby(['char_count']).size().reset_index(name='counts').sort_values("char_count",
                                                                                              ascending=False)
fig = plt.figure()
#plt.figure(figsize=(20, 5))
plt.title("Y is the number of tweets and X is the number of chars in each tweet")
plt.bar(np.array(char_count["char_count"]),
        char_count["counts"], width=0.8)
fig.savefig('data/Plots/Char_count_in_all_tweets.png')        


fig = plt.figure()
#plt.figure(figsize=(20, 5))
plt.title("Y is the number of tweets and X is the number of chars in each tweet")
plt.bar(np.array(char_count[char_count["char_count"] < 160]["char_count"]),
        char_count[char_count["char_count"] < 160]["counts"], width=0.8)
fig.savefig('data/Plots/Char_count_in_tweets_less_than_160.png')        


fig = plt.figure()
#plt.figure(figsize=(20, 5))
plt.title("Y is the number of tweets and X is the number of chars in each tweet")
plt.bar(np.array(char_count[char_count["char_count"] >= 120]["char_count"]),
        char_count[char_count["char_count"] >= 120]["counts"], width=0.8)
fig.savefig('data/Plots/Char_count_in_tweets_more_than_120.png') 


fig = plt.figure()
#plt.figure(figsize=(20, 5))
plt.title("Y is the number of tweets and X is the number of chars in each tweet")
plt.bar(np.array(char_count[char_count["char_count"] < 50]["char_count"]),
        char_count[char_count["char_count"] < 50]["counts"], width=0.8)
fig.savefig('data/Plots/Char_count_in_tweets_less_than_50.png')        
