import re
import pandas as pd
import os
from tqdm import tqdm
import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
import datetime
import matplotlib.patches as mpatches
from scipy.signal import savgol_filter

# Import the gold sentiments
directory = "data/GeoCOV19TweetsDataset"
sentiments = pd.DataFrame(columns=["ID", "gold"])
for entry in tqdm(os.scandir(directory), total=len(list(os.scandir(directory)))):
    try:
        tweets_csv = pd.read_csv(entry.path)
        tweets_csv.columns = ["ID", "gold"]
        sentiments = sentiments.append(tweets_csv)
    except ValueError as e:
        continue

sentiments['ID'] = sentiments['ID'].astype(str)
sentiments['gold'] = sentiments['gold'].astype(float)

# Import the all tweet instances and their corresponding features
directory = "data/Sentiment_Tweets/TweetsWithEmotions"
classified = pd.DataFrame(columns=['ID', 'COUNTRY', 'DAY', 'MONTH', 'TEXT_RAW', 'WORD COUNT', 'LEMMATIZED',
                                   'STRONGSUBJECTIVE', 'WEAKSUBJECTIVE', 'Sentiment anger',
                                   'Sentiment anticipation', 'Sentiment  disgust', 'Sentiment fear',
                                   'Sentiment joy', 'NEGATIVE', 'POSITIVE', 'Sentiment sadness',
                                   'Sentiment surprise', 'Sentiment trust', 'Capital Letters',
                                   'Longest Sequence Capital Letters', 'TEXT_RAW_PUNCTUATION'])

for entry in tqdm(os.scandir(directory), total=len(list(os.scandir(directory)))):
    if entry.path.endswith(".csv"):
        try:
            tweets_csv = pd.read_csv(entry.path)
            tweets_csv.columns = ['ID', 'COUNTRY', 'DAY', 'MONTH', 'TEXT_RAW', 'WORD COUNT', 'LEMMATIZED',
                                  'STRONGSUBJECTIVE', 'WEAKSUBJECTIVE', 'Sentiment anger',
                                  'Sentiment anticipation', 'Sentiment  disgust', 'Sentiment fear',
                                  'Sentiment joy', 'NEGATIVE', 'POSITIVE', 'Sentiment sadness',
                                  'Sentiment surprise', 'Sentiment trust', 'Capital Letters',
                                  'Longest Sequence Capital Letters', 'TEXT_RAW_PUNCTUATION']
            classified = classified.append(tweets_csv)
        except ValueError as e:
            continue

classified['ID'] = classified['ID'].astype(str)


# This methods transforms binary vectors into real numbers
def getValue(liste):
    liste = str(liste)
    summe = 0
    liste = liste.strip('][')
    for val in liste:
        try:
            summe = summe + int(val)
        except:
            continue
    return summe / len(liste.split())


# This methods counts the length of the inputted string and returns it
def countLength(word):
    return len(str(word))


# This methods maps values to either -1,0,1
def getBinary(score):
    score = float(score)
    if score > 0:
        return 1
    elif score < 0:
        return -1
    else:
        return 0


# Put all "features" into the desired format by transforming them into numeric values
classified['Sentiment anger'] = classified['Sentiment anger'].apply(getValue)
classified['Sentiment anticipation'] = classified['Sentiment anticipation'].apply(getValue)
classified['Sentiment  disgust'] = classified['Sentiment  disgust'].apply(getValue)
classified['Sentiment fear'] = classified['Sentiment fear'].apply(getValue)
classified['Sentiment joy'] = classified['Sentiment joy'].apply(getValue)
classified['NEGATIVE'] = classified['NEGATIVE'].apply(getValue)
classified['POSITIVE'] = classified['POSITIVE'].apply(getValue)
classified['Sentiment sadness'] = classified['Sentiment sadness'].apply(getValue)
classified['Sentiment surprise'] = classified['Sentiment surprise'].apply(getValue)
classified['Sentiment trust'] = classified['Sentiment trust'].apply(getValue)
classified['Longest Sequence Capital Letters'] = classified['Longest Sequence Capital Letters'].apply(countLength)

# Here we merge the gold sentiments and the calculated features into one df
classified = pd.merge(classified, sentiments, on="ID")
classified['gold'] = classified['gold'].apply(getBinary)

# The gold labels of each tweet as array
y = np.array(classified["gold"].tolist())

# Only use the "relevant" features
forFeatures = classified[['WORD COUNT', 'Sentiment anger',
                         'Sentiment anticipation', 'Sentiment  disgust', 'Sentiment fear',
                         'Sentiment joy', 'NEGATIVE', 'POSITIVE', 'Sentiment sadness',
                         'Sentiment surprise', 'Sentiment trust', 'Longest Sequence Capital Letters']]

# The feature values of each tweet as array --> feature matrix
x = forFeatures.to_numpy()


# Method that splits data in to k-folds in order to apply k-fold-cross-validation
def split_folds(data, target, L):
    perm = np.random.permutation(range(len(target)))
    X_folds = np.array_split(data[perm], L)
    y_folds = np.array_split(target[perm], L)
    return np.array(X_folds), np.array(y_folds)


# Method that calculates the mean accuracy applying k-fold-cross-validation for a given classifier
def crossValidation(x, y, k, classifier):
    X_folds, y_folds = split_folds(x, y, k)
    f1 = []
    for n in range(0, len(X_folds)):
        X_train_f = np.concatenate([X_folds[i] for i in range(k) if i != n])
        X_test_f = X_folds[n]
        y_train_f = np.concatenate([y_folds[i] for i in range(k) if i != n])
        y_test_f = y_folds[n]
        classifier.fit(X_train_f, y_train_f)
        y_pred = classifier.predict(X_test_f)
        f1.append(f1_score(y_test_f, y_pred, average='micro'))

    return np.mean(np.array(f1))


######## Test multiple classifiers
"""
clf = DecisionTreeClassifier(random_state=0)
f1 = crossValidation(x, y, 5, clf)
print(f"{clf} : f1-score: {f1}\n")

clf = RandomForestClassifier(max_depth=10, random_state=0)
f1 = crossValidation(x, y, 5, clf)
print(f"{clf} : f1-score: {f1}\n")

clf = KNeighborsClassifier(n_neighbors=10)
f1 = crossValidation(x, y, 5, clf)
print(f"{clf} : f1-score: {f1}\n")

clf = GaussianNB()
f1 = crossValidation(x, y, 5, clf)
print(f"{clf} : f1-score: {f1}\n")
"""

####### Fix one classifier and show results

# Choose on classifier and apply it on the complete dataset
clf = DecisionTreeClassifier(random_state=0)
clf.fit(x, y)
predictedLabels = clf.predict(x)

# Append prediction to df
classified["prediction"] = list(predictedLabels)

# Method that converts string into date object
def convertToDate(date):
    date = str(date)
    if str(date.split()[1]) == "Jan":
        date = datetime.datetime.strptime("{0} 2021".format(date), "%d %b %Y").strftime("%d-%m-%Y")
        date = datetime.date(int(date.split("-")[2]), int(date.split("-")[1]), int(date.split("-")[0]))
    else:
        date = datetime.datetime.strptime("{0} 2020".format(date), "%d %b %Y").strftime("%d-%m-%Y")
        date = datetime.date(int(date.split("-")[2]), int(date.split("-")[1]), int(date.split("-")[0]))
    return date


# Convert day+month to date object
classified['DAY'] = classified['DAY'].astype(str)
classified['date'] = classified['DAY'] + " " + classified['MONTH']
classified['date'] = classified['date'].apply(convertToDate)

# For Total Count
relativeSentiments = classified[['COUNTRY', 'date', 'prediction']]
maskNegative = (classified['prediction'] == -1)
maskNeutral = (classified['prediction'] == 0)
maskPositive = (classified['prediction'] == 1)
negatives = relativeSentiments[maskNegative]
neutrals = relativeSentiments[maskNeutral]
positives = relativeSentiments[maskPositive]

negatives = negatives.groupby('date').count()[["prediction"]]
neutrals = neutrals.groupby('date').count()[["prediction"]]
positives = positives.groupby('date').count()[["prediction"]]
negatives = negatives.rename(columns={"prediction": "Negative"})
neutrals = neutrals.rename(columns={"prediction": "Neutral"})
positives = positives.rename(columns={"prediction": "Positive"})
TotalSentiments = pd.merge(negatives, neutrals, left_index=True, right_index=True)
TotalSentiments = pd.merge(TotalSentiments, positives, left_index=True, right_index=True)

x = TotalSentiments.index.tolist()
yNeg = TotalSentiments["Negative"].tolist()
yNeut = TotalSentiments["Neutral"].tolist()
yPos = TotalSentiments["Positive"].tolist()

fig, ax = plt.subplots(figsize=(12, 7))
negativePatch = mpatches.Patch(color='red', label='Negative')
neutralPatch = mpatches.Patch(color='black', label='Neutral')
positivePatch = mpatches.Patch(color='green', label='Positive')

plt.legend(loc="upper left", handles=[negativePatch, neutralPatch, positivePatch], fontsize=15)

plt.title('Total Sentiments over time', fontsize=15)
plt.xticks(rotation='vertical', fontsize=15)
plt.yticks(rotation='horizontal', fontsize=15)

yNeg = savgol_filter(yNeg, 51, 5)  # window size 51, polynomial order 3
yNeut = savgol_filter(yNeut, 51, 5)  # window size 51, polynomial order 3
yPos = savgol_filter(yPos, 51, 5)  # window size 51, polynomial order 3

plt.plot(x, yNeg, linewidth=2, color="black")
plt.plot(x, yNeut, linewidth=2, color="red")
plt.plot(x, yPos, linewidth=2, color="green")

plt.show()
fig.savefig("data/Classifier_Evaluation/1)TotalSentiments.svg", format="svg")

# For Country Count USA
relativeSentiments = classified[['COUNTRY', 'date', 'prediction']]
relativeSentiments = relativeSentiments.loc[relativeSentiments['COUNTRY'] == "Vereinigte Staaten"]

maskNegative = (classified['prediction'] == -1)
maskNeutral = (classified['prediction'] == 0)
maskPositive = (classified['prediction'] == 1)

negatives = relativeSentiments[maskNegative]
neutrals = relativeSentiments[maskNeutral]
positives = relativeSentiments[maskPositive]

negatives = negatives.groupby('date').count()[["prediction"]]
neutrals = neutrals.groupby('date').count()[["prediction"]]
positives = positives.groupby('date').count()[["prediction"]]
negatives = negatives.rename(columns={"prediction": "Negative"})
neutrals = neutrals.rename(columns={"prediction": "Neutral"})
positives = positives.rename(columns={"prediction": "Positive"})
TotalSentiments = pd.merge(negatives, neutrals, left_index=True, right_index=True)
TotalSentiments = pd.merge(TotalSentiments, positives, left_index=True, right_index=True)

x = TotalSentiments.index.tolist()
yNeg = TotalSentiments["Negative"].tolist()
yNeut = TotalSentiments["Neutral"].tolist()
yPos = TotalSentiments["Positive"].tolist()

fig, ax = plt.subplots(figsize=(12, 7))
negativePatch = mpatches.Patch(color='red', label='Negative')
neutralPatch = mpatches.Patch(color='black', label='Neutral')
positivePatch = mpatches.Patch(color='green', label='Positive')

plt.legend(loc="upper left", handles=[negativePatch, neutralPatch, positivePatch], fontsize=15)

plt.title('Total Sentiments over time USA', fontsize=15)
plt.xticks(rotation='vertical', fontsize=15)
plt.yticks(rotation='horizontal', fontsize=15)

yNeg = savgol_filter(yNeg, 51, 5)  # window size 51, polynomial order 3
yNeut = savgol_filter(yNeut, 51, 5)  # window size 51, polynomial order 3
yPos = savgol_filter(yPos, 51, 5)  # window size 51, polynomial order 3

plt.plot(x, yNeg, linewidth=2, color="black")
plt.plot(x, yNeut, linewidth=2, color="red")
plt.plot(x, yPos, linewidth=2, color="green")

plt.show()
fig.savefig("data/Classifier_Evaluation/2)TotalSentiments_USA.svg", format="svg")

# For Country Count USA
relativeSentiments = classified[['COUNTRY', 'date', 'prediction']]
relativeSentiments = relativeSentiments.loc[relativeSentiments['COUNTRY'] == "Republik Indien"]

maskNegative = (classified['prediction'] == -1)
maskNeutral = (classified['prediction'] == 0)
maskPositive = (classified['prediction'] == 1)

negatives = relativeSentiments[maskNegative]
neutrals = relativeSentiments[maskNeutral]
positives = relativeSentiments[maskPositive]

negatives = negatives.groupby('date').count()[["prediction"]]
neutrals = neutrals.groupby('date').count()[["prediction"]]
positives = positives.groupby('date').count()[["prediction"]]
negatives = negatives.rename(columns={"prediction": "Negative"})
neutrals = neutrals.rename(columns={"prediction": "Neutral"})
positives = positives.rename(columns={"prediction": "Positive"})
TotalSentiments = pd.merge(negatives, neutrals, left_index=True, right_index=True)
TotalSentiments = pd.merge(TotalSentiments, positives, left_index=True, right_index=True)

x = TotalSentiments.index.tolist()
yNeg = TotalSentiments["Negative"].tolist()
yNeut = TotalSentiments["Neutral"].tolist()
yPos = TotalSentiments["Positive"].tolist()

fig, ax = plt.subplots(figsize=(12, 7))
negativePatch = mpatches.Patch(color='red', label='Negative')
neutralPatch = mpatches.Patch(color='black', label='Neutral')
positivePatch = mpatches.Patch(color='green', label='Positive')

plt.legend(loc="upper left", handles=[negativePatch, neutralPatch, positivePatch], fontsize=15)

plt.title('Total Sentiments over time Indien', fontsize=15)
plt.xticks(rotation='vertical', fontsize=15)
plt.yticks(rotation='horizontal', fontsize=15)

yNeg = savgol_filter(yNeg, 51, 5)  # window size 51, polynomial order 3
yNeut = savgol_filter(yNeut, 51, 5)  # window size 51, polynomial order 3
yPos = savgol_filter(yPos, 51, 5)  # window size 51, polynomial order 3

plt.plot(x, yNeg, linewidth=2, color="black")
plt.plot(x, yNeut, linewidth=2, color="red")
plt.plot(x, yPos, linewidth=2, color="green")

plt.show()
fig.savefig("data/Classifier_Evaluation/3)TotalSentiments_Indien.svg", format="svg")

# For Country Count USA
relativeSentiments = classified[['COUNTRY', 'date', 'prediction']]
relativeSentiments = relativeSentiments.loc[relativeSentiments['COUNTRY'] == "Vereinigtes Königreich"]

maskNegative = (classified['prediction'] == -1)
maskNeutral = (classified['prediction'] == 0)
maskPositive = (classified['prediction'] == 1)

negatives = relativeSentiments[maskNegative]
neutrals = relativeSentiments[maskNeutral]
positives = relativeSentiments[maskPositive]

negatives = negatives.groupby('date').count()[["prediction"]]
neutrals = neutrals.groupby('date').count()[["prediction"]]
positives = positives.groupby('date').count()[["prediction"]]
negatives = negatives.rename(columns={"prediction": "Negative"})
neutrals = neutrals.rename(columns={"prediction": "Neutral"})
positives = positives.rename(columns={"prediction": "Positive"})
TotalSentiments = pd.merge(negatives, neutrals, left_index=True, right_index=True)
TotalSentiments = pd.merge(TotalSentiments, positives, left_index=True, right_index=True)

x = TotalSentiments.index.tolist()
yNeg = TotalSentiments["Negative"].tolist()
yNeut = TotalSentiments["Neutral"].tolist()
yPos = TotalSentiments["Positive"].tolist()

fig, ax = plt.subplots(figsize=(12, 7))
negativePatch = mpatches.Patch(color='red', label='Negative')
neutralPatch = mpatches.Patch(color='black', label='Neutral')
positivePatch = mpatches.Patch(color='green', label='Positive')

plt.legend(loc="upper left", handles=[negativePatch, neutralPatch, positivePatch], fontsize=15)

plt.title('Total Sentiments over time England', fontsize=15)
plt.xticks(rotation='vertical', fontsize=15)
plt.yticks(rotation='horizontal', fontsize=15)

yNeg = savgol_filter(yNeg, 51, 5)  # window size 51, polynomial order 3
yNeut = savgol_filter(yNeut, 51, 5)  # window size 51, polynomial order 3
yPos = savgol_filter(yPos, 51, 5)  # window size 51, polynomial order 3

plt.plot(x, yNeg, linewidth=2, color="black")
plt.plot(x, yNeut, linewidth=2, color="red")
plt.plot(x, yPos, linewidth=2, color="green")

plt.show()
fig.savefig("data/Classifier_Evaluation/4)TotalSentiments_England.svg", format="svg")

# For Total Sentiments + Total Infections
##########################################################################
path = "data/Classifier_Evaluation/owid-covid-data.csv"
coronaMeta = pd.read_csv(path, index_col=False)
coronaMeta = coronaMeta[["location", "date", "new_cases", "new_deaths"]]
coronaMeta = coronaMeta.loc[coronaMeta['location'].isin(['India', 'United Kingdom', 'United States'])]
coronaMeta['date'] = pd.to_datetime(coronaMeta['date'])
adaptDate = coronaMeta['date'] >= datetime.datetime(2020, 4, 1)
coronaMeta = coronaMeta[adaptDate]
coronaMeta['new_deaths'] = coronaMeta['new_deaths'].fillna(0)

coronaMeta = coronaMeta[["date", "new_cases"]]
coronaMeta = coronaMeta.set_index('date')

relativeSentiments = classified[['COUNTRY', 'date', 'prediction']]
maskNegative = (classified['prediction'] == -1)
maskNeutral = (classified['prediction'] == 0)
maskPositive = (classified['prediction'] == 1)
negatives = relativeSentiments[maskNegative]
neutrals = relativeSentiments[maskNeutral]
positives = relativeSentiments[maskPositive]

negatives = negatives.groupby('date').count()[["prediction"]]
neutrals = neutrals.groupby('date').count()[["prediction"]]
positives = positives.groupby('date').count()[["prediction"]]
negatives = negatives.rename(columns={"prediction": "Negative"})
neutrals = neutrals.rename(columns={"prediction": "Neutral"})
positives = positives.rename(columns={"prediction": "Positive"})
TotalSentiments = pd.merge(negatives, neutrals, left_index=True, right_index=True)
TotalSentiments = pd.merge(TotalSentiments, positives, left_index=True, right_index=True)

TotalSentiments = pd.merge(TotalSentiments, coronaMeta, left_index=True, right_index=True)

x = TotalSentiments.index.tolist()
yNeg = TotalSentiments["Negative"].tolist()
yNeut = TotalSentiments["Neutral"].tolist()
yPos = TotalSentiments["Positive"].tolist()
yTotal = [(yNeg[i] + yNeut[i] + yPos[i]) for i in range(0, len(yPos))]

yInfections = TotalSentiments["new_cases"].tolist()
yInfections = [0.01 * (yInfections[i]) for i in range(0, len(yInfections))]

fig, ax = plt.subplots(figsize=(12, 7))
tweets = mpatches.Patch(color='black', label='Tweets')
infections = mpatches.Patch(color='red', label='New Infections * 0.01')

plt.legend(loc="upper left", handles=[tweets, infections], fontsize=15)

plt.title('Sentiments vs. Infections over time ', fontsize=15)
plt.xticks(rotation='vertical', fontsize=15)
plt.yticks(rotation='horizontal', fontsize=15)

yTotal = savgol_filter(yTotal, 51, 5)  # window size 51, polynomial order 3
yInfections = savgol_filter(yInfections, 51, 5)  # window size 51, polynomial order 3

plt.plot(x, yTotal, linewidth=2, color="black")
plt.plot(x, yInfections, linewidth=2, color="red")

plt.show()
fig.savefig("data/Classifier_Evaluation/5)TotalSentiments+TotalInfections.svg", format="svg")
