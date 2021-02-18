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
                 "You can either experience the pain of sentiments or the pain of regret. The choice is yours.",
                 "If something is important enough, even if the odds are stacked against you, you should still do it.",
                 "If you hear a voice within you say ‘you cannot rate,’ "
                 "then by all means rate and that voice will be silenced."]


def generate_kappa_anno_dict(annot_dict_path,sample=20):
    """param sample: how many tweets should be in dict"""
    if os.path.exists(annot_dict_path):
        print("You may be not supposed to run this again. "
              "Delete annot_dict file first if you really want to regenerate and overwrite the dict.")
        return 0
    else:
        doc_names = []
        for entry in os.scandir("data/Hydrated_Tweets"):
            if entry.path.endswith(".csv"):
                doc_names.append(f"{os.path.basename(entry.path)}")

        annot_basis = random.choices(doc_names, k=sample)

        annot_dict = {}
        for entry in annot_basis:
            tweet = pd.read_csv(f"data/Hydrated_Tweets/{entry}")[["ID", "TEXT_RAW"]].sample(1)
            ID = int(tweet["ID"].values[0])
            # print(str(text.values))
            # print(str(ID.values))
            # text = tweet["TEXT_RAW"]
            annot_dict[ID] = {'path': entry, 'ahmad': None, 'severin': None, 'sina': None, 'ute': None}

        # print(annot_dict)

        with open(annot_dict_path, 'wb') as f:  # generate and save annot dict as a pickle
            pickle.dump(annot_dict, f)


def annotate_basis_tweets(annot_dict_path, kappa_test=True):
    annotator = None
    while annotator not in ['ahmad', 'severin', 'sina', 'ute']:
        annotator = input("Welcome to the manual sentiment annotation.\n"
                          "What's your name? Choose from 'ahmad', 'severin', 'sina' and 'ute':\n")

    if kappa_test:
        with open(annot_dict_path+".pkl", 'rb') as f:
            annot_dict = pickle.load(f)
    elif not kappa_test:
        with open(str(annot_dict_path + "_" + annotator + ".pkl"), 'rb') as f:
            annot_dict = pickle.load(f)

    print(f"Hello {annotator}! Please rate the sentiment of the following tweets.\n"
          f"Negative (-1), neutral (0) or positive (1). \n"
          f"- If you can't tell or if not applicable choose (0) too.\n"
          f"- Rate it regarding the Corona situation. (example: 'I hate my sister!' would be (0))\n"
          f"- If you see something positive, but are not sure if it's really THAT much positive or even actually positive, choose (1)\n"
          f"- Rate the sentiment that is (somehow) transported by the tweeter- do not rate the positivity of the provided facts. "
          f"(example: neutral conveyed news about rise in deaths)\n"
          f"- Don't click on links or google for unknown concepts. Tweet itself = full information (Exception: unknown vocabulary)\n"
          f"- Hashtags and Emojis are part of the tweet and its sentiment.\n"
          f"You can cancel and continue anytime.\n")

    count = 0
    for i in annot_dict:
        if annotator in annot_dict[i] and annot_dict[i][annotator] is not None:
            count += 1

    print(f"You have annotated {count} tweets so far.\n")

    for tweet_id in annot_dict:
        if annotator in annot_dict[tweet_id] and annot_dict[tweet_id][annotator] is None:
            ID = np.int64(tweet_id)
            tweets = pd.read_csv(f"data/Hydrated_Tweets/{annot_dict[tweet_id]['path']}")[["ID", "TEXT_RAW"]]
            tweet = tweets[tweets['ID'].values == ID]
            raw_tweet = tweet["TEXT_RAW"].values[0]
            print(f"{len(raw_tweet) * '-'}")
            print(raw_tweet)
            print(f"{len(raw_tweet) * '-'}")
            sentiment = None
            while sentiment not in ["-1", "0", "1"]:
                sentiment = input("rate it: ")
            sentiment = int(sentiment)
            annot_dict[tweet_id][annotator] = sentiment
            if kappa_test:
                with open((annot_dict_path+".pkl"), 'wb') as g:
                    pickle.dump(annot_dict, g)
            elif not kappa_test:
                with open((annot_dict_path + "_" + annotator + ".pkl"), 'wb') as g:
                    pickle.dump(annot_dict, g)
            count += 1

            if count % 20 == 0:
                print(
                    f"You have annotated {count} tweets. I feel you should hear this:\n{random.choice(motivationals)}")
            elif count % 10 == 0:
                print(f"You have annotated {count} tweets so far. YOU GO {annotator.upper()}!")
    print(f"You have annotated {count} tweets. Thanks. ")


def gen_great_annot_dict(annot_dict_path, sample=1000):
    "param sample: how many tweets should be in the dict"
    if os.path.exists(annot_dict_path + "_sina.pkl"):
        print("You may be not supposed to run this again. "
              "Delete annot_dict file first if you really want to regenerate and overwrite the dict.")
        return 0
    else:
        doc_names = []
        for entry in os.scandir("data/Hydrated_Tweets"):
            if entry.path.endswith(".csv"):
                doc_names.append(f"{os.path.basename(entry.path)}")

        annot_basis = random.choices(doc_names, k=1000)  # change back to 100 or anything else. 20 is for short testing
        annot_dict = {}
        annot_dict_splits = [annot_basis[i:i + 250] for i in range(0, len(annot_basis), 250)]
        team = ['ahmad', 'severin', 'sina', 'ute']

        for split, annotator in zip(annot_dict_splits, team):
            for entry in split:
                tweet = pd.read_csv(f"data/Hydrated_Tweets/{entry}")[["ID", "TEXT_RAW"]].sample(1)
                ID = int(tweet["ID"].values[0])
                while ID in annot_dict:
                    tweet = pd.read_csv(f"data/Hydrated_Tweets/{entry}")[["ID", "TEXT_RAW"]].sample(1)
                    ID = int(tweet["ID"].values[0])
                annot_dict[ID] = {'path': entry, annotator: None}

            with open(annot_dict_path + "_" + annotator + ".pkl",
                      'wb') as f:  # generate and save annot dict as a pickle
                pickle.dump(annot_dict, f)
                # pprint(annot_dict)
                # pprint(len(annot_dict))


def merge_single_anno_dicts():
    merged_dict = {}
    for member in ['ahmad', 'ute', 'severin', 'sina']:
        with open("data/Manual_Annotation/annot_ID_dict_" + member + ".pkl", 'rb') as f:
            member_dict = pickle.load(f)
        merged_dict.update(member_dict)

    with open("data/Manual_Annotation/merged_annotation_dict.pkl",
              'wb') as f:  # generate and save annot dict as a pickle
        pickle.dump(merged_dict, f)
    # pprint(merged_dict)
    print("Annotation dicts are merged now. Please add/push to Git, if you are the last finishing annotator.")


def gen_annot_mean_dict(anno_dict):
    mean_dict = {}
    annotation = pd.read_pickle(anno_dict)
    for id in annotation:
        sumup = 0
        for member in ['ahmad', 'ute', 'severin', 'sina']:
            sumup += annotation[id][member]
        mean = round(sumup/len(member))
        mean_dict[id] = {}
        mean_dict[id]['mean'] = mean
        mean_dict[id]['path'] = annotation[id]['path']
    return mean_dict


if __name__ == '__main__':
    # for 2. kappa test with 20 samples
    # annot_dict_path = "data/Manual_Annotation/annot_ID_dict_2nd_kappa_test_20"
    # generate_kappa_anno_dict(annot_dict_path=annot_dict_path, sample=20)  # already run and output uploaded by sina. don't overwrite
    # annotate_basis_tweets(annot_dict_path=annot_dict_path, kappa_test=True)

    # for 3. kappa test
    # annot_dict_path = "data/Manual_Annotation/annot_ID_dict_3._kappa_test_50"
    # generate_kappa_anno_dict(annot_dict_path=annot_dict_path, sample=50)  # already run and output uploaded by sina. don't overwrite
    # annotate_basis_tweets(annot_dict_path=annot_dict_path, kappa_test=True)

    # for single annotation of 250 tweets per team member, 1000 in total
    long_annot_dict_path = "data/Manual_Annotation/annot_ID_dict"
    # gen_great_annot_dict(long_annot_dict_path, sample=1000) # already run and output uploaded by sina. don't overwrite
    annotate_basis_tweets(long_annot_dict_path, kappa_test=False)
    merge_single_anno_dicts()  # merge dicts of each team member. irrelevant if complete or not.

    # calc mean of 2. kappa test and add generated mean_dict to the merged dict
    mean_dic = gen_annot_mean_dict("data/Manual_Annotation/annot_ID_dict_3._kappa_test_50.pkl")
    merged_dict = pd.read_pickle("data/Manual_Annotation/merged_annotation_dict.pkl")
    merged_dict.update(mean_dic)
    pd.to_pickle(merged_dict, "data/Manual_Annotation/merged_annotation_dict.pkl")

    # result
    print("This is the final annotation dict: ")
    pprint(merged_dict)
