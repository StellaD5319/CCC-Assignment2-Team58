User Guide

1. Prerequisite

Users need to install Ansible to run all shell files, and the OpenStack password for this project is OGU4NzU4NzM1MzYxMmI5.


2. Deploy instances on MRC


./run_deployment_instance.sh
python inventory/record_instances.py
 
In this step, ansible would automate install required packages such as python3 and OpenStack into localhost, create required volumes, security groups and instances. Three instances are created and attached with specified volumes, and we need to record their IP in the inventory file and host variables file for further use. Python file record_instances.py could record all instances created and allocate them to different groups when executed. Therefore, we can orchestrate them by group name later.
 
3.Configure instances on MRC

./run_config.sh

This step would upload a private key to the remote and add a proxy to all instances to allow access from external. After that, it would install dependencies, set up the environment required to run docker and mount the volume.
 
4. Deploy database

./run_database.sh

This step deploys the database in a specific instance, the database used in this system is single-node CouchDB. It installs all packages required and CouchDB, modifies the configuration file and then restarts the server.

5. Deploy back-end

./run_back-end.sh 

This step deploys the back-end in a specific instance and Flask is required in this instance. It installs Flask, modifies the configuration file and then restarts the server. 

7. Deploy web application
8. 
./run_front-end.sh

This step deploys the front-end in the specific instance. Nginx is used for web application interfaces, so it installs Nginx, modifies the configuration file and then restarts the server.
 
9. Deploy harvest

./run_crawler.sh

This step deploys seven harvests in three instances, it deploys two search containers and five stream containers in total and distributes them into three instances.
