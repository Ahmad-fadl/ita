#!/usr/bin/env python
# coding: utf-8

import csv
import re
from tqdm import tqdm
import os
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
import re
import numpy as np
import pandas.errors

os.chdir(os.path.dirname(__file__))  # changes path to current file path, to make sure it works for everyone

nltk.download('wordnet')
directory = "data/Preprocessed_Tweets/"

lemmatizer = WordNetLemmatizer()


def lemmatize(tweet):
    """returns lemmatized tweet of raw text"""
    text_tweet = str(tweet)
    words = text_tweet.split()
    lemmatized = [None]*len(words)
    for i in range(len(words)):
        lemmatized[i] = lemmatizer.lemmatize(words[i])
    return lemmatized


def get_emotions(tweet_words):
    """get emotions for each word in a string
    :param: tweet a string
    :return: returns a list of lists where each list has the emotions of a word in a string in the order
    'Sentiment anger',  'Sentiment anticipation' , 'Sentiment  disgust', 'Sentiment fear' , 
    'Sentiment joy', 'Sentiment sadness', 'Sentiment surprise' , 'Sentiment trust' """

    emotions = [[] for _i in range(len(tweet_words))]
    filepath = "data/Sentiment_Classifier/NRC-Emotion-Lexicon-Senselevel-v0.92.txt"
    emolex_df = pd.read_csv(filepath,  names=["word", "emotion", "association"],
                            skiprows=45, sep='\t', keep_default_na=False)
    #subjlex = pd.read_csv("data/Sentiment_Classifier/subjclueslen1-HLTEMNLP05.tff",  
    #                names=["type", "len", "word1","pos1","stemmed1","priorpolarity"],
    #                skiprows=0, sep=',', keep_default_na=False)

    j = 0
    for word in tweet_words:
        word = word.lower()
        try:
            # get the index of the word in lexikon
            idx = emolex_df.loc[emolex_df['word'] == word].index[0]
            for i in range(10):
                emotions[j].append(emolex_df["association"][idx+i]) 
        except:
            # print("Word *"+ word + "* is not in the lexikon")
            for i in range(10):
                emotions[j].append(0)
       
        #"""
         #try:
          #  subj_index = subjlex.loc[subjlex["word1"]==word].index[0]  
           # if subjlex.at[subj_index,"type"]=="strongsubj":
            #    emotions[j].append(1)
             #   emotions[j].append(0)
            #if subjlex.at[subj_index,"type"]=="weaksubj":    
             #   emotions[j].append(0)
              #  emotions[j].append(1)
        #except:
         #   emotions[j].append(0)
        #  emotions[j].append(0) """
        finally:
            j = j+1
  
    return emotions


def create_df_with_emotions(Preprocessed_Tweets):
    Sentiment_Tweets = pd.DataFrame(columns=['ID', 'COUNTRY', 'DAY', 
                                             'MONTH', 'TEXT_RAW', 'WORD COUNT',
                                             'LEMMATIZED', 'STRONGSUBJECTIVE', 'WEAKSUBJECTIVE', 
                                             'Sentiment anger',  'Sentiment anticipation', 'Sentiment  disgust',
                                             'Sentiment fear', 'Sentiment joy', 'NEGATIVE', 'POSITIVE',
                                             'Sentiment sadness', 'Sentiment surprise', 'Sentiment trust',
                                             'Capital Letters', 'Longest Sequence Capital Letters',
                                             "TEXT_RAW_PUNCTUATION"])
    Sentiment_Tweets['ID'] = Preprocessed_Tweets['ID']
    Sentiment_Tweets['COUNTRY'] = Preprocessed_Tweets['COUNTRY']
    Sentiment_Tweets['DAY'] = Preprocessed_Tweets['DAY']
    Sentiment_Tweets['MONTH'] = Preprocessed_Tweets['MONTH']
    Sentiment_Tweets['TEXT_RAW'] = Preprocessed_Tweets['TEXT_RAW']
    Sentiment_Tweets['TEXT_RAW_PUNCTUATION'] = Preprocessed_Tweets['TEXT_RAW_PUNCTUATION']
    for index, row in Sentiment_Tweets.iterrows():
        tweet_words = lemmatize(row['TEXT_RAW'])
        emotions = get_emotions(tweet_words)
        emotions = np.array([np.array(xi) for xi in emotions])
        #Sentiment_Tweets.at[index,'STRONGSUBJECTIVE'] = np.sum(emotions[:,10])
        #Sentiment_Tweets.at[index,'WEAKSUBJECTIVE'] = np.sum(emotions[:,11])
        Sentiment_Tweets.at[index, 'LEMMATIZED'] = tweet_words
        Sentiment_Tweets.at[index, 'WORD COUNT'] = len(Sentiment_Tweets.loc[index, 'LEMMATIZED'])
        Sentiment_Tweets.at[index, 'Sentiment anger'] = emotions[:,0]
        Sentiment_Tweets.at[index, 'Sentiment anticipation'] = emotions[:,1]
        Sentiment_Tweets.at[index, 'Sentiment  disgust'] = emotions[:,2]
        Sentiment_Tweets.at[index, 'Sentiment fear'] = emotions[:,3]
        Sentiment_Tweets.at[index, 'Sentiment joy'] = emotions[:,4]
        Sentiment_Tweets.at[index, 'NEGATIVE'] = emotions[:,5]
        Sentiment_Tweets.at[index, 'POSITIVE'] = emotions[:,6]
        try:
            Sentiment_Tweets.at[index,'Sentiment sadness'] = emotions[:,7]
        except:
            print("emotions error the emotions list are", emotions, "Tweet ID is", Sentiment_Tweets.at[index, 'ID'])
        Sentiment_Tweets.at[index, 'Sentiment surprise'] = emotions[:,8]
        Sentiment_Tweets.at[index, 'Sentiment trust'] = emotions[:,9]
        
        try:
            Sentiment_Tweets.at[index, 'Capital Letters'] = sum(1 for c in row['TEXT_RAW'] if c.isupper())
        except:
            Sentiment_Tweets.at[index, 'Capital Letters'] = 0
        
        try:
            Sentiment_Tweets.at[index, 'Longest Sequence Capital Letters'] = max(re.findall('[A-Z]+', row['TEXT_RAW']), key=len)
        except:
            Sentiment_Tweets.at[index, 'Longest Sequence Capital Letters'] = 0
    return Sentiment_Tweets


target_path = "data/Sentiment_Tweets/TweetsWithEmotions"

if not os.path.exists(target_path):
    os.mkdir(target_path)

for entry in tqdm(list(os.scandir(directory))):

    # checks if file already exist, so you can stop/continue anytime with generating the files
    if os.path.exists(target_path + "/" + os.path.basename(entry.path)):
        continue

    if not entry.path.endswith(".csv"):
        print(f"skipped {os.path.basename(entry.path)}")
        continue

    try:
        Preprocessed_Tweets = pd.read_csv(entry.path)
    except pandas.errors.ParserError:
        print(f"pandas.errors.ParserError. Skipped {os.path.basename(entry.path)}")
        continue

    Tweets_with_emotions = create_df_with_emotions(Preprocessed_Tweets)
    Tweets_with_emotions.to_csv(target_path + "/" + os.path.basename(entry.path), index=False, header=True)

