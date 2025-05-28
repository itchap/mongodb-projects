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

1. Use the provided Python script to populate the live collection with sample system log data.
2. Update the MongoDB connection string in the script with your MongoDB Atlas credentials and cluster details.
3. Run the script to insert the specified number of system logs into the live collection.

```python
from pymongo import MongoClient
import datetime
import random
from dateutil.relativedelta import relativedelta
import sys

# Connect to MongoDB
client = MongoClient('mongodb+srv://<username>:<password>@<hostname>/?retryWrites=true&w=majority')
db = client['test']
collection = db['sample_logs']

# Function to generate a random system log
def generate_system_log():
    log_levels = ["INFO", "WARNING", "ERROR"]
    log_messages = [
        "System startup",
        "Database connection established",
        "User login failed",
        "Insufficient disk space",
        "Network connection lost",
        "Critical error occurred",
    ]

    log_level = random.choice(log_levels)
    log_message = random.choice(log_messages)
    timestamp = generate_random_timestamp()

    log = {
        "level": log_level,
        "message": log_message,
        "timestamp": timestamp
    }

    return log

# Function to generate a random timestamp from the past 6 months
def generate_random_timestamp():
    current_time = datetime.datetime.now()
    six_months_ago = current_time - relativedelta(months=6)
    random_timestamp = random.uniform(six_months_ago.timestamp(), current_time.timestamp())
    return datetime.datetime.fromtimestamp(random_timestamp)

# Insert generated system logs into MongoDB
def insert_logs(num_logs):
    for _ in range(num_logs):
        log = generate_system_log()
        collection.insert_one(log)

# Get the number of logs to insert from command line argument
if len(sys.argv) > 1:
    num_logs = int(sys.argv[1])
else:
    num_logs = 10  # Default value

# Call the insert_logs function to insert the specified number of system logs
insert_logs(num_logs)
```
``` bash
python3 logGenerator.py 10000
```

``` bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
aws configure set role_arn arn:aws:iam::123456789012:role/defaultrole
aws configure set source_profile default
aws configure set role_session_name session_user1
aws configure set region us-west-2
aws configure set output json
```

### Step 3: Configure Federated Archive Cluster

1. Create a MongoDB Atlas cluster for the federated archive.
2. Enable Data Federation in the federated archive cluster.
3. Configure the AWS S3 bucket integration with the federated archive cluster. This allows the archiving process to copy data to the S3 bucket using the `$out` operator.

<img width="1201" alt="image" src="https://github.com/itchap/mongodb-guides/assets/75799589/81b4cc31-c405-495d-8514-465dcc49d0b1">
<img width="573" alt="image" src="https://github.com/itchap/mongodb-guides/assets/75799589/f6f599a6-f8a4-4eea-bc14-ec89de841a93">
<img width="887" alt="image" src="https://github.com/itchap/mongodb-guides/assets/75799589/e856876a-6b98-4f3d-b004-244e7dc549b4">
<img width="919" alt="image" src="https://github.com/itchap/mongodb-guides/assets/75799589/bb0f8894-e8bd-49fb-a13c-8d97475ae2bc">
<img width="916" alt="image" src="https://github.com/itchap/mongodb-guides/assets/75799589/727d6d2b-f54d-4636-bd47-e71b7b9bc6e5">
<img width="909" alt="image" src="https://github.com/itchap/mongodb-guides/assets/75799589/400c15d5-0c57-4f0d-91ad-999e10917b35">
<img width="900" alt="image" src="https://github.com/itchap/mongodb-guides/assets/75799589/d4bdfd6c-b579-4ff2-9cd4-22aa5d84ec22">
<img width="876" alt="image" src="https://github.com/itchap/mongodb-guides/assets/75799589/269e54c3-5e0c-4191-ab57-0c8624a9b83e">
<img width="750" alt="image" src="https://github.com/itchap/mongodb-guides/assets/75799589/3fa31742-0925-4027-9b2f-14777940ade2">
<img width="929" alt="image" src="https://github.com/itchap/mongodb-guides/assets/75799589/511c53c4-615b-4f1e-bdc9-a2864e023bd8">
<img width="863" alt="image" src="https://github.com/itchap/mongodb-guides/assets/75799589/9e0e289b-329d-4af6-aedf-701cd0795630">
<img width="924" alt="image" src="https://github.com/itchap/mongodb-guides/assets/75799589/d09a1bbe-40fb-4069-a8e2-2c31d500ca21">


### Step 4: Create Serverless Function

1. Create a serverless function in MongoDB Atlas.
2. Use the provided JavaScript code to define the serverless function.
3. Customize the code according to your specific requirements.
4. Set the schedule for the serverless function to run every hour.

``` javascript
exports = async function () {
  const DAYS_TO_SUBTRACT = 160; // Number of days to subtract from the current date

  const currentDate = new Date();
  const start_date = new Date(currentDate.getTime() - DAYS_TO_SUBTRACT * 24 * 60 * 60 * 1000); // Subtract days from the current date

  // Get the 'logs' collection from the 'prodArchive' database in the 'FederatedArchive' service
  const collName = context.services.get('FederatedArchive').db('prodArchive').collection('logs');

  // Define the aggregation pipeline for archiving
  const pipeline = [
    {
      $match: {
        timestamp: {
          $lt: start_date
        }
      }
    },
    {
      $out: {
        s3: {
          bucket: 'mongodb-user-demo-bucket',
          region: 'eu-central-1',
          filename: `${start_date.toISOString().replace(/:/g, '-')}Z-${currentDate.toISOString().replace(/:/g, '-')}Z`,
          format: { name: 'json', maxFileSize: '200MiB' }
        }
      }
    }
  ];

  // Archive data by running the aggregation pipeline
  await collName.aggregate(pipeline).toArray();
  console.log('Archive created!');

  // Get the 'sample_logs' collection from the 'test' database in the 'DemoCluster' service
  const collName2 = context.services.get('DemoCluster').db('test').collection('sample_logs');

  // Define the deletion query to remove archived records
  const deleteQuery = {
    timestamp: {
      $lt: start_date
    }
  };

  // Delete archived data
  const deleteResult = await collName2.deleteMany(deleteQuery);
  console.log('Deleted', deleteResult.deletedCount, 'records.');
};
```

### Step 5: Query Cold Data from S3 via Data Federation

1. Use the provided Python script to query the cold data stored in the S3 bucket through the federated archive cluster.
2. Update the MongoDB connection string in the script with your MongoDB Atlas credentials and cluster details.
3. Customize the script by setting the desired time range and log level for the query.
4. Run the script to retrieve the matching documents and aggregated results from the S3 bucket.

```python
from pymongo import MongoClient
import datetime

# Connect to the MongoDB server
client = MongoClient('mongodb://<username>:<password>@<hostname>/?ssl=true&authSource=admin')

# Access the desired database and collection
db = client.get_database('prodArchive')
coll = db.get_collection('logs')

print('A query to see all the docs from S3 where there were ERROR logs between midnight and noon on a specified date:')

# Define the time range and level for the query
start_time = datetime.datetime(2023, 4, 9, 0, 0, 0)  # Replace with your desired start time
end_time = datetime.datetime(2023, 4, 9, 12, 0, 0)  # Replace with your desired end time
level = 'ERROR'  # Replace with your desired level

# Perform a separate find query for the specified time range and level
find_query = {
    'timestamp': {
        '$gte': start_time,
        '$lte': end_time
    },
    'level': level
}

# Execute the find query and retrieve the results
result = coll.find(find_query)

# Print the matching documents
for doc in result:
    print(doc)

print('\nI can also run an aggregation pipeline to group all log levels on the specified date.')

# Define the aggregation pipeline stages
pipeline = [
    {
        '$match': {
            'timestamp': {
                '$gte': start_time,
                '$lte': end_time
            }
        }
    },
    {
        '$group': {
            '_id': '$level',
            'count': { '$sum': 1 }
        }
    },
    {
        '$project': {
            '_id': 0,
            'level': '$_id',
            'count': 1
        }
    }
]

# Execute the aggregation pipeline and retrieve the results
agg_result = coll.aggregate(pipeline)

# Print the aggregated results
for result in agg_result:
    print(result)
```

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

