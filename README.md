# Text Analytics Project
* Maintainers
* Requirements for Twitter Access (src/data)

-------------
-------------
## Maintainers
* [Ahmad Fadlallah](abohmaid@windowslive.com), 3442106, Applied Computer Science B.A.
* [Severin Laicher](severin.laicher@web.de), 3665790, Applied Computer Science M.Sc.
* [Sina Denzel](sinadenzel@gmail.com), 4018461, Computational Linguistics B.A
* [Ute Gradmann](utegradmann@gmx.de), 4050818, Computational Linguistics B.A.
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


### Data Preprocessing
* When you have done the above, run ``src/Text_Preprocessing.py``. 
* While this is running, you may want to check out the readme's in ``src/data/Hydrated_Tweets`` and ``src/data/Preprocessed_Tweets`` (not needed to execute the following steps).

### Look at statistics
* If you want to see some statistics about the data .... **TODO** @Ahmad. what should we do to run your code? Please document here. (question: should we transform it to py? jupyter may not be optimal here)

### Sentiment Classification
* When you have done the above, run ``src/Classifier0.2.py``.
* This python file creates feature vectors for the preprocessed tweets saved in `src/data/Sentiment_Tweets`
* May take a few hours.



### Evaluation
* When you have done the above, run ``src/Classifier_Evaluation.py``.
* This python file creates numeric features out of the recently created features. On those features several classifiers are compared regarding their performance using the given sentiments as gold labels. In addition several visualizations are computed and saved locally. 
