# ops manager demo

Login - http://ec2-18-116-240-150.us-east-2.compute.amazonaws.com:8080/v2/63e144151d1d7f31c240ae48#deployment/topology

Agent - mongodb-mms-automation-agent-manager_10.14.24.6508-1_amd64.ubuntu1604.deb
10.14.24.6508-1

API Key
63e1444c1d1d7f31c240ae770f3932dada0b85ef0e01adbe4d1a3775

Project ID
63e144151d1d7f31c240ae48

Path you should use for enabling backup is /data/headdb
No username or password needed

The temporary password, if promoted, is 260VT8Wi6Its


mongodump --uri mongodb+srv://itchap:NokiaN900@democluster.0wrhw.mongodb.net/sample_airbnb
mongodump --uri mongodb+srv://itchap:NokiaN900@democluster.0wrhw.mongodb.net/sample_analytics
mongodump --uri mongodb+srv://itchap:NokiaN900@democluster.0wrhw.mongodb.net/sample_geospatial
mongodump --uri mongodb+srv://itchap:NokiaN900@democluster.0wrhw.mongodb.net/sample_guides
mongodump --uri mongodb+srv://itchap:NokiaN900@democluster.0wrhw.mongodb.net/sample_mflix
mongodump --uri mongodb+srv://itchap:NokiaN900@democluster.0wrhw.mongodb.net/sample_restaurants
mongodump --uri mongodb+srv://itchap:NokiaN900@democluster.0wrhw.mongodb.net/sample_supplies
mongodump --uri mongodb+srv://itchap:NokiaN900@democluster.0wrhw.mongodb.net/sample_training
mongodump --uri mongodb+srv://itchap:NokiaN900@democluster.0wrhw.mongodb.net/sample_weatherdata

mongorestore --host server01 --port 27019 --username itchap --password NokiaN900 ./dump


mongodump --uri mongodb+srv://<DB_USERNAME>:<PASSWORD>@<DATABASE_HOSTNAME>/<DATABASE> 

mongodump --host localhost --port 27019 --username <DB_USERNAME> --password <DB_PASSWORD> ./dump
mongorestore --uri mongodb+srv://<DB_USERNAME>:<DB_PASSWORD>@<ATLAS_CLUSTER_DOMAIN>.mongodb.net ./dump/

curl -OL http://admin:8080/download/agent/automation/mongodb-mms-automation-agent-manager_12.0.17.7665-1_amd64.ubuntu1604.deb
sudo dpkg -i mongodb-mms-automation-agent-manager_12.0.17.7665-1_amd64.ubuntu1604.deb
sudo vi /etc/mongodb-mms/automation-agent.config
sudo mkdir -p /data
sudo chown mongodb:mongodb /data
sudo systemctl start mongodb-mms-automation-agent.service
sudo systemctl status mongodb-mms-automation-agent.service
