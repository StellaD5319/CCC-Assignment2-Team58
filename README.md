# CCC-Assignment2-Team58

---
backServer:

Flask + Nginx, Flask is used to connect the CouchDB, then get some data. Wrap it into API giving to front <Melody>. Main API focus on  `/api/` `/app/` two parts.

Nginx is for load balanced for the flask. Then, using sock 5000 as communicated way to connect to flask, now, only one flask as Master. Open port is 8080, to public.

The font files: put into `/data/` in docker container.


