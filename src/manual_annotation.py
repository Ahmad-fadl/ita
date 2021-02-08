#!/usr/bin/env python
# coding: utf-8

import os
import pickle
import random
from pprint import pprint

import numpy as np
import pandas as pd

motivationals = ["All tweets can come true, if we have the courage to rate them.",
                 "The secret of getting ahead is getting started.",
                 "The best time to rate a tweet was 20 years ago. The second best time is now!",
                 "If people are doubting how many tweets you can judge, go so far that they can't judge you anymore.",
                 "Rate one tweet every day that scares you.",
                 "Choose the sentiment that you feel in your heart to be right – for you’ll be criticized anyway.",
                 "Smart people learn from everything and everyone, average people from their experiences, "
                 "stupid people already have all the answers.",
                 "You can either experience the pain of discipline or the pain of regret. The choice is yours.",
                 "If something is important enough, even if the odds are stacked against you, you should still do it.",
                 "If you hear a voice within you say ‘you cannot rate,’ "
                 "then by all means rate and that voice will be silenced."]


def generate_annot_dict(annot_dict_path):
    if os.path.exists(annot_dict_path):
        print("You may be not supposed to run this again. "
              "Delete annot_dict file first if you really want to regenerate and overwrite the dict.")
        return 0
    else:
        doc_names = []
        for entry in os.scandir("data/Hydrated_Tweets"):
            if entry.path.endswith(".csv"):
                doc_names.append(f"{os.path.basename(entry.path)}")

        annot_basis = random.choices(doc_names, k=20)  # change back to 100 or anything else. 20 is for short testing

        annot_dict = {}
        for entry in annot_basis:
            tweet = pd.read_csv(f"data/Hydrated_Tweets/{entry}")[["ID", "TEXT_RAW"]].sample(1)
            ID = int(tweet["ID"].values[0])
            # print(str(text.values))
            # print(str(ID.values))
            # text = tweet["TEXT_RAW"]
            annot_dict[ID] = {'path': entry, 'ahmad': None, 'severin': None, 'sina': None, 'ute': None}

        print(annot_dict)

        with open(annot_dict_path, 'wb') as f:  # generate and save annot dict as a pickle
            pickle.dump(annot_dict, f)

        with open(annot_dict_path, 'wb') as f:
            pickle.dump(annot_dict, f)


def annotate_basis_tweets(annot_dict_path):
    with open(annot_dict_path, 'rb') as f:
        annot_dict = pickle.load(f)
    #pprint(annot_dict)
    annotator = None
    while annotator not in ['ahmad', 'severin', 'sina', 'ute']:
        annotator = input("Welcome to the manual sentiment annotation.\n"
                          "What's your name? Choose from 'ahmad', 'severin', 'sina' and 'ute':\n")
    print(f"Hello {annotator}! Please rate the sentiment of the following tweets regarding the Corona situation.\n"
          f"Negative (-1), neutral (0) or positive (1). If unsure or not applicable choose (0) too.\n"
          f"You can cancel and continue anytime.\n")
    count = 0
    for i in annot_dict:
        if annot_dict[i][annotator] is not None:
            count += 1
    print(f"You have annotated {count} tweets so far.\n")

    for tweet_id in annot_dict:
        if annot_dict[tweet_id][annotator] is None:
            ID = np.int64(tweet_id)
            tweets = pd.read_csv(f"data/Hydrated_Tweets/{annot_dict[tweet_id]['path']}")[["ID", "TEXT_RAW"]]
            tweet = tweets[tweets['ID'].values == ID]
            print("------------------------------------------------")
            print(tweet["TEXT_RAW"].values[0])
            print("------------------------------------------------")
            sentiment = None
            while sentiment not in ["-1", "0", "1"]:
                sentiment = input("rate it: ")
            sentiment = int(sentiment)
            annot_dict[tweet_id][annotator] = sentiment
            with open(annot_dict_path, 'wb') as g:
                pickle.dump(annot_dict, g)
            count += 1
            if count % 20 == 0:
                print(
                    f"You have annotated {count} tweets. I feel you should hear this:\n{random.choice(motivationals)}")
            elif count % 10 == 0:
                print(f"You have annotated {count} tweets so far. YOU GO {annotator.upper()}!")
    print(f"You have annotated {count} tweets. Thanks. ")
    # TODO implement evaluation for more tweets but for single persons


annot_dict_path = "data/Manual_Annotation/annot_ID_dict.pkl"

generate_annot_dict(annot_dict_path=annot_dict_path)  # already run and output uploaded by sina. don't overwrite
annotate_basis_tweets(annot_dict_path=annot_dict_path)

# TODO implement kappa / annotator agreement
