
import csv
import re
from tqdm import tqdm
import os
import pandas as pd
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def lemmatize(tweet):
    """lemmatizes the raw text"""
    text_tweet = str(tweet)
    words = text_tweet.split()
    lemmatized = []
    for word in words:
        lemma = lemmatizer.lemmatize(word)
        lemmatized.append(lemma)
    return lemmatized

def length(tweet):
    """ returns the amount of tokens in the raw text"""
    return len(tweet.split())


def positives(tweet):
    """ compares the words in the <tweet> to the NRC Emotion lexicon, counts positive words"""
    tweet_words = lemmatize(tweet)
    positive = 0
    with open("data/Sentiment_Classifier/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt") as lex:
        lex_reader = csv.reader(lex, delimiter = '\t')
        for entry in lex_reader:
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "positive" and entry[2] == "1":
                positive += 1
        return positive

def negatives(tweet):
    """ compares the words in the <tweet> to the NRC Emotion lexicon, counts negative words"""
    tweet_words = lemmatize(tweet)
    negative = 0
    with open("data/Sentiment_Classifier/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt") as lex:
        lex_reader = csv.reader(lex, delimiter='\t')
        for entry in lex_reader:
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "negative" and entry[2] == "1":
                negative += 1
        return negative

def subjectivity_strong(tweet):
    """counts the strong subjective words based on the MPQA lexicon.
    Returns the amount of strong subjective words."""
    tweet_words = lemmatize(tweet)
    strong_subj = 0
    with open("data/Sentiment_Classifier/subjclueslen1-HLTEMNLP05.tff", "r") as lex:
        lex_reader = lex.read().splitlines()
        lex_reader_clean = []
        for element in lex_reader:
            element_clean = re.sub("word1=", "", element)
            lex_reader_clean.append(element_clean)
        subjlex = []
        for line in lex_reader_clean:
            subjlex.append(line.split())
        #print(subjlex)
        for entry in subjlex:
            if entry[2] in tweet_words and entry[0] == "type=strongsubj":
                strong_subj += 1
    return strong_subj

def subjectivity_weak(tweet):
    """counts the weak subjective words based on the MPQA lexicon.
    Returns the amount of weak subjective words."""
    tweet_words = lemmatize(tweet)
    weak_subj = 0
    with open("data/Sentiment_Classifier/subjclueslen1-HLTEMNLP05.tff", "r") as lex:
        lex_reader = lex.read().splitlines()
        lex_reader_clean = []
        for element in lex_reader:
            element_clean = re.sub("word1=", "", element)
            lex_reader_clean.append(element_clean)
        subjlex = []
        for line in lex_reader_clean:
            subjlex.append(line.split())
        #print(subjlex)
        for entry in subjlex:
            if entry[2] in tweet_words and entry[0] == "type=weaksubj":
                weak_subj += 1
    return weak_subj

def fine_sentiment_anger(tweet):
    """ compares the words in the <tweet> to the NRC Emotion lexicon, counts the
    amount of words of every sentiment category and calculates the percentage"""
    tweet_words = lemmatize(tweet)
    anger = 0
    with open("./NRC-Emotion-Lexicon-Wordlevel-v0.92.txt") as lex:
        lex_reader = csv.reader(lex, delimiter='\t')
        for entry in lex_reader:
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "anger" and entry[2] == "1":
                anger += 1
        return anger

def fine_sentiment_anticipation(tweet):
    """ compares the words in the <tweet> to the NRC Emotion lexicon, counts the
    amount of words of every sentiment category and calculates the percentage"""
    tweet_words = lemmatize(tweet)
    anticipation = 0
    with open("./NRC-Emotion-Lexicon-Wordlevel-v0.92.txt") as lex:
        lex_reader = csv.reader(lex, delimiter='\t')
        for entry in lex_reader:
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "anticipation" and entry[2] == "1":
                anticipation += 1
        return anticipation

def fine_sentiment_disgust(tweet):
    """ compares the words in the <tweet> to the NRC Emotion lexicon, counts the
    amount of words of every sentiment category and calculates the percentage"""
    tweet_words = lemmatize(tweet)
    disgust = 0
    with open("./NRC-Emotion-Lexicon-Wordlevel-v0.92.txt") as lex:
        lex_reader = csv.reader(lex, delimiter='\t')
        for entry in lex_reader:
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "disgust" and entry[2] == "1":
                disgust += 1
        return disgust

def fine_sentiment_fear(tweet):
    """ compares the words in the <tweet> to the NRC Emotion lexicon, counts the
    amount of words of every sentiment category and calculates the percentage"""
    tweet_words = lemmatize(tweet)
    fear = 0
    with open("./NRC-Emotion-Lexicon-Wordlevel-v0.92.txt") as lex:
        lex_reader = csv.reader(lex, delimiter='\t')
        for entry in lex_reader:
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "fear" and entry[2] == "1":
                fear += 1
        return fear

def fine_sentiment_joy(tweet):
    """ compares the words in the <tweet> to the NRC Emotion lexicon, counts the
    amount of words of every sentiment category and calculates the percentage"""
    tweet_words = lemmatize(tweet)
    joy = 0
    with open("./NRC-Emotion-Lexicon-Wordlevel-v0.92.txt") as lex:
        lex_reader = csv.reader(lex, delimiter='\t')
        for entry in lex_reader:
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "joy" and entry[2] == "1":
                joy += 1
        return joy

def fine_sentiment_sadness(tweet):
    """ compares the words in the <tweet> to the NRC Emotion lexicon, counts the
    amount of words of every sentiment category and calculates the percentage"""
    tweet_words = lemmatize(tweet)
    sadness = 0
    with open("./NRC-Emotion-Lexicon-Wordlevel-v0.92.txt") as lex:
        lex_reader = csv.reader(lex, delimiter='\t')
        for entry in lex_reader:
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "sadness" and entry[2] == "1":
                sadness += 1
        return sadness


def fine_sentiment_surprise(tweet):
    """ compares the words in the <tweet> to the NRC Emotion lexicon, counts the
    amount of words of every sentiment category and calculates the percentage"""
    tweet_words = lemmatize(tweet)
    surprise = 0
    with open("./NRC-Emotion-Lexicon-Wordlevel-v0.92.txt") as lex:
        lex_reader = csv.reader(lex, delimiter='\t')
        for entry in lex_reader:
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "surprise" and entry[2] == "1":
                surprise += 1
        return surprise

def fine_sentiment_trust(tweet):
    """ compares the words in the <tweet> to the NRC Emotion lexicon, counts the
    amount of words of every sentiment category and calculates the percentage"""
    tweet_words = lemmatize(tweet)
    trust = 0
    with open("./NRC-Emotion-Lexicon-Wordlevel-v0.92.txt") as lex:
        lex_reader = csv.reader(lex, delimiter='\t')
        for entry in lex_reader:
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "trust" and entry[2] == "1":
                trust += 1
        return trust


def capital_letters(tweet):
    """ returns the amount of capital letters in Tweet"""
    regex = "[A-Z]"
    regex = re.compile(regex)
    return len(re.findall(regex, tweet))

def capital_letters_longest_sequence(tweet):
    """ returns the number of the longest sequence of capital letters in Tweet"""
    regex_2 = "[A-Z| ]*"
    regex_2 = re.compile(regex_2)
    return len(max(re.findall(regex_2, tweet)))

directory = "data/Sentiment_Classifier"

for entry in tqdm(os.scandir(directory)):
    if not entry.path.endswith(".csv"):
        print(f"skipped {os.path.basename(entry.path)}")

    Sentiment_Tweets = pd.DataFrame(columns=['ID', 'COUNTRY', 'DAY', 'MONTH', 'TEXT_RAW', 'WORD COUNT','LEMMATIZED', 'POSITIVE', 'NEGATIVE', 'STRONGSUBJECTIVE', 'WEAKSUBJECTIVE', 'Sentiment anger',  'Sentiment anticipation' , 'Sentiment  disgust', 'Sentiment fear' , 'Sentiment joy', 'Sentiment sadness', 'Sentiment surprise' , 'Sentiment trust', 'Capital Letters' , 'Longest Sequence Capital Letters'])

    Preprocessed_Tweets = pd.read_csv(entry.path)

    Sentiment_Tweets['ID'] = Preprocessed_Tweets['ID']
    Sentiment_Tweets['COUNTRY'] = Preprocessed_Tweets['COUNTRY']
    Sentiment_Tweets['DAY'] = Preprocessed_Tweets['DAY']
    Sentiment_Tweets['MONTH'] = Preprocessed_Tweets['MONTH']
    Sentiment_Tweets['TEXT_RAW'] = Preprocessed_Tweets['TEXT_RAW']
    Sentiment_Tweets['WORD COUNT'] = Preprocessed_Tweets['TEXT_RAW'].apply(length)
    Sentiment_Tweets['LEMMATIZED'] = Preprocessed_Tweets['TEXT_RAW'].apply(lemmatize)
    Sentiment_Tweets['POSITIVE'] = Preprocessed_Tweets['TEXT_RAW'].apply(positives)
    Sentiment_Tweets['NEGATIVE'] = Preprocessed_Tweets['TEXT_RAW'].apply(negatives)

    Sentiment_Tweets['STRONGSUBJECTIVE'] = Preprocessed_Tweets['TEXT_RAW'].apply(subjectivity_strong)
    Sentiment_Tweets['WEAKSUBJECTIVE'] = Preprocessed_Tweets['TEXT_RAW'].apply(subjectivity_weak)

    Sentiment_Tweets['Sentiment anger'] = Preprocessed_Tweets['TEXT_RAW'].apply(fine_sentiment_anger)
    Sentiment_Tweets['Sentiment anticipation'] = Preprocessed_Tweets['TEXT_RAW'].apply(fine_sentiment_anticipation)
    Sentiment_Tweets['Sentiment  disgust'] = Preprocessed_Tweets['TEXT_RAW'].apply(fine_sentiment_disgust)
    Sentiment_Tweets['Sentiment fear'] = Preprocessed_Tweets['TEXT_RAW'].apply(fine_sentiment_fear)
    Sentiment_Tweets['Sentiment joy'] = Preprocessed_Tweets['TEXT_RAW'].apply(fine_sentiment_joy)
    Sentiment_Tweets['Sentiment sadness'] = Preprocessed_Tweets['TEXT_RAW'].apply(fine_sentiment_sadness)
    Sentiment_Tweets['Sentiment surprise'] = Preprocessed_Tweets['TEXT_RAW'].apply(fine_sentiment_surprise)
    Sentiment_Tweets['Sentiment trust'] = Preprocessed_Tweets['TEXT_RAW'].apply(fine_sentiment_trust)

    Sentiment_Tweets['Capital Letters'] = Preprocessed_Tweets['TEXT_RAW'].apply(capital_letters)
    Sentiment_Tweets['Longest Sequence Capital Letters'] = Preprocessed_Tweets['TEXT_RAW'].apply(capital_letters_longest_sequence)

    Sentiment_Tweets.to_csv("data/Sentiment_Tweets/" + os.path.basename(entry.path), index=False, header=True)
