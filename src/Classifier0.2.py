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
import regex
from string import punctuation

# os.chdir(os.path.dirname(__file__))  # changes path to current file path, to make sure it works for everyone

nltk.download('wordnet')
directory = "data/Preprocessed_Tweets/"

lemmatizer = WordNetLemmatizer()


#################################################
# This method gets as input a string  outputs a list of all emojis in the string
def findEmojis(data):
    global emoji_subs_fails

    try:
        removeWords = re.compile('[a-zA-Z]')
        emoji = re.compile("["
                           u"\U0001F600-\U0001F64F"
                           u"\U0001F300-\U0001F5FF"
                           u"\U0001F680-\U0001F6FF"
                           u"\U0001F1E0-\U0001F1FF"
                           u"\U00002500-\U00002BEF"
                           u"\U00002702-\U000027B0"
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           u"\U0001f926-\U0001f937"
                           u"\U00010000-\U0010ffff"
                           u"\u2640-\u2642"
                           u"\u2600-\u2B55"
                           u"\u200d"
                           u"\u23cf"
                           u"\u23e9"
                           u"\u231a"
                           u"\ufe0f"
                           u"\u3030"
                           "]+", re.UNICODE)

        temp = str(re.sub(removeWords, '', data))
        temp = [char for char in temp]
        return emoji.findall(str(temp))
    except Exception as e:
        print(e)
        emoji_subs_fails += 1

        return data


# This method gets as input a string  outputs a list of all hashtags in the string
def findHashtags(data):
    HASHS = []
    for word in str(data).split():
        if word.startswith('#'):
            HASHS.append(word)
    return HASHS


# This method gets as input a list of emojis outputs a binary vector that "says" if a smiley is in the string
def convertEmojisToVector(data):
    # This are the most frequent smileys 
    SMILEYS = ['👐', '🍆', '🔬', '𝗼', '🥡', '🌪', '💌', '💆', '🏍', '🧢', '💴', '𝐄', '😯', '🏎', '⛪', '😟', '🏙', '⚔',
               '🦦', '🍏', '😖', '𝘁', '𝙞', '𝙤', '⛽', '🥦', '🥓', '🚩', '🏘', '⚫', '⛈', '🦞',
               '👎', '🐔', '𝐃', '🛒', '🧨', '𝐮', '🎇', 'Ⓦ', '💳', '⬆', '🐀', '🐒', '●', '🚘', '𝙖', '𝗻', '🔵', '🥒',
               '🌽', '☯', '🔙', '🌃', '💼', '🇽', '𝐓', '🕯', '🤚', 'Ⓞ', '✏', '🍀', '👅', '🏰', '𝕤',
               '🐏', '𝙚', '🥕', '𝗮', '𝗶', '🥬', '🎡', '📽', '💘', '😹', '🦸', '𝐥', 'Ⓡ', '𝕚', '𝕥', '⛄', '♻', '🍉',
               '😰', '🍝', '🇭', '🥋', '😠', '🧿', '𝐧', '𝐀', '👕', '🌵', '🛏', '🤵', '🕶', '🐅', '♠',
               '🥘', '🐍', '🎢', '☁', '🐠', '🐘', '𝕠', '✝', '🧜', '➖', '🧸', '🤛', '🏚', '🗳', '𝗲', '🧚', '🏳', '🌭',
               '🍞', '🛹', '🦊', '🙀', '🦢', '🦾', '😪', '🐈', '🩺', '😣', '𝕖', '🥤', '🥩',
               '🦓', '♡', '🐐', '⛔', '🌷', '🏄', '🌶', '𝕒', '🎀', '🐥', '🧪', '𝐬', '☆', '𝐫', '🦌', '🏔', '🐰', '💵',
               '🌡', '🤲', '🧠', '🎆', '🖥', '☘', '🙊', '🥑', '🚙', '🐣', '🦅', '🇯', '🤴', '🌤',
               '🍬', '🖐', '📦', '🎞', '🌾', '💣', '🍗', '⛱', '🐄', '🗓', '🏫', '👰', '🥇', '☃', '🔴', '🔹', '🍌', '👙',
               '🏁', '👦', '🐼', '⛰', '⛵', '🔫', '🔑', '🤜', '🍊', '🦆', '▶', '🎾', '👣',
               '☮', '￼', '🧁', '🌬', '🐯', '🌏', '💸', '🥁', '😓', '🦄', '🍅', '𝐚', '𝐭', '🧀', '🩸', '🐆', '🤒', '🥗',
               '⬅', '🍪', '💍', '🍩', '🐟', '🍭', '💧', '🐴', '𝐨', '🍫', '𝐢', '🦍', '🌙', '😕',
               '🐺', '🦇', '🧻', '🐱', '👯', '🧟', '😮', '🐿', '𝐞', '🍟', '▫', '😲', '🇵', '😑', '☎', '🤠', '🚗', '🏌',
               '🇪', '🤨', '👱', '🧑', '💝', '⚾', '⚪', '🧔', '📱', '🧤', '🍴', '🦁', '🍿', '📢',
               '☑', '🌄', '💄', '💭', '😛', '🍓', '💊', '🤮', '☔', '🇦', '🎹', '🐦', '🚶', '🤎', '🍦', '🤑', '😐', '🤝',
               '👧', '📞', '😴', '🤫', '🤢', '📈', '❓', '📖', 'ー', '📣', '📌', '🤡', '🕊',
               '😥', '🤸', '🌧', '👁', '✍', '🛑', '🌛', '🇹', '🚲', '🇨', '💤', '🔐', '⬇', '⛳', '😞', '💩', '🛍', '☹',
               '🏀', '🎙', '🎭', '🐻', '📀', '🏞', '🍰', '🍄', '🌲', '🏥', '🙅', '🇷', '🌼', '🤭',
               '👶', '🔒', '🏈', '🥶', '🎯', '💓', '🍋', '⚕', '📺', '🌀', '🗽', '🎸', '🚫', '👸', '🍎', '💡', '💅',
               '😌', '🏊', '🍑', '🥃', '🥊', '🐝', '🧐', '🏆', '👆', '🧼', '🚀', '🚴', '☠', '🏴',
               '🤟', '👈', '❌', '🌮', '😡', '📲', '🔊', '😤', '🎼', '🍕', '🏝', '🐕', '💐', '🦋', '🤤', '🍔', '🕉',
               '🍳', '🇲', '🍽', '👽', '💎', '😻', '🌹', '🍂', '♐', '🕺', '🦃', '😒', '🎧', '▪',
               '🍃', '🎨', '🌻', '☢', '🏠', '💰', '🤬', '👟', '🎓', '😫', '🎵', '📝', '🍸', '💔', '📍', '🥴', '📆',
               '😝', '🥵', '😄', '💞', '😇', '💇', '✔', '⚜', '📚', '🎬', '🎊', '🤧', '🍹', '⚽',
               '✈', '🎅', '🙂', '🌺', '💈', '🤓', '🐾', '🎈', '🌿', '😏', '😔', '🤯', '💁', '🎤', '🙋', '➡', '🏖', '💦',
               '💨', '🍁', '🏋', '☣', '❣', '🌱', '❗', '☺', '💉', '😱', '⚡', '🙈', '❄', '👻',
               '🤞', '🙃', '🔮', '🌍', '🤙', '😈', '🗣', '💻', '🧘', '🎁', '👋', '⚠', '👇', '🌸', '🍾', '🧡', '🌳',
               '🌟', '👑', '🌎', '💋', '🌴', '💗', '😬', '💃', '🥺', '📷', '🖕', '🤘', '😢', '💫', '☕',
               '🤍', '🐶', '🎂', '👨', '✂', '👊', '🌊', '💖', '😩', '🎥', '🇮', '🍷', '🌆', '🇳', '🏃', '🥂', '💀',
               '🤗', '😀', '😳', '🙄', '👩', '😆', '👉', '😜', '🍻', '🎃', '👌', '🇧', '💛', '🏡', '🍺',
               '🇬', '💥', '🥳', '⭐', '🌞', '😭', '👏', '✊', '😅', '💚', '🎶', '♥', '✅', '🤩', '😋', '🎄', '🌈', '⠀',
               '💜', '🤪', '👀', '✌', '🖤', '🌅', '😘', '😉', '🤔', '🚨', '🏿', '💾', 'Ⓨ', '🎉',
               '😁', '☝', 'Ⓣ', 'Ⓢ', '😃', '😊', '🤦', '💙', '・', '👍', '💕', '☀', '🤷', '💯', '📸', '🥰', '🙌', '😎',
               '🇸', '✨', '🇺', '😍', '💪', '🦠', '🤣', '🔥', '♂', '♀', '🏼', '🏾', '🏽', '🏻', '🙏',
               '😂', '😷', '❤']

    vector = [0 for i in range(0, len(SMILEYS))]
    for i in range(0, len(SMILEYS)):
        if SMILEYS[i] in data:
            vector[i] = 1

    return vector


# This method gets as input a list of hashtags outputs a binary vector that "says" if a smiley is in the string
def convertHashtagsToVector(data):
    # This are the most frequent smileys 
    HASHLIST = ['#corona', '#alone', '#apocalypse', '#covid', '#Corona', '#IndiaFightsCorona', '#coronavid19',
                '#corona…', '#quarantine', '#quarantinelife', '#virus', '#rona',
                '#socialdistancing', '#stayhome', '#staysafe…', '#covid_19', '#staysafe', '#support', '#success',
                '#COVID19', '#coronadiaries', '#lockdown', '#home', '#isolation',
                '#safetyfirst', '#stayhomestaysafe', '#StayAtHome', '#CovidIndia', '#coronamemes', '#stayathome',
                '#lockdown…', '#covid19', '#savelives', '#God', '#love', '#happy',
                '#stayhealthy', '#coronavirus', '#throwback', '#newnormal', '#covi̇d19', '#emptystreets', '#emptynyc',
                '#nycshutdown', '#stayhome…', '#coronavirusitalianews', '#lockdown2020',
                '#workfromhome', '#selflove', '#selfisolation', '#socialdistancing…', '#doctor', '#live', '#quarentine',
                '#staypositive', '#sunshine', '#21dayslockdown', '#covid19india',
                '#covidart', '#coronaindia', '#bored', '#truth', '#CORONA', '#people', '#coronatime', '#familytime',
                '#family', '#handsanitizer', '#positivevibes', '#StaySafe', '#thankful',
                '#pandemic', '#online', '#friendship', '#friends', '#Covid-19', '#mask', '#washyourhands',
                '#CoronaVirus', '#Virus', '#Covid19', '#covıd19', '#protection', '#coronavirus…',
                '#saferathome', '#relax', '#cuarentena', '#Covid', '#toiletpaper', '#maskon', '#COVID19…', '#empty',
                '#selfquarantine', '#covid-19', '#safety', '#safe', '#thoughts', '#reflection',
                '#covid19…', '#facemask', '#essential', '#freedom', '#StayHomeStaySafe', '#news', '#covid2020',
                '#gocorona', '#quarantineandchill', '#nurse', '#walkwhileyoucan', '#shopping',
                '#StayHome', '#peace', '#covid_19…', '#fight', '#quarantine…', '#humanity', '#motivation',
                '#coronavírus', '#washingtondc', '#masks', '#strength', '#party', '#Health', '#outside',
                '#Coronavirus', '#maskup', '#happiness', '#hope', '#besafe', '#flattenthecurve', '#sanitizer',
                '#stopthespread', '#care', '#staystrong', '#smile', '#zoom', '#stayinghome',
                '#alonetogether', '#Covid_19', '#Quarantine', '#supportsmallbusiness', '#shopsmall', '#coronawarriors',
                '#homesweethome', '#staycation', '#help', '#CoronaVirusUk', '#CoronaUk',
                '#essentialworkers', '#lockdownlife', '#inspiration', '#doctors', '#pandemic2020', '#stayhomesavelives',
                '#update', '#healthcareworkers', '#frontlineworkers', '#socialdistance',
                '#positivity', '#thankyou', '#PublicHealth', '#politics', '#firstresponders', '#pandemic.',
                '#SocialDistancing', '#COVID_19', '#weareinthistogether', '#coronaviruspandemic',
                '#shutdown', '#healthy', '#free', '#sanitize', '#blessed', '#open', '#anxiety', '#indiafightscorona',
                '#education', '#depression', '#health', '#workingfromhome', '#pandemic…',
                '#lifeinthetimeofcorona', '#coronavirusmemes😂😂😂', '#Pandemic', '#protectyourself', '#memories',
                '#inthistogether', '#pandemiclife', '#bekind', '#laugh', '#faith',
                '#mentalhealth', '#COVID19.', '#vaccine', '#backtowork', '#leadership', '#covid…', '#chill#COVID-19',
                '#facemasks', '#COVID', '#masks4all', '#nurses', '#TogetherAtHome',
                '#Lockdown2020', '#coronavirus.', '#socialdistancing2020', '#wearyourmask', '#Coronavirus!',
                '#SaveTheWorld:thanksdoc:', '#SaveTheWorld', '#Covid-19!', '#SaveTheWorld❤',
                '#wewillsurvive', '#thenewnormal', '#getoutside', '#Mask', '#Coronaupdate', '#relief', '#supportlocal',
                '#dailywalk', '#QuarantineLife', '#loveoneanother', '#lovelife',
                '#homeschooling', '#homeschool', '#homeworkout', '#team', '#grateful', '#healthcare', '#wearamask',
                '#covid19.', '#doingmypart', '#COVID19,', '#staysafeeveryone',
                '#coronaupdate', '#crisis', '#Truth', '#localbusiness', '#keepgoing', '#wakeup', '#ShopLocal',
                '#smallbusiness', '#TrumpVirus', '#together', '#facecovering', '#reopening',
                '#children', '#faceshield', '#HelpUsToHelpYou', '#TogetherForIndia', '#WorkFromHome',
                '#supportlocalbusiness', '#wearamask😷', '#LOCKDOWN2020', '#justice', '#worker',
                '#WearAMask', '#MaskUp', '#stayingsafe', '#BeatThePandemic', '#Masks4All#covidvacccine']

    vector = [0 for i in range(0, len(HASHLIST))]
    for i in range(0, len(HASHLIST)):
        if HASHLIST[i] in data:
            vector[i] = 1
    return vector


# This method gets as input a string and outputs a list of counts for each special chair
def findSpecialChairs(data):
    specialChairs = list(set(punctuation))
    vector = [0 for _ in range(0, len(specialChairs))]
    for i in range(0, len(specialChairs)):
        vector[i] = data.count(specialChairs[i])

    return vector


###################################################
def lemmatize(tweet):
    """returns lemmatized tweet of raw text"""
    text_tweet = str(tweet)
    words = text_tweet.split()
    lemmatized = [None] * len(words)
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
    emolex_df = pd.read_csv(filepath, names=["word", "emotion", "association"],
                            skiprows=45, sep='\t', keep_default_na=False)
    # subjlex = pd.read_csv("data/Sentiment_Classifier/subjclueslen1-HLTEMNLP05.tff",
    #                names=["type", "len", "word1","pos1","stemmed1","priorpolarity"],
    #                skiprows=0, sep=',', keep_default_na=False)

    j = 0
    for word in tweet_words:
        word = word.lower()
        try:
            # get the index of the word in lexikon
            idx = emolex_df.loc[emolex_df['word'] == word].index[0]
            for i in range(10):
                emotions[j].append(emolex_df["association"][idx + i])
        except:
            # print("Word *"+ word + "* is not in the lexikon")
            for i in range(10):
                emotions[j].append(0)

        finally:
            j = j + 1
    return emotions


def create_df_with_emotions(Preprocessed_Tweets):
    Sentiment_Tweets = pd.DataFrame(columns=['ID', 'COUNTRY', 'DAY',
                                             'MONTH', 'TEXT_RAW', 'WORD COUNT',
                                             'LEMMATIZED', 'STRONGSUBJECTIVE', 'WEAKSUBJECTIVE',
                                             'Sentiment anger', 'Sentiment anticipation', 'Sentiment  disgust',
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
        # Sentiment_Tweets.at[index,'STRONGSUBJECTIVE'] = np.sum(emotions[:,10])
        # Sentiment_Tweets.at[index,'WEAKSUBJECTIVE'] = np.sum(emotions[:,11])
        Sentiment_Tweets.at[index, 'LEMMATIZED'] = tweet_words
        Sentiment_Tweets.at[index, 'WORD COUNT'] = len(Sentiment_Tweets.loc[index, 'LEMMATIZED'])
        Sentiment_Tweets.at[index, 'Sentiment anger'] = emotions[:, 0]
        Sentiment_Tweets.at[index, 'Sentiment anticipation'] = emotions[:, 1]
        Sentiment_Tweets.at[index, 'Sentiment  disgust'] = emotions[:, 2]
        Sentiment_Tweets.at[index, 'Sentiment fear'] = emotions[:, 3]
        Sentiment_Tweets.at[index, 'Sentiment joy'] = emotions[:, 4]
        Sentiment_Tweets.at[index, 'NEGATIVE'] = emotions[:, 5]
        Sentiment_Tweets.at[index, 'POSITIVE'] = emotions[:, 6]
        try:
            Sentiment_Tweets.at[index, 'Sentiment sadness'] = emotions[:, 7]
        except:
            print("emotions error the emotions list are", emotions, "Tweet ID is", Sentiment_Tweets.at[index, 'ID'])
        Sentiment_Tweets.at[index, 'Sentiment surprise'] = emotions[:, 8]
        Sentiment_Tweets.at[index, 'Sentiment trust'] = emotions[:, 9]

        try:
            Sentiment_Tweets.at[index, 'Capital Letters'] = sum(1 for c in row['TEXT_RAW'] if c.isupper())
        except:
            Sentiment_Tweets.at[index, 'Capital Letters'] = 0

        try:
            Sentiment_Tweets.at[index, 'Longest Sequence Capital Letters'] = max(re.findall('[A-Z]+', row['TEXT_RAW']),
                                                                                 key=len)
        except:
            Sentiment_Tweets.at[index, 'Longest Sequence Capital Letters'] = 0

        try:
            # Find all emojis
            Sentiment_Tweets["rawEmojis"] = Preprocessed_Tweets["TEXT_RAW_PUNCTUATION"].apply(findEmojis)
        except:
            continue

        try:
            # Convert emojis to binary vectors
            Sentiment_Tweets["rawEmojis"] = Sentiment_Tweets["rawEmojis"].apply(convertEmojisToVector)
        except:
            continue

        try:
            # Create special chair counts
            Sentiment_Tweets["specialChairs"] = Preprocessed_Tweets["TEXT_RAW_PUNCTUATION"].apply(findSpecialChairs)

        except:
            continue

        ######
        try:
            # Find all hashtags
            Sentiment_Tweets["rawHashtags"] = Preprocessed_Tweets["TEXT_RAW_PUNCTUATION"].apply(findHashtags)
        except:
            continue

        try:
            # Convert emojis to binary vectors
            Sentiment_Tweets["rawHashtags"] = Sentiment_Tweets["rawHashtags"].apply(convertHashtagsToVector)
        except:
            continue

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
