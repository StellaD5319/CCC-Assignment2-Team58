#!/usr/bin/python

"""
This code is used to search the tweets in certain regions from start_date to end_date.

"""
import tweepy
from tweepy import API
from tweepy import OAuthHandler
import datetime
import os, json, sys, argparse
from utils import dbOperations
import time
import datetime

#--------------------------------------------------------------------------------#
##   Global variable define
#--------------------------------------------------------------------------------#
TWITTER_API_PATH = "config/twitter_api.json"
REGION_GEO = './config/regions.json'
CITIES = ["Greater_Sydney", "Greater_Melbourne", "Greater_Brisbane", "Greater_Perth", "Greater_Adelaide"]

#--------------------------------------------------------------------------------#
##   Global variable catch.
#--------------------------------------------------------------------------------#
with open(TWITTER_API_PATH, "r") as key_f:
    TOKENS_TW = json.load(key_f)
with open(REGION_GEO, "r") as geo_f:
    GEO_AREAS = json.load(geo_f)
#--------------------------------------------------------------------------------#
##   Class define
#--------------------------------------------------------------------------------#
class search_API(object):
    def __init__(self, start_time, end_time, db_server, db_name, token_idx=0):
        self.token_idx = token_idx
        self.server = db_server
        self.db_name = db_name
        self.begin = start_time
        self.end = end_time

    def token_get(self, token_index=0):
        return TOKENS_TW[token_index]

    def _build_pipe(self, token):
        auth = OAuthHandler(token["consumer_key"], token["consumer_secret"])
        auth.set_access_token(token["access_token"], token["access_secret"])
        return auth

    def area_to_place_id(self, city_name):
        name = city_name.lower()
        if name in GEO_AREAS.keys():
            return GEO_AREAS[name]["location_id"]
        else:
            print("[-] ERROR not found the city we want to search!!")
            sys.exit(0)

    def search_twitters(self, area="australia"):
        token = self.token_get(self.token_idx)
        auth = self._build_pipe(token)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        if area == "australia":
            place_id = "3f14ce28dc7c4566"
        else:
            place_id = self.area_to_place_id(area)

        public_tweets = tweepy.Cursor(api.search,
                                            q="place:%s -filter:retweets" % place_id,
                                            since=self.begin,
                                            until=self.end).items(1000000)
        return public_tweets

def save_tweets(db_server, db_name, tweets):
    while True:
        try:
            tweet = tweets.next()
            # Insert into db
            db_server.save_views_into_tables(db_name, tweet._json)
        except tweepy.TweepError:
            time.sleep(60 * 15)
            continue
        except StopIteration:
            break

def get_opts():
    """
    Getting the input file.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--city', type=str,
                        default='australia',
                        help='search the position')
    parser.add_argument('--duration', type=str,
                        default='7',
                        help='search the period time of twitters')
    parser.add_argument('--token_id', type=str,
                        default='0',
                        help='use one token. total 5 tokens')
    parser.add_argument('--start_time', type=str,
                        default=None,
                        help="the start time we setting, current + start_time - duration")
    parser.add_argument("--end_time", type=str,
                        default=None,
                        help="the end time we setting, current - end_time")

    return parser.parse_args()


if __name__ == "__main__":
    """
    Set the different cases:
    case1: python search_tweet_interface.py 
           default crawler the australia twitters. save into dbname as "whole"
           default search period is 7 days due to twitter limitation.
    case2: python search_tweet_interface.py city_name
           search certain city, in 7 days.
    case3:  python search_tweet_interface.py city_name
    """

    db_ip = os.getenv("COUCH_DB_IP")
    try:
        container_num = os.getenv("SEARCH_CONTAINER_NUM")
    except:
        pass
    #db_ip = "172.26.129.170"
    dbname = "au_tweets"
    hparams = get_opts()
    if hparams.start_time is not None and hparams.end_time is not None:
        # current time 2021-05-11, if start_time is 2, 
        # start become 2021-05-11 - 7 + 2 --> 2021-05-06.
        # end become 2021-05-11. 
        # period : 2021-05-06 -> 2021-05-11
        # if end_time is 4:
        # 2021-05-11 - 4 = 2021-05-07.
        # period is : 2021-05-06 -> 2021-05-07.
        start = datetime.date.today() - datetime.timedelta(days=int(hparams.duration)+int(hparams.start_time))
        end   = datetime.date.today() - datetime.timedelta(days=int(hparams.end_time))
    else:
        start = datetime.date.today() - datetime.timedelta(days=int(hparams.duration))
        end = datetime.date.today()
    # connect the databases
    client = dbOperations(db_ip=db_ip, db_port=5984, db_username="ccc58", db_passwd="ccc58", databases=[dbname])

    search = search_API(start_time=start, end_time=end, db_server=client,
                        db_name=dbname, token_idx=hparams.token_id)
    tweets = search.search_twitters(hparams.city)
    save_tweets(client, dbname, tweets)
    print("[+] Saving the all tweets into couchdb.")







