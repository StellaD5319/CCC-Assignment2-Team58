from . import dbOperations
import os
import json

db_ip = os.getenv("COUCH_DB_IP")
db_port = os.getenv("COUCH_DB_PORT")
db_username = os.getenv("COUCH_DB_USER")
db_passwd = os.getenv("COUCH_DB_PASSWD")

db_list =  ["aurin", "twitter","test123","try123"]
db_server = dbOperations(db_ip, db_port, db_username, db_passwd, ["aurin", "twitter","test123","try123"])

for db in db_list:
    db_server.save_views_into_tables(db, json.load(open("utils/data.json","r")))
