import json
import os
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import time

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
OAUTH_TOKEN = os.environ["OAUTH_TOKEN"]
OAUTH_TOKEN_SECRET = os.environ["OAUTH_TOKEN_SECRET"]

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth)


def user_information(user_id, number_of_tweets=200):
    user = api.get_user(user_id)

    d_json = {"screen_name": user.screen_name,  "followers_count": user.followers_count,
              "friends_count": user.friends_count, "user_location": user.location, "tweets": []}

    statuses = api.user_timeline(user_id, count=number_of_tweets)

    for tweet in statuses:
        d_tweet = {"tweet_id": tweet.id_str, "text": tweet.text, "tweet_geo": tweet.geo,
                   "hashtags": tweet.entities["hashtags"], "user_mentions": tweet.entities["user_mentions"],
                   "date": tweet.created_at}
        d_json["tweets"].append(d_tweet)

    print(d_json)
    print("ℵ")
    return True


class StdOutListener(StreamListener):

    def __init__(self, time_limit=10000):
        self.time = time.time()
        self.limit = time_limit
        self.tweet_data = []

    def on_data(self, data):

        decoded = json.loads(data)

        user_id = decoded["user"]["id_str"]

        if user_id not in observed_users.keys():
            # New user
            # We add the information for this unobserved user
            too_many_requests = True
            while too_many_requests:
                try:
                    user_information(user_id, 50)
                    observed_users[user_id] = 1
                    too_many_requests = False
                except:
                    time.sleep(10)
        else:
            observed_users[user_id] += 1

        if (time.time() - self.time) > self.limit:
            print(observed_users)
            exit()

        return True

    def on_error(self, status):
        print("Error !")

if __name__ == '__main__':

    observed_users = {}

    l = StdOutListener(time_limit=300)
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data by the hashtags of the french candidates for
    # the presidential election

    stream.filter(track=["#Macron2017", "#Hamon2017", "#MLP2017", "#Fillon2017", "#JLM2017", "#NDA2017", "#Jadot2017"])

