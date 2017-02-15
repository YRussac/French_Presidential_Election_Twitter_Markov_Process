import pprint
import twitter
import os
import json
import time

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
hashtag_list2=["#Macron2017"]

# We browse the list and we only keep the info we want from the tweets

# print are here for debugging, once we will have defined all the info we want to keep
# we'll save it in a dataframe

for hashtag in hashtag_list2:

    print(hashtag)

    # To handle "Too many requests" error
    Too_Many_Requests = True
    while Too_Many_Requests:
        try:
            # result_type = recent (only recent tweets), popular (only popular tweets) or mixed
            # count is the number of tweet we want to get, max_count=100
            # q is the query
            search_results = twitter_api.search.tweets(q=hashtag, result_type="recent", count=1)
            Too_Many_Requests = False
        except:
            print("Too many requests !")
            Too_Many_Requests = True
            time.sleep(100)

    statuses = search_results['statuses']
    print("statut de type:")
    print(type(statuses))
    for tweet in statuses:

        #print(json.dumps(tweet, indent=2))
        print('----------------')

        # Tweet info
        # Tweet id :
        print(tweet["id"])

        # Tweet localisation :
        print(tweet["geo"])

        # Tweet text :
        print(tweet['text'])

        # User info
        # Tweet from @... (author) :
        print(tweet["user"]["screen_name"])

        # Author number of followers
        print(tweet["user"]["followers_count"])

        # Author number of friends (number of accounts he follows)
        print(tweet["user"]["friends_count"])

        # Author id :
        print(tweet["user"]["id"])
        print("Ceci est le contenu intégral du tweet")
        print(tweet)
