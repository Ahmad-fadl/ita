#!/usr/bin/env python
# coding: utf-8

import re
import pandas as pd
import os
from tqdm import tqdm


log_into_file = True
def print_log(msg):
    """Use instead of print, to print and log.
    Set global variable 'log_into_file to False, is logging not wished."""
    global log_into_file
    tqdm.write(msg)  # similar to print, but better optics when using tqdm loading bar
    if log_into_file:
        with open("data/Preprocessed_Tweets_Report.txt", "a") as log:
            log.write(msg+"\n")


emoji_subs_fails = 0
url_subs_fails = 0
remove_specialChairs_fails = 0





# Remove Emojis Method
def remove_emojis(data):
    global emoji_subs_fails
    try:
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
        return re.sub(emoji, '', data)
    except Exception as e:
        print_log(e)
        emoji_subs_fails += 1
        return data


# Remove URLS Method
def remove_urls(data) -> str:
    global url_subs_fails
    try:
        return str(re.sub(r'http\S+', '', data))
    except Exception as e:
        print_log(e)
        url_subs_fails += 1
        return str(data)

    
# Remove all non alphabetic chairs but some selected
def remove_specialChairsAll(data) -> str:
    global remove_specialChairs_fails
    try:
        regex = re.compile('[^a-zA-Z ]')
        data = regex.sub('', str(data))
        return ' '.join([w for w in data.split() if len(w)>1])
    except Exception as e:
        print_log(e)
        remove_specialChairs_fails += 1
        return str(data) 
    

count_files = 0
directory = "data/Hydrated_Tweets"

# For each file/day
for entry in os.scandir(directory):
    if not entry.path.endswith(".csv"):
        print(f"skipped {os.path.basename(entry.path)}")
        continue
    count_files += 1
    
    # Load csv file containing the tweet ID's
    Twitter_Tweets = pd.read_csv(entry.path)



    # Preprocessing: Remove all emojis from the raw text
    #Twitter_Tweets['TEXT_RAW'] = Twitter_Tweets['TEXT_RAW'].apply(remove_emojis)
    # Preprocessing: Remove all URLs from the raw text    
    Twitter_Tweets['TEXT_RAW'] = Twitter_Tweets['TEXT_RAW'].apply(remove_urls)
    # Preprocessing: Kremove every non alphabetic chair
    Twitter_Tweets['TEXT_RAW'] = Twitter_Tweets['TEXT_RAW'].apply(remove_specialChairsAll)    
    # Keep the raw text with punctuation etc. if we need it
    Twitter_Tweets['TEXT_RAW_PUNCTUATION'] = Twitter_Tweets['TEXT_RAW']
    


    # Save DF to csv file
    Twitter_Tweets.to_csv("data/Preprocessed_Tweets/" + os.path.basename(entry.path), index=False, header=True)
    print_log(f"File {count_files}, {os.path.basename(entry.path)} contains: {len(Twitter_Tweets)} Tweets")
    
print_log(f"-----FINAL REPORT------\n"
          f"Looked through {count_files} Files. \n"
          f"{emoji_subs_fails} emoji substitutions failed \n"
          f"{url_subs_fails} URL substitutions failed. \n"
          f"{remove_specialChairs_fails} Special chair substitutions failed.\n\n\n")
