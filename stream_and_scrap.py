import json
import os
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import pprint
import twitter
import time
import io
import ast

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
OAUTH_TOKEN = os.environ["OAUTH_TOKEN"]
OAUTH_TOKEN_SECRET = os.environ["OAUTH_TOKEN_SECRET"]

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth)
start_time = time.time() #grabs the system time
users_observed = {}


def information_user(id,tweets_number,dico):
    """
    :param id: c'est l'id de l'utilisateur twitter que l'on considère
    :param tweets_number: nombre de derniers tweet sur lesquels on récupère les infos
    :param dico: dictionnaire qui devra contenir l'ensemble des informations pour les utilisateurs observés
    :return: actualise le dictionnaire avec les nouvelles valeurs
    """
    user = api.get_user(id)
    dico[id] = {}
    print(user.screen_name)
    dico[id]["user.screen_name"] = user.screen_name
    print(user.followers_count)
    dico[id]["user.followers_count"] = user.followers_count
    print(user.friends_count)
    dico[id]["user.friends_count"] = user.friends_count
    statuses = api.user_timeline(id,count=tweets_number)
    dico[id]["statuses"] = {}
    dico[id]["statuses"]["id_tweet"] = []
    dico[id]["statuses"]["Text"] = []
    dico[id]["statuses"]["Geo"] = []
    dico[id]["statuses"]["hashtags"] = []
    dico[id]["statuses"]["user_mentions"] = []
    for tweet in statuses:
        print("Observation d'un nouveau tweet...")
        print("|||")
        print("id du tweet:")
        print(tweet.id)
        dico[id]["statuses"]["id_tweet"] += [tweet.id]
        print("Text du tweet observé:")
        print(tweet.text)
        dico[id]["statuses"]["Text"] += [tweet.text]
        print("géographie:")
        print(tweet.geo)
        dico[id]["statuses"]["Geo"] += [tweet.geo]
        print("Mention du Tweet:")
        print(tweet.entities["hashtags"])
        print(tweet.entities["user_mentions"])
        dico[id]["statuses"]["hashtags"] += [tweet.entities["hashtags"]]
        dico[id]["statuses"]["user_mentions"] += [tweet.entities["user_mentions"]]
    print("Fin affichage des informations utilisateurs et mentions")
    print(dico[id])
        # Rq: dans id pour user mentions c'est bien l'id du compte tweeter mentionné.
        # la fonction information_user fonctionne par effet de bords!

class StdOutListener(StreamListener):

    def __init__(self,start_time,time_limit=60):
        self.time = start_time
        self.limit = time_limit
        self.tweet_data = []


    def on_data(self, data):
        saveFile = io.open('raw_tweets.json', 'a', encoding='utf-8')
        saveFile2 = io.open('info_utilisateurs.txt', 'a', encoding='utf-8')
        while (time.time() - self.time) < self.limit:
            #print(data)
            print("Affichage de l'id d'utilisateur:")
            decoded=json.loads(data)
            print(decoded["user"]["id"])
            temp_user_id=decoded["user"]["id"]
            if temp_user_id not in users_observed:
                print("Utilisateur non observé !")
                # We had the information for this unobserved user
                information_user(temp_user_id, 2, users_observed)
            print("------")
            print()

        #print('@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore')))
        #champs utiles à premiere vue: text, id_str, user[screen_name],user['id_str'], geo, statuses_count, friends_count,created_at,followers_count
            try:
                self.tweet_data.append(data)

            except BaseException as e:
                print('failed ondata,', str(e))
                time.sleep(60)
                pass
            return True
        saveFile = io.open('raw_tweets.json', 'w', encoding='utf-8')
        saveFile.write(u'[\n')
        saveFile.write(','.join(self.tweet_data))
        saveFile.write(u'\n]')
        saveFile.close()
        print("le dictionnaire d'information ressemble à:")
        print(users_observed)
        saveFile2.write(str(users_observed))
        saveFile2.close()
        exit()


    def on_error(self, status):
        print(status)
        print("j'affiche status")
        print("------")
        print("ZZZZZZZZZZZZZZZZZZZZZZZ")

if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener(start_time,time_limit=10)
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the #hashtags of the french candidates for the presidential election
    stream.filter(track=["#Macron2017", "#Hamon2017", "#MLP2017", "#Fillon2017", "#JLM2017", "#NDA2017", "#Jadot2017"])

