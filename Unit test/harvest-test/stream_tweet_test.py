#!/usr/bin/python

"""
This code is used to stream the tweets in certain regions.
"""

import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import json
import sys, os
from utils import dbOperations
import datetime as dt
import couchdb
import http.client

# put different consumer_keys
def _get_twitter_api(token_idx='0'):
    #set up twitter authentication
    # Return: tweepy.OAuthHandler object

    twitter_api_file = './config/twitter_api.json'
    with open(twitter_api_file, "r") as f:
        tokens = json.load(f)

    auth = OAuthHandler(tokens[token_idx]["consumer_key"], tokens[token_idx]["consumer_secret"])
    auth.set_access_token(tokens[token_idx]["access_token"], tokens[token_idx]["access_secret"])
    return auth

def _get_coordinates_base_city(city):
    region_geo = './config/regions.json'
    locations = []
    with open(region_geo, 'r') as f:
        city_geo = json.load(f)
        try:
            locations = city_geo[city]["coordinate"]
        except Exception as e:
            print("[-] ERROR : some error happen, ", e)
    return locations


@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

class MyListener(StreamListener):
    def __init__(self, db_server, db_name):
        self.db_name = db_name
        self.server = db_server

    def on_data(self, data):
        try:
            self.server.save_views_into_tables(self.db_name, json.loads(data))
        except AttributeError:
            print("[-] ERROR : some error happen, ", data)
        except http.client.IncompleteRead as e:
            print(e.partial)
            file = e.partial
        return True

    def on_error(self, status):
        print(status)
        return True

def get_twitters_stream(location, db_server, db_name):
    # Set the hashtag to be searched
    twitter_stream = Stream(_get_twitter_api(), MyListener(db_server, db_name))

    # twitter_stream.filter(place!=None)
    twitter_stream.filter(locations=location)


if __name__ == '__main__':
    """
    Test the function of harvest API.
    """
    token_idx = '0'
    geo_only = False
    db_ip = "172.26.129.170" # test database IP.
    #db_ip = "172.26.129.170"
    db_name = "whole_au"
    client = dbOperations(db_ip=db_ip, db_port=5984,
                          db_username="ccc58", db_passwd="ccc58", databases=[db_name])
    if len(sys.argv) == 2:
        city = sys.argv[1]
        location = _get_coordinates_base_city(city)
        print("Harvest streaming tweets from {} ...".format(city))
        get_twitters_stream(location, client, db_name)
    elif len(sys.argv) > 2:
        city = sys.argv[1]
        api_get = sys.argv[2]
        location = _get_coordinates_base_city(city)
        print("Harvest streaming tweets from {} with API {} ...".format(city, api_get))
        get_twitters_stream(location, client, db_name)
    else:
        print("Please input city name and API number...")

