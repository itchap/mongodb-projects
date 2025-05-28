from pymongo import MongoClient
from pymongo.errors import PyMongoError
from config import Config
from bson.objectid import ObjectId
import random
import time
import logging

# MongoDB connection setup
try:
    client = MongoClient(Config.MONGODB_URI)  # Use MongoDB URI from config
    db = client[Config.MONGODB_DATABASE]      # Select the database
    collection = db[Config.MONGODB_COLLECTION]  # Select the collection
    logging.info("Successfully connected to MongoDB.")
except PyMongoError as e:
    logging.error(f"Failed to connect to MongoDB: {e}")
    raise

# Function to Generate Complex Graph Data
# Generate realistic parent-child relationships
num_events = 100000
bulk_data = []

for i in range(1, num_events + 1):
    event_id = f"Event_{i}"
    num_children = random.randint(0, 3)
    num_parents = random.randint(0, 2)

    child_links = [f"Event_{i + j}" for j in range(1, num_children + 1) if i + j <= num_events]
    parent_links = [f"Event_{i - j}" for j in range(1, num_parents + 1) if i - j > 0]

    bulk_data.append({
        "_id": event_id,
        "name": f"File_{random.randint(10000, 99999)}",
        "parent_links": parent_links,
        "child_links": child_links,
        "operations": [{"operation": "WRITE", "status": "COMPLETED"}],
        "metadata": {
            "size": random.randint(1000, 5000),
            "owner": f"user{random.randint(1, 10)}",
            "created_at": "2023-12-23",
            "system": "systemA"
        }
    })

# Bulk insert into MongoDB
collection.insert_many(bulk_data)
print(f"Inserted {num_events} events with realistic parent-child relationships.")