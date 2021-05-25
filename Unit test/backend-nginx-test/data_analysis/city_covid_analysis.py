"""
Analysis the Covid disscusion rate within every different city.
1. Create the view;
2. Get the data from MapReduce view based on different city view.
3. Analysis the text of every tweet within cities.
4. return the JSON to Flask as API.
"""
import re
import os
import couchdb
import logging

#------------------------------------------------------------------------#
#   couchdb class define
#------------------------------------------------------------------------#
class dbOperations(object):
    def __init__(self, db_ip, db_port, db_username, db_passwd, databases=None):
        self.ip = db_ip
        self.port = db_port
        self.username = db_username
        self.passwd = db_passwd
        self.server = None
        self.databases = databases

        self._connect_db()

        self._create_databases()

    def _connect_db(self):
        print("[+] Connecting CouchDB...................")
        try:
            self.server = couchdb.Server("http://{}:{}@{}:{}".format(self.username, self.passwd, self.ip, self.port))
            print("[+] Connecting CouchDB success!!!")
        except Exception as e:
            raise Exception("[-] ERROR: Due to some reasons, Connected DB failed, ", e)

    def _create_databases(self):
        """
           **kwargs: input parameters with key:value
        """
        if self.databases is None:
            raise Exception("[-] ERROR: Input the empty table name, cannot find, error!!")
        if self.databases is str: 
            self.databases = list(self.databases)
        for name in self.databases:
            try:
                self.server.create(name)
                print("[+] Creating database {} success!!".format(name))
            except:
                print("[*] WARNING: the {} already existed.".format(name))
    
    def _create_view(self, db_name, design_doc_name, view_name, map_function, **kwargs):
        data = {
        "_id": f"_design/{design_doc_name}",
        "views": {
            view_name: {
                "map": map_function
                }
        },
        "language": "javascript",
        "options": {"partitioned": False }
        }
        logging.info(f"creating view {design_doc_name}/{view_name}" )
        self.server[db_name].save(data)
    
    def _get_view_data(self, db_name, view_syntax, **kwargs):
        return self.server[db_name].view(view_syntax)

    def save_views_into_tables(self, db_name, json_data):
        ## input key is table name, value is json_data; 
        if db_name not in self.databases:
            self.server.create(db_name)
            self.tables.append(db_name)

        self.server[db_name].save(json_data)
        
    def save(self, **kwargs):
        pass

    #def __del__(self):
    def del_database(self):
        for name in self.databases:
            self.server.delete(name)
        #self.server.close()

#----------------------------------------------------------------#
#    Global Variable Generating
#----------------------------------------------------------------#
## connect the CouchDB
db_name = "au_tweets"
db_ip = os.getenv("COUCH_DB_IP", "null")
if db_ip == "null":
    db_ip = "172.26.129.170"
server = dbOperations(db_ip, db_port=5984, db_username="ccc58", db_passwd="ccc58", databases=[db_name])

#----------------------------------------------------------------#
#    Functions Definitions
#----------------------------------------------------------------#
def generate_map_function(city_name):
    mapFunction = '''function (doc) {
                        if(doc.place.name == "XXX")
                        emit(doc.id, [doc.place.name, doc.text, doc.lang]);
                    }'''.replace("XXX", city_name)
    return mapFunction

def get_data_from_db_views(db_name, city_name): # db_name, design_doc_name, view_name, map_function
    try:
        mapFunction = generate_map_function(city_name)
        server._create_view(db_name, design_doc_name= str(city_name)+"_DOC",
                            view_name= str(city_name)+"_info", map_function=mapFunction)
    except:
        print("[*] view has already exist!")
    view_str = city_name+"_DOC/"+city_name+"_info"
    return server._get_view_data(db_name, view_str)

def process_data(input):
    total_count = 0 
    count = 0
    for item in get_data_from_db_views(db_name=input[0], city_name=input[1]):
        total_count += 1
        if len(item.value[1]) == 0:
            continue
        if "covid" in item.value[1].lower():
            count += 1
    return (input[1], count/total_count)

def _covid_rate_result(db_name):
    cities = ["Sydney", "Melbourne", "Brisbane", "Perth (WA)", "Adelaide"]
    inputs, r = [], {}
    for i in range(len(cities)):
        inputs.append([db_name, cities[i]])
    result = map(process_data, inputs)
    for res in result:
        r[res[0]] = res[1]
    return r


if __name__ == "__main__":
    cities = ["Sydney", "Melbourne", "Brisbane", "Perth (WA)", "Adelaide"]
    #get_data_from_db_views("sydney", cities[0])
    print(_covid_rate_result("whole_au"))