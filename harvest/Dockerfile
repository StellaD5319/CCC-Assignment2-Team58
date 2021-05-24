FROM python:3.7

### environment
ENV COUCH_DB_IP=172.26.133.252
ENV HTTP_PROXY=http://wwwproxy.unimelb.edu.au:8000/
ENV HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/

ENV SEARCH_CONTAINER_NUM=2

WORKDIR /app

COPY requirements.txt .
COPY search_tweet_interface.py .

COPY ./utils ./utils
COPY ./config ./config


RUN pip install --no-cache-dir -r requirements.txt

# search the whole australia, and duration is 7 days.
# start as 7 days before, end with current - 3 days.
CMD python search_tweet_interface.py --duration 7 --start_time 0 --end_time 3 --token_id 0

