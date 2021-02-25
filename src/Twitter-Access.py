#!/usr/bin/env python
# coding: utf-8

import time
from tqdm import tqdm
from twython import Twython
import twython.exceptions
import pandas as pd
import os
import json
from pprint import pprint

# requirements:
# install twyton package
# install geopy package

# !pip install twython
# !pip install geopy
# !pip install tqdm

# bash command to hydrate an example tweet
# curl -X GET -H "Authorization: Bearer <BEARER TOKEN>" "https://api.twitter.com/2/tweets/20"
# get your bearer token (and the keys) here -> https://developer.twitter.com/en/portal/dashboard


# Enter your keys/secrets as strings in the following fields
# credentials = {}
# credentials['CONSUMER_KEY'] = "xxx"  # key names not consistent ->  API KEY = CONSUMER_KEY
# credentials['CONSUMER_SECRET'] = "xxx" # API SECRET KEY = CONSUMER_SECRET
# credentials['ACCESS_TOKEN'] = "xxx"   # not needed for now?
# credentials['ACCESS_SECRET'] = "xxx" # not needed for now?
# credentials['BEARER_TOKEN'] = 'xxx' # seee celll above
# comment out these lines after you have saved them to twitter_credentials.json to ita_project/


# Load credentials from json file
with open("twitter_credentials.json", "r") as file:
    credentials = json.load(file)

# Instantiate an object
python_tweets = Twython(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'], credentials['ACCESS_TOKEN'],
                        credentials['ACCESS_SECRET'], credentials['BEARER_TOKEN'])


# show json for a specific ID using show_status()
# tweet= python_tweets.show_status(id="1245219745311404032")
# pprint(tweet)

# show country
# print(tweet["place"]["country"])

# show date
# print(tweet["created_at"].split()[1])
# print(tweet["created_at"].split()[2])

# request limit: 900 requests/15 mins.
# so if you make 1 request per second, everything will be fine. (15*60 secs = 900secs)
# Rolling window? -> No
# DONE dynamische Berechnung der time-limits um ensprechend anfragefrequenz automatisch regeln

log_into_file = True


def print_log(msg):
    """Use instead of print, to print and log.
    Set global variable 'log_into_file to False, is logging not wished."""
    global log_into_file
    tqdm.write(msg)  # similar to print, but better optics when using tqdm loading bar
    if log_into_file:
        with open("data/Hydrated_Tweets_Report_Long.txt", "a") as log:
            log.write(msg + "\n")


def calc_delay_to_not_run_into_rate_limit(delay=True, request_method='show') -> float:
    """
    Recommended if you make more than 900 requests per session.
    If that's not the case or the request rate is still slower than 1 request/seconds,
    shorter delay times then returned here could succeed and be quicker.
    Calculation based on the 'python_tweets.show_status(id)' and 'python_tweets.lookup_status(id)'-method.
    Last one ist for ID-batches of 100, first one for a single ID request.
    You should call this function every 50th request to work properly.
    Args:
        request_method: 'lookup' or 'show'
        delay: set to False if you don't want a delay
    Returns:
        seconds to sleep before next request
    """
    resource = python_tweets.get_application_rate_limit_status(resources='statuses')
    # if you get a permission denied error here, you have to change your "project settings" here (developer.twitter.com)
    # to "Read, Write, and Direct Messages" and regenerate all keys.

    if request_method == 'show':
        resource = resource["resources"]["statuses"]["/statuses/show/:id"]
        # eg.: {"limit": 900,"remaining": 900, "reset": 1403602426} -- for 1 ID request
    elif request_method == 'lookup':
        resource = resource["resources"]["statuses"]["/statuses/lookup"]
        # e.g: "{"limit": 900,"remaining": 900, "reset": 1403602426} -- for 100 ID requests at once (same limits)
    else:
        raise NotImplementedError

    print(f" remaining requests until reset (<15mins): {resource['remaining']}")

    if not delay:
        return 0

    if resource["remaining"] == 0:
        return resource["reset"] - time.time()

    # no delay until you have less than 100 requests left, which is the case when you send less than 1 request/second.
    if resource["remaining"] > 100:
        return 0

    return (resource["reset"] - time.time()) / resource["remaining"]


start = time.time()

directory = "data/GeoCOV19TweetsDataset"

if not os.path.exists("data/Hydrated_Tweets_Long"):
    os.mkdir("data/Hydrated_Tweets_Long")

count_files = 0

# error collecting
count_corrupted_files = 0
tweets_not_found = 0
count_metadata_fail = 0
count_other_errors = 0

print_log("--------\n" + time.strftime("%d.%m.%y, %H:%M") + " --- Start hydration and logging...")

# For each csv-file (containing two days)
for csv in tqdm(os.scandir(directory), total=len(list(os.scandir(directory))), desc="Files", position=1):
    long_path = "data/Hydrated_Tweets_Long/Long_" + os.path.basename(csv.path)
    print(long_path, "HIER")
    if os.path.exists(long_path):
        print(f"skipped {os.path.basename(csv.path)}, because it's already hydrated")
        continue
    if not csv.path.endswith(".csv"):
        print(f"skipped {os.path.basename(csv.path)}")
        continue

    count_files += 1
    metadata_fail = 0

    # Load csv file containing the tweet IDs
    tweets_csv = pd.read_csv(csv.path)  # [:20]  # only first few rows for testing
    try:
        tweets_csv.columns = ["ID", "Sentiment"]
    except ValueError as e:
        print_log(f"{count_files}. File: {csv.path})\n{e} --------------------")
        count_corrupted_files += 1
        continue
    except Exception as f:
        count_corrupted_files += 1
        print(f)
        continue

    del tweets_csv["Sentiment"]  # or better keep, in case we need it later?

    # Initialize panda dataframe for the tweets
    Twitter_Tweets = pd.DataFrame(columns=['ID', 'COUNTRY', 'DAY', 'MONTH', 'TEXT_RAW'])

    # Only countries from the following list are considered
    countries_of_interest = ["Vereinigte Staaten", "Republik Indien", "Vereinigtes Königreich"]

    ID_list = [tweets_csv['ID'].values[i] for i in range(len(tweets_csv['ID'].values))]
    print(len(ID_list))

    twython_errors = 0
    other_errors = 0
    not_of_interest = 0  # count irrelevant countries

    # For each tweet_ID in the file:
    iteration = -1
    for tweet_ID in tqdm(ID_list, desc=f'Tweets in {os.path.basename(csv.path)}', position=0):
        iteration += 1
        # Delay the tweet extraction since otherwise the rate limit exceeds
        if iteration % 50 == 0:
            delay = calc_delay_to_not_run_into_rate_limit(delay=True, request_method='show')
            print("new delay:", ("%.2f" % delay), "secs")
        time.sleep(delay)

        try:
            tweet = python_tweets.show_status(id=tweet_ID, tweet_mode='extended')
        except twython.exceptions.TwythonRateLimitError as too_many_requests:
            print("This should not have happened. Please call the technician. "
                  "(And/or restart program - no real harm should have been done.")
            raise too_many_requests
        except twython.exceptions.TwythonError as e:
            twython_errors += 1
            continue
        except Exception as e:
            other_errors += 1
            continue

        # If all values exist, add the tweets ID, Country, Day, Month and Raw Text to the DF
        try:
            if str(tweet["place"]["country"]) in countries_of_interest:
                data = {
                    'ID': tweet['id'],
                    'COUNTRY': tweet["place"]["country"],
                    'DAY': tweet["created_at"].split()[2],
                    'MONTH': tweet["created_at"].split()[1],
                    'TEXT_RAW': tweet["full_text"]}
                Twitter_Tweets = Twitter_Tweets.append(data, ignore_index=True)
                # print(tweet["text"])
            else:
                not_of_interest += 1

        except Exception as meta_fail:
            metadata_fail += 1
            print(f"Metadata Extraction failed: {meta_fail} (probably no location provided)")
            continue

    # Save DF to csv file
    Twitter_Tweets.to_csv(long_path, index=False, header=True)
    print_log("")
    if len(ID_list) != len(Twitter_Tweets):
        print_log(
            f"{count_files}. File: {os.path.basename(csv.path)}:\n {twython_errors} tweets NOT found or sth. similar."
            f"\n {other_errors} other errors."
            f"\n {metadata_fail} metadata extractions failed.\n {len(Twitter_Tweets)}/{len(ID_list)} tweets extracted."
            f" ({not_of_interest} tweets not of interest)")
    else:
        print_log(f"NO ERRORS IN FILE {count_files}")
    print_log("--------------------")

    # sum up errors
    count_metadata_fail += metadata_fail
    tweets_not_found += twython_errors
    count_other_errors += other_errors

duration = time.time() - start
duration = f"{duration // 3600}h {duration // 60 % 60}m {int(duration % 60)}s"

print_log(f"""-----FINAL REPORT------
        {time.strftime("%d.%m.%y, %H:%M")}
        Looked through {count_files} files.
        {tweets_not_found} tweets not found.
        Metadata extraction failed {count_metadata_fail} times
        {count_corrupted_files} corrupted .csv-files
        execution duration: {duration}\n\n\n""")
