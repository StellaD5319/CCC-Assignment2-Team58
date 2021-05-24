#!/bin/bash

sudo docker build -t stream_sy -f Dockerfile_stream_sy .
sudo docker build -t stream_pe -f Dockerfile_stream_pe .
sudo docker build -t stream_ml -f Dockerfile_stream_ml .
sudo docker build -t stream_br -f Dockerfile_stream_br .
sudo docker build -t stream_ad -f Dockerfile_stream_ad .

sudo docker run stream_sy &
sudo docker run stream_pe &
sudo docker run stream_ml &
sudo docker run stream_br &
sudo docker run stream_ad &
