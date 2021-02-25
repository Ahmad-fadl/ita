* ``Hydrated_Tweets_Long`` is where the **long** tweets go to.  
They replace the former dir ``Hydrated_Tweets``, the tweets there were cut off.   ``
Twitter-Access.py`` was updated, so now the long tweets will be hydrated (but that will have a longer execution duration) 
using another extraction method.
  
### Rename dir afterwards
* For further use - after hydrating - you should **rename** this folder back to ``Hydrated_Tweets``, 
so that the further processing uses these tweets, not the short ones.