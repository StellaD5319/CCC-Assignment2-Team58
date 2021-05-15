#!/bin/bash

# Using to config the network for apt-get and docker
echo "Start to config the network for downloading the packages!!!!"

echo "HTTP_PROXY=http://wwwproxy.unimelb.edu.au:8000/"  >> /etc/environment
echo "HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/" >> /etc/environment
echo "http_proxy=http://wwwproxy.unimelb.edu.au:8000/"  >> /etc/environment
echo "https_proxy=http://wwwproxy.unimelb.edu.au:8000/" >> /etc/environment
echo "no_proxy=localhost,127.0.0.1,localaddress,172.16.0.0/12,.melbourne.rc.nectar.org.au,.storage.unimelb.edu.au,.cloud.unimelb.edu.au" >> /etc/environment

source /etc/environment

echo "Finish------------!!!"

echo "Start to config the docker network!!!!"

mkdir -p /etc/systemd/system/docker.service.d

touch /etc/systemd/system/docker.service.d/http-proxy.conf

echo "[Service]" >> /etc/systemd/system/docker.service.d/http-proxy.conf

echo 'Environment="HTTP_PROXY=http://wwwproxy.unimelb.edu.au:8000/" "HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/" "no_proxy=localhost,127.0.0.1,localaddress,172.16.0.0/12,.melbourne.rc.nectar.org.au,.storage.unimelb.edu.au,.cloud.unimelb.edu.au"' >> /etc/systemd/system/docker.service.d/http-proxy.conf

sudo systemctl daemon-reload
sudo systemctl restart docker

echo "Finish all network config!!!"



