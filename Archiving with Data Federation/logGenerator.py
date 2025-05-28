import argparse
import datetime
import logging
import random
from dateutil.relativedelta import relativedelta
from pymongo import MongoClient, errors
from config import Config

# Configure logging to provide useful timestamped output for monitoring and debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# def connect_to_mongodb(uri: str) -> MongoClient:
#     """
#     Establish a connection to MongoDB using the provided URI.
#     Args:
#         uri (str): MongoDB connection URI.
#     Returns:
#         MongoClient: A connected MongoClient instance.
#     Raises:
#         ConnectionFailure: If unable to connect to MongoDB.
#     """
#     try:
#         client = MongoClient(uri)
#         # The following line triggers a connection attempt
#         client.admin.command("ping")
#         logging.info("Connected to MongoDB successfully.")
#         return client
#     except errors.ConnectionFailure as e:
#         logging.error(f"Failed to connect to MongoDB: {e}")
#         raise

def generate_random_timestamp() -> datetime.datetime:
    """
    Generate a random timestamp within the past 6 months.
    Returns:
        datetime.datetime: A randomly generated timestamp.
    """
    current_time = datetime.datetime.now()
    six_months_ago = current_time - relativedelta(months=6)
    random_ts = random.uniform(six_months_ago.timestamp(), current_time.timestamp())
    return datetime.datetime.fromtimestamp(random_ts)

def generate_system_log() -> dict:
    """
    Generate a random system log entry containing a severity level, message, and timestamp.
    Returns:
        dict: A dictionary representing a simulated system log.
    """
    log_levels = ["INFO", "WARNING", "ERROR"]
    log_messages = [
        "System startup",
        "Database connection established",
        "User login failed",
        "Insufficient disk space",
        "Network connection lost",
        "Critical error occurred",
    ]

    log = {
        "level": random.choice(log_levels),
        "message": random.choice(log_messages),
        "timestamp": generate_random_timestamp()
    }

    return log

def insert_logs(collection, num_logs: int) -> None:
    """
    Insert a specified number of randomly generated logs into a MongoDB collection.
    Args:
        collection: A pymongo Collection instance to insert documents into.
        num_logs (int): Number of log documents to insert.
    """
    for i in range(num_logs):
        log = generate_system_log()
        try:
            collection.insert_one(log)
            logging.debug(f"[{i+1}/{num_logs}] Inserted log: {log}")
        except errors.PyMongoError as e:
            logging.error(f"Failed to insert log: {e}")

def parse_arguments() -> int:
    """
    Parse command-line arguments to determine how many logs to insert.
    Returns:
        int: Number of logs to insert (default is 10 if not provided).
    """
    parser = argparse.ArgumentParser(description="Insert sample system logs into MongoDB.")
    parser.add_argument(
        "num_logs",
        type=int,
        nargs="?",
        default=10,
        help="Number of logs to insert (default: 10)"
    )
    args = parser.parse_args()
    return args.num_logs

def main() -> None:
    """
    Main entry point of the script. Connects to MongoDB and inserts logs based on user input.
    """
    num_logs = parse_arguments()

    # Connect to MongoDB using credentials and parameters from the external config
    client = MongoClient(Config.MONGODB_URI)  # Use MongoDB URI from config
    db = client[Config.MONGODB_DATABASE]
    collection = db[Config.MONGODB_COLLECTION]

    logging.info(f"Starting to insert {num_logs} logs into '{Config.MONGODB_COLLECTION}' collection.")
    insert_logs(collection, num_logs)
    logging.info("Log insertion complete.")

if __name__ == "__main__":
    main()