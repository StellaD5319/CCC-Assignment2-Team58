---
Totally need to run 7 containers.

---
couchDB instance:

Run two search containers.

`sudo docker build -t search_1 -f Dockerfile .`

`sudo docker build -t search_2 -f Dockerfile_2 .`

`sudo docker run search_1 --restart=always`

`sudo docker run search_2 --restart=always`

---
web instance:

Run two stream containers.

`sudo docker build -t stream_sy -f Dockerfile_stream_sy .`

`sudo docker build -t stream_pe -f Dockerfile_stream_pe .`

`sudo docker run stream_sy --restart=always`

`sudo docker run stream-pe --restart=always`

---
another instance:

Run three stream containers.

`sudo docker build -t stream_ml -f Dockerfile_stream_ml .`

`sudo docker build -t stream_br -f Dockerfile_stream_br .`

`sudo docker build -t stream_ad -f Dockerfile_stream_ad .`

`sudo docker run stream_ml --restart=always`

`sudo docker run stream_br --restart=always`

`sudo docker run stream_ad --restart=always`

---
Scaling UP/DOWN

The environment in Dockerfile is `SEARCH_CONTAINER_NUM` is determine how many search containers we can set to capture the data at the same time. 

If setting as 2, there are two containers running at the same time, then rougly divide into 3 days, and 4 days.

And it will be config in the openstack.

---
Because the containters will fail due to some unknonw errors, we set the container restart after it fail.
