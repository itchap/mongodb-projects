from pymongo import MongoClient
from pymongo.errors import PyMongoError
from config import Config
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

# Function to Run Descendant Query
def find_descendants(start_event, max_depth=20):
    """Find all descendants starting from a specific node."""
    print(f"\nFinding descendants for {start_event}...")
    pipeline = [
        {"$match": {"_id": start_event}},
        {"$graphLookup": {
            "from": "events",
            "startWith": "$child_links",
            "connectFromField": "child_links",
            "connectToField": "_id",
            "as": "descendants",
            "maxDepth": max_depth
        }},
        {"$project": {"_id": 1, "descendants_count": {"$size": "$descendants"}}}
    ]
    result = list(collection.aggregate(pipeline))
    print(f"Descendants for {start_event}: {result}")

# Function to Run Ancestor Query
def find_ancestors(start_event, max_depth=20):
    """Find all ancestors starting from a specific node."""
    print(f"\nFinding ancestors for {start_event}...")
    pipeline = [
        {"$match": {"_id": start_event}},
        {"$graphLookup": {
            "from": "events",
            "startWith": "$parent_links",
            "connectFromField": "parent_links",
            "connectToField": "_id",
            "as": "ancestors",
            "maxDepth": max_depth
        }},
        {"$project": {"_id": 1, "ancestors_count": {"$size": "$ancestors"}}}
    ]
    result = list(collection.aggregate(pipeline))
    print(f"Ancestors for {start_event}: {result}")

if __name__ == "__main__":
    print("Starting Aggregation Queries...")

    # Example event to query
    start_event = "Event_5000"  # Change as needed
    max_depth = 20

    # Run Queries
    find_descendants(start_event=start_event, max_depth=max_depth)
    find_ancestors(start_event=start_event, max_depth=max_depth)

    print("\nAggregation queries complete.")