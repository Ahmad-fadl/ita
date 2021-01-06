
import csv
import re


def posneg_classifier(tweet):
    """ compares the words in the <tweet> to the NRC Emotion lexicon, counts positive and
    negative words and calculates the percentage. returns positive sentiment percentage"""
    tweet_open = open(tweet, "r") #### bzw. preprocessed tweet, am besten lemmatized
    tweet_words = tweet_open.read().split()
    print (tweet_words, "\n")
    positive = 0
    negative = 0
    with open("data/Sentiment_Classifier/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt") as lex:
        lex_reader = csv.reader(lex, delimiter = '\t')
        for entry in lex_reader:
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "positive" and entry[2] == "1":
                positive += 1
            if len(entry) == 3 and entry[0] in tweet_words and entry[1] == "negative" and entry[2] == "1":
                negative += 1
        print(f"positive: {str(100 / (positive + negative) * positive)}% and negative: {str(100 / (positive + negative) * negative)}%")
        return 100 / (positive + negative) * positive


def subjectivity(tweet):
    """counts the strong subjective and weak subjective words based on the
    MPQA lexicon. Prints the percentage of strong subjective, weak subjective
    and neutral words. If a sequence of minimum 9 characters (including whitespace)
    is found, the count of strong subjective words is doubled"""
    tweet_open = open(tweet, "r") #### bzw. preprocessed tweet, am besten lemmatized
    tweet_read = tweet_open.read()
    #print(tweet_read, "\n")
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
        print (re.search(regex, tweet_read))
        strong_subj = strong_subj*2
    print("strongsubj: " + str(100/(strong_subj + weak_subj + neutral) * strong_subj))
    print("weaksubj: " + str(100/(strong_subj + weak_subj + neutral) * weak_subj))
    print("neutral: " + str(100/(strong_subj + weak_subj + neutral) * neutral))

def fine_sentiment(tweet):
    """ compares the words in the <tweet> to the NRC Emotion lexicon, counts the
    amount of words of every sentiment category and calculates the percentage"""
    tweet_open = open(tweet, "r") #### bzw. preprocessed tweet, am besten lemmatized
    tweet_words = tweet_open.read().split()
    sentiments = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
    sentiment_dict = {key: 0 for key in sentiments}
    with open("data/Sentiment_Classifier/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt") as lex:
        lex_reader = csv.reader(lex, delimiter = '\t')
        for entry in lex_reader:
            if len(entry) == 3 and entry[0] in tweet_words and entry[2] == "1" and entry[1] in sentiments:
                sentiment_dict[entry[1]] += 1

    print(sentiment_dict)
    total = sum(value for k, value in sentiment_dict.items())
    for k, v in sentiment_dict.items():
        print(f"{k}: {v*100/total}%")


#import os
#print (os.getcwd())

posneg_classifier("data/Sentiment_Classifier/tweet_test.txt")
print ("")
subjectivity("data/Sentiment_Classifier/tweet_test.txt")
print ("")
fine_sentiment("data/Sentiment_Classifier/tweet_test.txt")