
import csv
import re


def posneg_classifier(tweet):
    """ compares the words in the tweet to the NRC Emotion lexicon, counts positive and
    negative words and calculates the percentage"""
    tweet_open = open(tweet, "r") #### bzw. preprocessed tweet, am besten lemmatized
    tweet_words = tweet_open.read().split()
    positive = 0
    negative = 0
    with open("data/Sentiment_Classifier/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt") as lex:
        lex_reader = csv.reader(lex, delimiter = '\t')
        for entry in lex_reader:
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "positive" and entry[2] == "1":
                positive += 1
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "negative" and entry[2] == "1":
                negative += 1
        print("positive: " + str(100/(positive+negative) * positive) + " % and negative: " + str(100/(positive+negative) * negative) + " %")

def subjectivity(tweet):
    """counts the strong subjective and weak subjective words based on  the
    MPQA lexicon. Returns the percentage of strong subjective, weak subjective
    and neutral words. If a sequence of minimum 9 characters (including whitespace)
    is found, the count of strong subjective words is doubled"""
    tweet_open = open(tweet, "r") #### bzw. preprocessed tweet, am besten lemmatized
    tweet_read = tweet_open.read()
    print(tweet_read)
    tweet_words = tweet_read.split()
    strong_subj = 0
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
            if entry[2] in tweet_words and entry[0] == "type=strongsubj":
                strong_subj += 1
            if entry[2] in tweet_words and entry[0] == "type=weaksubj":
                weak_subj += 1
    neutral = len(tweet) - strong_subj - weak_subj
    regex = "([A-Z\s]){9,200}"
    regex = re.compile(regex)
    if re.search(regex, tweet_read):
        strong_subj = strong_subj*2
    print("strongsubj: " + str(100/(strong_subj + weak_subj + neutral) * strong_subj))
    print("weaksubj: " + str(100/(strong_subj + weak_subj + neutral) * weak_subj))
    print("neutral: " + str(100/(strong_subj + weak_subj + neutral) * neutral))

def fine_sentiment(tweet):
    """ compares the words in the tweet to the NRC Emotion lexicon, counts the
    amount of words of every category and calculates the percentage"""
    tweet_open = open(tweet, "r") #### bzw. preprocessed tweet, am besten lemmatized
    tweet_words = tweet_open.read().split()
    anger = 0
    anticipation = 0
    disgust = 0
    fear = 0
    joy = 0
    sadness = 0
    surprise = 0
    trust = 0
    with open("data/Sentiment_Classifier/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt") as lex:
        lex_reader = csv.reader(lex, delimiter = '\t')
        for entry in lex_reader:
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "anger" and entry[2] == "1":
                anger += 1
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "anticipation" and entry[2] == "1":
                anticipation += 1
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "disgust" and entry[2] == "1":
                disgust += 1
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "fear" and entry[2] == "1":
                fear += 1
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "joy" and entry[2] == "1":
                joy += 1
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "sadness" and entry[2] == "1":
                sadness += 1
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "surprise" and entry[2] == "1":
                surprise += 1
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "trus" and entry[2] == "1":
                trust += 1
        print("anger: " + str(100/(anger + anticipation + disgust + fear + joy + sadness + surprise + trust) * anger))
        print("anticipation: " + str(100 / (anger + anticipation + disgust + fear + joy + sadness + surprise + trust) * anticipation))
        print("disgust: " + str(100 / (anger + anticipation + disgust + fear + joy + sadness + surprise + trust) * disgust))
        print("fear: " + str(100 / (anger + anticipation + disgust + fear + joy + sadness + surprise + trust) * fear))
        print("joy: " + str(100 / (anger + anticipation + disgust + fear + joy + sadness + surprise + trust) * joy))
        print("sadness: " + str(100 / (anger + anticipation + disgust + fear + joy + sadness + surprise + trust) * sadness))
        print("surprise: " + str(100 / (anger + anticipation + disgust + fear + joy + sadness + surprise + trust) * surprise))
        print("trust: " + str(100 / (anger + anticipation + disgust + fear + joy + sadness + surprise + trust) * trust))

#import os
#print (os.getcwd())

subjectivity("data/Sentiment_Classifier/tweet_test.txt")
print ("")
posneg_classifier("data/Sentiment_Classifier/tweet_test.txt")
print ("")
fine_sentiment("data/Sentiment_Classifier/tweet_test.txt")