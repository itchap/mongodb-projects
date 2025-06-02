# MongoDB Atlas Data Archiving with Data Federation

This is a documentation guide for setting up a MongoDB Atlas Data Archiving solution using Atlas Data Federation. The solution involves automating the archiving of cold data from a live cluster collection in MongoDB Atlas to an AWS S3 bucket using a MongoDB Atlas Trigger, Serverless Function, and Data Federation.

## Architecture Overview

The architecture of the solution consists of the following components:

1. **Live Cluster**: The MongoDB Atlas cluster where the live collection resides.
2. **Federated Archive Pipeline**: The MongoDB Atlas Federated instance used for archiving cold data to AWS S3 parquet files.
3. **Federated Databse**: The MongoDB Atlas Federated instance used for accessing and querying parquet files in AWS S3.
4. **Atlas Trigger**: A trigger in MongoDB Atlas that monitors changes in the live collection.
5. **Serverless Function**: A serverless JS function that is triggered by the Atlas Trigger and performs the sceduled archiving of cold data.
6. **AWS S3 Bucket**: The destination for storing the archived data.

## Setup Instructions

### Step 1: Create Live Collection and Cluster

1. Create a MongoDB Atlas cluster for the live data.
2. Create a database and collection in the live cluster to store the system log data.

### Step 2: Populate Sample System Log Data

1. Use the provided Python script [(logGenerator.py)](https://github.com/itchap/mongodb-projects/blob/main/Archiving%20with%20Data%20Federation/logGenerator.py) to populate the live collection with sample system log data.
2. Add the MongoDB connection string to a local .env file with your MongoDB Atlas credentials and cluster details.
``` bash
MONGODB_URI=mongodb+srv://[USERNAME]:[PASSWORD]@[DOMAIN]/?retryWrites=true&w=majority&appName=loggenerator
```
3. Run the logGenerator.py script to insert the specified number of system logs into the live collection.
``` bash
python3 logGenerator.py 10000
```

### Step 3: Create an S3 Bucket

1. Log in to AWS and go to the S3 service section (ensure you're using the right region in AWS)
2. Create a new bucket and give it a name like `atlasfederatedarchive` (use the default settings) 

### Step 4: Configure Federated Archive Cluster

1. Create a Federated Database that feeds downstream systems like AWS S3 with your data to Parquet, CSV, BSON, or Extended JSON files
2. Select AWS as the cloud provider
3. Give your Federated Database Instance a name like - awsS3FederatedArchive
4. Next add the live source cluster and database collection you want to archive
5. Authorise a new AWS IAM Role or use an exiting one
6. Follow the instruction to create New Role with the AWS CLI (use a name like atlas-data-archive-role)
7. Don't forget to install AWS CLI and do an SSO login
``` bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
aws configure sso
aws sts get-caller-identity --profile xyz-id
```
Take the sso config details
If already installed, you will need to establish a new sso session 
``` bash
aws sso login --profile xyz-id
```
8. Run this command in the terminal to generate a ARN for the new IAM role
``` bash
aws iam create-role \                                                                                                                                                          ✔  took 12s  
 --role-name atlas-federation-archive-role \
 --assume-role-policy-document file://role-trust-policy.json \
 --profile xyz
```
9. Copy the ARN value and paste it into Atlas and click on validate.
10. Next add the name of the S3 bucket you created earlier (e.g. atlasfederatedarchive)
11. Follow the instructions to give Atlas access to the bucket
``` bash
aws iam put-role-policy \
  --role-name atlas-federation-archive-role \
  --policy-name atlas-federation-archive-role-policy \
  --policy-document file://adl-s3-policy.json \
  --profile xyz
```
12. Then validate access is possible
13. Finally configure the trigger scedule and how you would like the JS Funciton to output the data to the AWS s3 (e.g. Parquet or JSON)
14. Click on create once you are happy with the configuration


### Step 5: Update the Trigger Function to Archive and Delete 

1. Go to the Triggers section in Atlas and locate the the Trigger created in the previous section.
2. Copy the code provided in JavaScript file [(trigger-function.js)](https://github.com/itchap/mongodb-projects/blob/main/Archiving%20with%20Data%20Federation/trigger-function.js)  to define the serverless function
3. Make sure that the names used in your federation configuration are represented correctly in the script.
``` script
  // Configuration constants for services, database, and collection
  const ARCHIVE_SERVICE = 'awsS3FederatedArchive';  // S3-linked Atlas Data Federation service
  const CLUSTER_SERVICE = 'DemoCluster';            // Primary Atlas Cluster
  const DB_NAME = 'system-logs';                    // Database name
  const COLL_NAME = 'db-server-01';                 // Collection name
  const BUCKET_NAME = 'atlasfederatedarchive';      // S3 bucket name for archive
```
4. Click on Save
5. Run to test
6. Tweak the script further if needed and save.

### Step 6: Setup Data Federated Database for Accessing Data diretly from in S3 storage

1. In the Data Federation section of Atlas, select `Create New Federated Database` and chose the manual option
2. Select AWS and give the Federated Database Instance a name (e.g. awsS3FederatedDatabase)
3. Next click on Add Data Sources and select AWS
4. Select the previously created IAM role
5. Enter the name of the previously created S3 bucket (e.g. atlasfederatedarchive)
6. Make sure you select read and write permissions
7. Specify the previously configured bucket prefix (e.g. databaseLogs/)
8. Skip the next step as you have previously granted access to the bucket
9. Now set the s3 uri path to the stored parquet files (e.g. s3://atlasfederatedarchive/databaseLogs/*)
10. Configure final path folder as any value *
11. Drag the S3 Store path to the virtual collection
12. Rename Virtual Database (e.g. virtual-db-system-logs ) and Collection (virtual-coll-db-server-01) accordingly and then click save

### Step 6: Query Cold Data from S3 via the new Atlas Federated Database

1. Use the provided Python script [(federationQuery.py)](https://github.com/itchap/mongodb-projects/blob/main/Archiving%20with%20Data%20Federation/federationQuery.py) to query the cold data stored in the S3 bucket through the federated database instance.
2. Update the MongoDB connection string in the .env file with your MongoDB Atlas credentials and connection details.
3. Customise the script by setting the desired time range and log level for the query.
4. Run the script to retrieve the matching documents and aggregated results from the S3 bucket.

## Indexing Recommendations

To optimize the performance of your live cluster queries during the archive job, consider creating appropriate indexes on the fields used in your filter query. Based on the provided JS function, you may consider indexing the following field:

  - `timestamp`: Create an ascending index on the `timestamp` field.


