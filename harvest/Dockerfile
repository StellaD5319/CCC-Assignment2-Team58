FROM python:3.7

### environment
ENV COUCH_DB_IP = 172.26.133.252
ENV HTTP_PROXY=http://wwwproxy.unimelb.edu.au:8000/
ENV HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/

COPY requirements.txt /app
COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

# search the whole australia, and duration is 7 days.
python search_tweet_interface.py

