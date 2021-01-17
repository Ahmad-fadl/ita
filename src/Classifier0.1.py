#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import re
from tqdm import tqdm
import os
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
import re
import numpy as np
nltk.download('wordnet')
directory = "data/Preprocessed_Tweets/"


# In[ ]:


lemmatizer = WordNetLemmatizer()

def lemmatize(tweet):
    """lemmatizes the raw text"""
    text_tweet = str(tweet)
    words = text_tweet.split()
    lemmatized = [None]*len(words)
    for i in range(len(words)):
        lemmatized[i] = lemmatizer.lemmatize(words[i])
    return lemmatized


# In[ ]:


def get_emotions(tweet):
    """    get emotions for ech word in a string

    :param: tweet a string
    :return: returns a list of lists where ech list has the emotions of a word in a string in the ordere 
    'Sentiment anger',  'Sentiment anticipation' , 'Sentiment  disgust', 'Sentiment fear' , 
    'Sentiment joy', 'Sentiment sadness', 'Sentiment surprise' , 'Sentiment trust' """

    tweet_words = lemmatize(tweet)
    emotions=[[] for i in range(len(tweet_words))]
    filepath= "data/Sentiment_Classifier/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
    emolex_df = pd.read_csv(filepath,  names=["word", "emotion", "association"],
                            skiprows=45, sep='\t', keep_default_na=False)
    #subjlex = pd.read_csv("data/Sentiment_Classifier/subjclueslen1-HLTEMNLP05.tff",  
     #                 names=["type", "len", "word1","pos1","stemmed1","priorpolarity"], 
      #                skiprows=0, sep=',', keep_default_na=False)
    j=0
    idx=0
    for word in tweet_words:
        try:
            #get the index of the word in lexikon
            idx = emolex_df.loc[emolex_df['word']== word].index[0]
            for i in range(10):
                emotions[j].append(emolex_df["association"][idx+i]) 
        except:
            #print("Word *"+ word + "* is not in the lexikon")
            for i in range(10):
                emotions[j].append(0)

      
        finally:
            j=j+1         
  
    return emotions


# In[ ]:


def Create_df_with_emotions(Preprocessed_Tweets):
    Sentiment_Tweets = pd.DataFrame(columns=['ID', 'COUNTRY', 'DAY', 
                                             'MONTH', 'TEXT_RAW', 'WORD COUNT',
                                             'LEMMATIZED', 'STRONGSUBJECTIVE', 'WEAKSUBJECTIVE', 
                                             'Sentiment anger',  'Sentiment anticipation' , 'Sentiment  disgust',
                                             'Sentiment fear' , 'Sentiment joy','NEGATIVE','POSITIVE', 'Sentiment sadness', 
                                             'Sentiment surprise' , 'Sentiment trust', 'Capital Letters' ,
                                             'Longest Sequence Capital Letters', "TEXT_RAW_PUNCTUATION"])
    Sentiment_Tweets['ID'] = Preprocessed_Tweets['ID']
    Sentiment_Tweets['COUNTRY'] = Preprocessed_Tweets['COUNTRY']
    Sentiment_Tweets['DAY'] = Preprocessed_Tweets['DAY']
    Sentiment_Tweets['MONTH'] = Preprocessed_Tweets['MONTH']
    Sentiment_Tweets['TEXT_RAW'] = Preprocessed_Tweets['TEXT_RAW']
    Sentiment_Tweets['TEXT_RAW_PUNCTUATION'] = Preprocessed_Tweets['TEXT_RAW_PUNCTUATION']
    for index, row in Sentiment_Tweets.iterrows():
        emotions = get_emotions(row['TEXT_RAW'])
        emotions=np.array([np.array(xi) for xi in emotions])
        #Sentiment_Tweets.at[index,'STRONGSUBJECTIVE'] = np.sum(emotions[:,10])
        #Sentiment_Tweets.at[index,'WEAKSUBJECTIVE'] = np.sum(emotions[:,11])
        Sentiment_Tweets.at[index,'LEMMATIZED'] = lemmatize(row['TEXT_RAW'])
        Sentiment_Tweets.at[index,'WORD COUNT'] = len(Sentiment_Tweets.loc[index,'LEMMATIZED'])
        Sentiment_Tweets.at[index,'Sentiment anger'] = emotions[:,0]
        Sentiment_Tweets.at[index,'Sentiment anticipation'] = emotions[:,1]
        Sentiment_Tweets.at[index,'Sentiment  disgust'] = emotions[:,2]
        Sentiment_Tweets.at[index,'Sentiment fear'] = emotions[:,3]
        Sentiment_Tweets.at[index,'Sentiment joy'] = emotions[:,4]
        Sentiment_Tweets.at[index,'NEGATIVE'] = emotions[:,5]
        Sentiment_Tweets.at[index,'POSITIVE'] = emotions[:,6]
        try:
            Sentiment_Tweets.at[index,'Sentiment sadness'] = emotions[:,7]
        except:
            print("emotions error the emotions list are",emotions,"Tweet ID is",Sentiment_Tweets.at[index,'ID'])
            
  
        Sentiment_Tweets.at[index,'Sentiment surprise'] = emotions[:,8]
        Sentiment_Tweets.at[index,'Sentiment trust'] = emotions[:,9]
        
        
        
        
        
        try:
            Sentiment_Tweets.at[index,'Capital Letters'] = sum(1 for c in row['TEXT_RAW'] if c.isupper())
        except:
            Sentiment_Tweets.at[index,'Capital Letters'] = 0
            
            
            
            
            
            
        try:
            Sentiment_Tweets.at[index,'Longest Sequence Capital Letters'] = max(re.findall('[A-Z]+',row['TEXT_RAW']), key=len)
        except:
            Sentiment_Tweets.at[index,'Longest Sequence Capital Letters'] = 0
            continue
    return Sentiment_Tweets
        
        


# In[ ]:


filepath= "data/Sentiment_Classifier/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
emolex_df = pd.read_csv(filepath,  names=["word", "emotion", "association"], skiprows=45, sep='\t', keep_default_na=False)


# In[ ]:


for entry in tqdm(os.scandir(directory)):
    if not entry.path.endswith(".csv"):
        print(f"skipped {os.path.basename(entry.path)}")    
    Preprocessed_Tweets = pd.read_csv(entry.path)
    Tweets_with_emotions = Create_df_with_emotions(Preprocessed_Tweets)
    Tweets_with_emotions.to_csv("data/Tweetswithemotions/" + os.path.basename(entry.path), index=False, header=True)


# In[ ]:




