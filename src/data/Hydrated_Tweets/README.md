# Text Analytics Project

This is the readme for `src/data/Hydrated_Tweets`.
This directory should be empty at the beginning. This is where the hydrated tweets will go to.  
Due to twitters user guidlines you are not allowed to pass the original tweets, so you need to repeat the hydration by your own.   
This is currently managed in `ita-project/Twitter-Access.py`.  
See main readme.
-----------
### Issues
* In the extracted files is one column too much. Some tweets show text in there, like " Pub  â€” https://t.co/ndtlNUjAbi" or " LEARN CLUB https://t.co/WNDCww4mm4"  
TODO Why / Remove them ?  
* File october28_october29.csv (File 214) lead to an error: `ValueError: Length mismatch: Expected axis has 1 elements, new values have 2 elements`, pointing to line 
`tweets_csv.columns = ["ID","Sentiment"]`. Currently handled by Exception Catch and omitting file.  
TODO check problem, fix corrupted file(s)? 

-------------
### Number of Tweets and "Too many Requests"
At 15. Dez. 2020 the sum of IDs in the original Dataset is 273.016. 
You can check this or future volume increase via bash with  `cat *.csv | wc -l`  
This could be relevant for request limits, for extraction, but just once.  
Twitter seems to use a sliding window for remaining requests / restart time, but further research is needed. 
We have implemented a time-delay-function, which is useful when using `/statuses/show` to not run into limits.
But we have replaced that method with using batch-extraction (100 Tweets per batch).  
In 15 minutes you can now make 90.000 requests when using the Twython lookup_status method (100 tweets==1 batch per second), 
so we would exceed the request rate limit thrice if the runtime was 0 seconds. 
Since the extraction for 880 tweets (9 batches=requests) took 20 seconds in a test, 
we don't reach the rate limit anymore. We keep the delay-function and the parameter option to make use of it or not (delay=True/False), in case something changes or other systems run in better time and then get a Too Many Request Error.
Btw: There are only daytime request limits for `/statuses/mentions_timelines` and `/statuses/user_timeline`,
which we don't use ([source](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/faq#:~:text=What%20are%20the%20new%20rate,auth%20and%20app%2Dauth%20requests.)).

----------
### Packaging
* install Twyton package for Twitter-Access.py
* install geopy
* install tqdm
* TODO: something missing? 
 ----------
### Recommendation for optics
* If you are using PyCharm and want a proper looking loading bar output while hydrating the Tweets, go to `Run` `Edit Configurations` and check `Emulate terminal in output console`.

-------------
### Requirements for src/data

