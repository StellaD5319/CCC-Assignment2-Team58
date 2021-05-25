#!/bin/bash

python search_tweet_interface.py --duration 3 --token_id 2 &
python stream_tweet_interface.py adelaide 0 &
