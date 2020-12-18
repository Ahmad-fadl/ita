# 1. General

## Project Name 
Time-dependent Sentiment Analysis for Covid-19 including a Correlation Analysis to Relevant Political Events

## Team Members 
* [Ahmad Fadlallah](abohmaid@windowslive.com), 3442106, Applied Computer Science B.A.
* [Severin Laicher](severin.laicher@web.de), 3665790, Applied Computer Science M.Sc.
* [Sina Denzel](sinadenzel@gmail.com), 4018461, Computational Linguistics B.A
* [Ute Gradmann](utegradmann@gmx.de), 4050818, Computational Linguistics B.A.

## Existing Code Fragments
We do not use existing code fragments. 

## Utilized libraries 
See requirements.txt


# 2. Project State

## Actual State
In the conversation with our tutor it was pointed out that we should expect a lot of time for data acquisition, since twitter does not always make it easy to extract large amounts of data quickly (e.g. limited number of requests per user and time). Therefore, we have modified our timeline and put our focus for december mainly on a clean and efficient data acquisition.  As our project aims to analyze corona-related tweets over time, we have used the perfectly matching, already existing dataset decribed in [3. Data Analysis](#data-analysis). So the initial step is downloading all of the roughly 265 csv files (one per day) containting the tweet IDs. In the follwing I will explain the data pipeline we have established so far: 

1. ita/src/Twitter-Access.py

* We import file after file into our python script and for each tweet ID we request the corresponding JSON object from the [Twitter API](https://python-twitter.readthedocs.io/en/latest/). This JSON object contains several metainformation about the tweet. 

* The challenges of the twitter API requests and how we solved them are described in "ita/src/data/Hydrated_Tweets/README.md".

* Here is the point where we had to make some decision. What information from each tweet do we need to keep? We decided to only keep the tweets ID, the country of the tweet, the date of the tweet and the raw text. Other information did not seem to be necessary in the context of our project. 

* Secondary, the tweets from which countries do we keep? Since the objective of our project is a country specific sentiment analysis, we did not keep the tweets from all countries, only selected ones. In our proposal we planned to consider only the USA, New Zealand and England. But, obviously, this only works, if we get enough tweets from all of this countries. Therefore we have checked exemplarily on a small subset of the csv files from which countries the most tweets originated. The USA had by far the most, followed by India, and in third place England. Therefore we decided to only keep and work with tweets from those three countries.  

* So for all tweets of the selected countries each of the mentionend values gets saved into a panda dataframe and is then stored locally. This gets applied to all of the csv files, resulting in 265 locally stored panda dataframes, one for each day. They are stored in "ita/src/data/Hydrated_Tweets".


2. ita/src/Text_Preprocessing.py

* After creating the Panda dataframes for each day, the second step is preprocessing the raw text for the perfect fit to our task. Therefore we import each of the created dataframes, preprocess the raw text and store them again locally.

* The first thing we did is checking a subset of a few hundred raw tweets to get an overview of "typicall tweets". 

* Most of the tweets contain Emojis and since our model will not be poweful enough to consider different types of Emojis, we simply remove them. 

* In Addition we have removed all type of URLs and Links from the tweets, since will not use them either. 

* Moreover we remove all non alphabetic characters, except !?,.#. We keep those characters sine the punctuation of a sentence can contain some information about a persons opinion (e.g "I hate it!!!!!!!!!" seems to be more angry than "I hate it"). For the # and the words that belong to the # we are currently planning a special use. Most tweets contain # and often the word after the # is an underline of the person's opinion. E.g. #Angry.

* Finally we remove all one character words.

* We have tested our preprocessing on one of the csv files (roughly 300 tweets) and the text looked as expected.  

* The preprocessed csv files are stored in "ita/src/data/Preprocessed_Tweets".

 
3. UTE
* <span style="color:red">UTE</span>


## Expected State
In the following we state all subgoals we planned to achieve until end of December, according to our proposal:

1. Data acquisition
* As already mentioned our first main goal was setting up a solid data pipeline. This includes on the one hand the extraction and filtering of the given tweets and on the other hand the text preprocessing. This subgoal was perfectly achieved, the data acquisition python files are written and executed. The data is ready to be analyzed.    

2. Research of political events:
* As part of our project, we are looking for correlations between tweets and infection rates/policies regarding Corona. This requires a detailed background check for the countries investigated. Unfortunately, we have not yet been able to address this task at all, as we have assigned it rather a low priority at the beginning of the project. Since we did not expect it to be done until december 18th but until end of december, we still plan to achieve this goal.   

3. Developing methods for sentiment analysis:
* Just like the research of political events, we planned to finish our sentiment classifier until end of december. Currently, we are convinced that we will achieve this subgoal in time. As described in [Actual State](#actual-state) we have alrady started implementing the classifier, but only rudimentaryly. We still have to put in some implementation effort in achieving this subgoal.  

## Future Planning

### December
1. Finishing the Sentiment Classifier
* <span style="color:red">UTE</span>
2. Prepare Baseline/Evaluation of Classifier
* <span style="color:red">SEVERIN</span>
3. Theoretical Research - USA
* <span style="color:red">SEVERIN</span>
4. Correlation Analysis - USA 
* <span style="color:red">SEVERIN</span>
5. Evaluate Classifier - USA

### January
6. Repeat 3. & 4. & 5 for India

7. Repeat 3. & 4. & 5 for England

8. Cross-National Comparison

### February

8. Finalize Code & Repository

9. Presentaion 

10. Report


# Data Analysis

## Data Sources
We use the [Coronavirus geo-tagged tweets dataset](https://ieee-dataport.org/open-access/coronavirus-covid-19-geo-tagged-tweets-dataset).
The mentioned dataset perfectly fits our project goals, since it contains about 270
thousands of English corona related geo-tagged tweets in the form of their
tweet-ID. The dataset consists of one csv file per day, starting on March 20th
until today. Each entry consists of exactly one tweet-ID and a sentiment score. The fact that the dataset only contains geo-tagged tweets
is very import for our project, since we want to assign each tweet to a specific country. In general this is not given for all tweets, since the user has
to explicitly agree that his tweets get geo-tagged. Additionally, we plan to use the given sentiment scores as a baseline later on. 

## Basic Statistics
* <span style="color:red">AHMAD</span>
The file ... contains various visualizations of the extracted data. You can find all metadata there. 

## Outlook and Examples 
We basically want our sentiment classifier to work as follows: 

* I hate those measures, corona kills me. 

Our classifier detects the words "hate" and "kills" and will (correctly) assign a neagtive sentiment to the sentence. 

But we do not know how well our sentiment analysis will actually work. The challenging part is that tweets are in contrast to e.g. newspaper articles or scientific papers not bounded by any type of language guidelines. Tweets contain human spelling errors, they include slang expressions or are meant ironically. Consider a text like

* Best year ever. Thank you so much Corona. 

What will our model probably do? Since we are probably not able to detect irony, it will erroneously get asigned a positive sentiment. Or consider the following example. 

* I hate school, it's hell on earth for me. But now I'm infected with Corona and I don't have to go to school. 

This is crucial. The classifier will detect the words "hate" and "hell" but it will probably not find out, that those words are actually not connected with the corona infection. Which sentiment should the classifier choose?



```python

```
