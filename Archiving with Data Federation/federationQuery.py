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