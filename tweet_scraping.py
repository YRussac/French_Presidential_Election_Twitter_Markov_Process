import pprint
import twitter
import os
import json

# Twitter Authentication
CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
OAUTH_TOKEN = os.environ["OAUTH_TOKEN"]
OAUTH_TOKEN_SECRET = os.environ["OAUTH_TOKEN_SECRET"]
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)


# We need to define a list of hashtags
# We start with a list of hashtag of the main candidates for the French presidential elections

hashtag_list = ["#Macron2017", "#Hamon2017", "#MLP2017", "#Fillon2017", "#JLM2017", "#NDA2017", "#Jadot2017"]

for hashtag in hashtag_list:
    print(hashtag)
    search_results = twitter_api.search.tweets(q=hashtag, count=100)
    statuses = search_results['statuses']
    for tweet in statuses:
        print(json.dumps(tweet, indent=2))
        print('----------------')

        # Tweet id
        print(tweet["id"])

        #
        break
    break