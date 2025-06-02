import logging
from datetime import datetime
from pymongo import MongoClient, errors
from config import Config  # Assumes this exists just like in your generator script

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def connect_to_federated_mongo() -> MongoClient:
    """
    Establishes connection to the federated MongoDB instance using the URI from Config.
    Returns:
        MongoClient instance
    """
    try:
        client = MongoClient(Config.FEDERATED_URI)
        client.admin.command("ping")
        logging.info("Connected to Federated MongoDB successfully.")
        return client
    except errors.PyMongoError as e:
        logging.error(f"Failed to connect to Federated MongoDB: {e}")
        raise SystemExit(1)

def query_error_logs(collection, target_day: datetime):
    """
    Find and log all ERROR level logs between midnight and noon on a given date.
    Args:
        collection: The MongoDB collection to query.
        target_day (datetime): The date to filter logs for.
    """
    start_time = target_day.replace(hour=0, minute=0, second=0)
    end_time = target_day.replace(hour=12, minute=0, second=0)

    query = {
        "timestamp": {
            "$gte": start_time,
            "$lte": end_time
        },
        "level": "ERROR"
    }

    logging.info(f"Querying ERROR logs from {start_time} to {end_time}")
    results = collection.find(query)
    found = False
    for doc in results:
        logging.info(doc)
        found = True
    if not found:
        logging.info("No ERROR logs found for the specified time range.")

def aggregate_log_levels(collection, target_day: datetime):
    """
    Run an aggregation pipeline to group log entries by level and count them.

    Args:
        collection: The MongoDB collection to aggregate.
        target_day (datetime): The date to filter logs for.
    """
    start_time = target_day.replace(hour=0, minute=0, second=0)
    end_time = target_day.replace(hour=23, minute=59, second=59)

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

    logging.info(f"Aggregating logs from {start_time} to {end_time}")
    results = collection.aggregate(pipeline)
    for result in results:
        logging.info(result)

def main():
    target_day = datetime(2024, 12, 24)  # Modify this date as needed

    client = connect_to_federated_mongo()
    db = client[Config.FEDERATED_DATABASE]
    collection = db[Config.FEDERATED_COLLECTION]

    query_error_logs(collection, target_day)
    aggregate_log_levels(collection, target_day)

if __name__ == "__main__":
    main()