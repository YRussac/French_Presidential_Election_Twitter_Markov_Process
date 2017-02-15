import json
import os
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
OAUTH_TOKEN = os.environ["OAUTH_TOKEN"]
OAUTH_TOKEN_SECRET = os.environ["OAUTH_TOKEN_SECRET"]


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        
        print(data)
        #we could use json to filter only data that we need: decoded = json.loads(data) 
        #print('@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore')))
        #champs utiles à premiere vue: text, id_str, user[screen_name],user['id_str'], geo, statuses_count, friends_count,created_at,followers_count 
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the #hashtags of the french candidates for the presidential election
    stream.filter(track=["#Macron2017", "#Hamon2017", "#MLP2017", "#Fillon2017", "#JLM2017", "#NDA2017", "#Jadot2017"])

#to save it in a file, print python stream_mining.py > tweets_data.txt