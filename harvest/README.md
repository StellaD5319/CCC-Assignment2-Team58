---
Totally need to run 7 containers.

---
couchDB instance:

Run two search containers.

`sudo docker build search_1 -f Dockerfile .`

`sudo docker build search_2 -f Dockerfile_2 .`

`sudo docker run search_1`

`sudo docker run search_2`

---
web instance:

Run two stream containers.

`sudo docker build stream_sy -f Dockerfile_stream_sy .`

`sudo docker build stream_pe -f Dockerfile_stream_pe .`

`sudo docker run stream_sy`

`sudo docker run stream-pe`

---
another instance:

Run three stream containers.

`sudo docker build stream_ml -f Dockerfile_stream_ml .`

`sudo docker build stream_br -f Dockerfile_stream_br .`

`sudo docker build stream_ad -f Dockerfile_stream_ad .`

`sudo docker run stream_ml`

`sudo docker run stream_br`

`sudo docker run stream_ad`

---
Scaling UP/DOWN

The environment in Dockerfile is `SEARCH_CONTAINER_NUM` is determine how many search containers we can set to capture the data at the same time. 

If setting as 2, there are two containers running at the same time, then rougly divide into 3 days, and 4 days.

And it will be config in the openstack.
