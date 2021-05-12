# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import tweepy
import requests
import couchdb
import json



def auth_twitter(com_key, com_secret, acc_token, acc_secret):
    # auth = tweepy.OAuthHandler(com_key, com_secret, callback_url)   # if not dynamic delete callback_url
    """
    Twitter authorization
    :param consumer_key:
    :param consumer_secret:
    :param access_token:
    :param access_secret:
    :return: tweeter api
    """

    auth = tweepy.OAuthHandler(com_key, com_secret)
    auth.set_access_token(acc_token, acc_secret)

    api = tweepy.API(auth)
    return api

def topTrendOfCities(api):
    """

    :param api:
    :return: each city top 50 trends hashtage in dictionary
    """
    WOEID_list = {"Sydney": "1105779", "Melbourne": "1103816", "Brisbane": "1100661", "Perth": "1098081",
                  "Adelaide": "1099805"}
    city_trend = {}
    for key, value in WOEID_list.items():
        city_trend[key] = api.trends_place(value)
    #city_top_trend = json.dumps(city_trend)
    return city_trend


def search_tweet_by_keyWords(kw, n):
    tweet_list = api.search(q = kw, count = n)
    return tweet_list

def trace_history_tweet(userid, n):
    hist_tweet = api.user_timeline(user_id = userid, count = n, exclude_replies = True)
    return hist_tweet

def convertinto_JSON(input_data, fileName):
    with open(fileName, "w") as f:
        json.dump(input_data, f)

    with open(fileName, "r") as f:
        out_put = json.load(f)
    print("file created and save")

def save_to_DB(input_data, fileName, server, output):
    input_data = json.load(open(fileName, "r"))
    for i in data:
        server[output].save(i)
    print("save data into CouchDB.")

def search_twitter_by_user(userid, n):
    user_tweet = api.user_timeline(user_id="2199299744", count=1, exclude_replies=True)
    return user_tweet


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ### build key and secret dictionary for use
    consumer_dic = {}
    acc_dic = {}
    consumer_k = "hd0ZhrIeZUWDQyprivabPkDmF"
    consumer_s = "vlAktprTXC9bA9GNtzgKrCqMeRM9WI68PJHC2MiNmhOkQ6X3Yf"

    acc_key = "928941886777180160-IJEgfP6I9RSAe5C3QPTbpBixCYZ0XlQ"
    acc_secret = "uvzR4wHYSAl0zeqEwLKkWbIYq0CNMeMnJ10AQ27bI5E4V"

    ### connect with CouchDB
    client = couchdb.Server(url='http://admin:admin@172.26.132.57:5984')

    # call authorization function
    api = auth_twitter(consumer_k, consumer_s, acc_key, acc_secret)


    # top trend hashtage analysis
    city_trends = topTrendOfCities(api)
    #convertinto_JSON(city_trends, top_hashtages)


    #r = search_tweet_by_keyWords("Melbourne", 1)
    #print(r, type(r))

    D = api.user_timeline(user_id = "2199299744", count = 1, exclude_replies = True)
    print(D, type(D))
