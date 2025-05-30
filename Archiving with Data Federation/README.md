# MongoDB Atlas Data Archiving with Data Federation

This is a documentation guide for setting up a MongoDB Atlas Data Archiving solution using Atlas Data Federation. The solution involves automating the archiving of cold data from a live cluster collection in MongoDB Atlas to an AWS S3 bucket using a MongoDB Atlas Trigger, Serverless Function, and Data Federation.

## Architecture Overview

The architecture of the solution consists of the following components:

1. **Live Cluster**: The MongoDB Atlas cluster where the live collection resides.
2. **Federated Archive**: The MongoDB Atlas cluster used for data federation with AWS S3.
3. **Atlas Trigger**: A trigger in MongoDB Atlas that monitors changes in the live collection.
4. **Serverless Function**: A serverless function that is triggered by the Atlas Trigger and performs the archiving of cold data.
5. **AWS S3 Bucket**: The destination for storing the archived data.

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

### Step 3: Configure Federated Archive Cluster

1. Create a MongoDB Atlas Federated Database Instance for the federated archive.
2. Select AWS as the cloud provider
3. Give your Federated Database Instance a name like - s3FederatedArchive
4. Next add a new Data Souce (i.e. AWS S3 Bucket)
5. Authorise a AWS IAM Role
6. Create New Role with the AWS CLI (use a name like atlas-data-archive-role)
7. Don't forget to install AWS CLI and do an SSO login 
``` bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
aws configure sso
aws sts get-caller-identity --profile xyz-id
``` 

<img width="922" alt="image" src="https://github.com/user-attachments/assets/4fc3c4da-2884-4890-9741-3ab3e673b3fd" />

3. Configure the AWS S3 bucket integration with the federated archive cluster. This allows the archiving process to copy data to the S3 bucket using the `$out` operator.

### Step 4: Create Serverless Function

1. Create a serverless function in MongoDB Atlas.
2. Use the provided JavaScript code to define the serverless function.
3. Customize the code according to your specific requirements.
4. Set the schedule for the serverless function to run every hour.

### Step 5: Query Cold Data from S3 via Data Federation

1. Use the provided Python script to query the cold data stored in the S3 bucket through the federated archive cluster.
2. Update the MongoDB connection string in the script with your MongoDB Atlas credentials and cluster details.
3. Customize the script by setting the desired time range and log level for the query.
4. Run the script to retrieve the matching documents and aggregated results from the S3 bucket.


## Indexing Recommendations

To optimize the performance of your queries, consider creating appropriate indexes on the fields used in your queries. Based on the provided serverless function and query script, you may consider indexing the following fields:

- For the aggregation pipeline query:
  - `timestamp`: Create an ascending index on the `timestamp` field.
  - `level`: Create an ascending index on the `level` field.

- For the find query:
  - `timestamp`: Create an ascending index on the `timestamp` field.
  - `level`: Create an ascending index on the `level` field.

Make sure to create the indexes in both the live cluster and the federated archive cluster to optimize query performance.

**Note**: The index creation may vary depending on your specific data and query requirements. Consider analyzing the query patterns and workload characteristics to determine the most suitable indexing strategy for your use case.

