# Text Analytics Project
* Maintainers
* Runthrough

-------------
-------------
## Maintainers
* [Ahmad Fadlallah](abohmaid@windowslive.com), 3442106, Applied Computer Science B.A.
* [Severin Laicher](severin.laicher@web.de), 3665790, Applied Computer Science M.Sc.
* [Sina Denzel](sinadenzel@gmail.com), 4018461, Computational Linguistics B.A
* [Ute Gradmann](utegradmann@gmx.de), 4050818, Computational Linguistics B.A.
-------------
## General requirements
* numpy
* twython
* tqdm
* pandas
* matplotlib
* csv
* re
* os
* nltk
* random
* sklearn
* datetime
* scipy

-------------

## Runthrough
To get everything going follow the instructions here. First some requirements need to be met: 

### Requirements for Twitter Access (src/data)
  * [Register](https://www.ieee.org/profile/public/createwebaccount/showRegister.html) for a (free) IEE-Account to get access to the ***GeoCOV19Tweets Dataset***. 
[Download](https://ieee-dataport.org/open-access/coronavirus-covid-19-geo-tagged-tweets-dataset#files 
) all csv-files. There's is no button to do that all at once, 
so you might want to use an extension like [GetThemAll!](https://chrome.google.com/webstore/detail/downthemall/nljkibfhlpcnanjgbnlnbjecgicbjkge). 
If you use Chrome, go to settings, search for "downloads" and deactivate "Ask where to save each file before downloading" for convenience.
Save files in `src/data/GeoCOV19TweetsDataset`
  * open `src/Twitter-Access.py` with an editor and follow the instructions given in the python-file (credentials for the Twitter API * Tweets Hydration)
For the final evaluation we need a file containing some information and numbers regarding Covid-19. Therefore got to https://github.com/owid/covid-19-data/tree/master/public/data and click "Download our complete COVID-19 dataset" as csv. Save the file in `src/data/Classifier_Evaluation/owid-covid-data.csv`. 
 
### Data Preprocessing
* When you have done the above, run ``src/Text_Preprocessing.py``. 
* While this is running, you may want to check out the readme's in ``src/data/Hydrated_Tweets`` and ``src/data/Preprocessed_Tweets`` (not needed to execute the following steps).

### Look at statistics
* To get a better overview and statistics about the data run the file vis.py .
* It visualizes the preproceced data from "data/Preprocessed_Tweets/" so make sure the preprocessed data are in data directory before running this file.
* Data like which country has how many tweets.
* the number of chars in each tweet.
* the most used words....
* It also provides an overview about how many tweet in each month from march to december.

### Sentiment Feature Extraction
* When you have done the above, run ``src/Classifier0.2.py``.
* to run this file you need to download the word lexikon from https://raw.githubusercontent.com/sebastianruder/emotion_proposition_store/master/NRC-Emotion-Lexicon-v0.92/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt into "data/Sentiment_Classifier/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
* May take 25 hours. You can stop and restart the session, since already generated files will be skipped then.
* after running this file the folowing columns will beadded to our dataframe each column is a list of (o or 1) with len="the number of words in each tweet"
* [WORD COUNT]['LEMMATIZED']['Sentiment anger']['Sentiment anticipation']['Sentiment disgust']['Sentiment fear']['Sentiment joy']['NEGATIVE']['POSITIVE']["rawEmojis"]["specialChairs"]["rawHashtags"]
* the new dataframe will be saved in `src/data/Sentiment_Tweets/TweetsWithEmotions`
### Sentiment Classification & Evaluation
* When you have done the above, go to ``src/data/Classifier_Evaluation`` and download the data how it's described in the readme there.
* Now run ``src/Classifier_Evaluation.py``.
* This python file creates numeric features out of the recently created features. This results in an numpy array that contains one row for each tweet and each row consists of multiple numeric features (number of anger words, number of sad words...)
* Then the given sentiment scores are loaded into the program. For now we use them as "gold truth" until we have annotated our own data. 
* Then we test multiple classifiers applying k-fold-cross-validation on the given feature matrix and the given "gold truth".
* The classification task is assigning each tweet either a positive, a negative or a neutral sentiment. 
* Afterwards we choose the best of the recently tested classifiers to for further work. We apply it to all of the tweets in order to get an idea how the final distribution looks like. 
* In addition several visualizations are computed and saved locally in the `src/data/Classifier_Evaluation/` folder as svg.
* May take 15-35 minutes.

### Relation to real world Covid development
* In the file ``src/data/timeline_corona_events_csv.csv`` the main covid-related events in the US, India and the UK are listed by date of the event.
Events of special importance are marked with 'x' and it will be checked if they show effects in twitter data, be it the number of tweets or a specific sentiment.  
  We have collected and put together the data by ourselfs, using these sources: https://www.ajmc.com/view/a-timeline-of-covid19-developments-in-2020,,https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_India_(January%E2%80%93May_2020),,https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_England_(2020),
https://timesofindia.indiatimes.com/india/coronavirus-india-timeline/articleshow/80030867.cms
-------------
