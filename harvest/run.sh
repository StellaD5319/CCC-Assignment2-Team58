#!/bin/bash

sudo docker build -t stream_sy -f Dockerfile_stream_sy .
sudo docker build -t stream_pe -f Dockerfile_stream_pe .
sudo docker build -t stream_ml -f Dockerfile_stream_ml .
sudo docker build -t stream_br -f Dockerfile_stream_br .
sudo docker build -t stream_ad -f Dockerfile_stream_ad .

sudo docker run stream_sy --restart=always &
sudo docker run stream_pe --restart=always &
sudo docker run stream_ml --restart=always &
sudo docker run stream_br --restart=always &
sudo docker run stream_ad --restart=always &
