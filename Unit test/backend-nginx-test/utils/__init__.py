## It will put the operations to CouchDB.
import couchdb, os
import logging

db_ip = os.getenv("COUCH_DB_IP")
db_port = os.getenv("COUCH_DB_PORT")
db_username = os.getenv("COUCH_DB_USER")
db_passwd = os.getenv("COUCH_DB_PASSWD")

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