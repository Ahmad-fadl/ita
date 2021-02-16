This is where the file or files of the manual annotation go to.  
To start manual annotation just run ``src/manual_annotation.py ``


## Annotation Guide
- Rate if the tweet is negative (-1), neutral (0) or positive (1).
- If you can't tell or if not applicable choose (0) too.
- Rate it regarding the Corona situation. (example: 'I hate my sister!' would be (0))
- If you see something positive, but are not sure if it's really THAT much positive or even actually positive, choose (1).
- Rate the sentiment that is (somehow) transported by the tweeter - do not rate the positivity of the provided facts. (example: neutral conveyed news about rise in deaths)
- Don't click on links or google for unknown concepts. Tweet itself = Full information (Exception: unknown vocabluary)You can cancel and continue anytime.
- Hashtags and Emojis are part of the tweet and its sentiment.

## Annotation Flow
- At the current state (16.02.21), if you run the ``src/manual_annotation.py `` you will first annotate the same 20 tweets as all of us.  
This is to check again if we annotate in the same way and to discuss it in our group meeting.
- After that you will annotate the the same 50 tweets as all of us.  
This is to recalculate kappa and later build the 'medoid' average to also use these tweets for training.
  Please tell group members when you are working on it. Else we may get conflicts. Upload after a session. Pull before starting.
- if completed, the annotation for another 250 tweets will start. Each of us get different tweets.
- if completed, the existing dicts get merged. When we all have uploaded our pickle-files, the last person finishing, should also upload the generated merged dict.
- since the single dicts (4x250 splits) are separated and get re-merged at the end, there is no need to wait for team members to upload/update their annotations.
- at the end we have 1000+50 gold labeled sentiment tweets for training.

## Notes
- You can stop and continue annotating any time
