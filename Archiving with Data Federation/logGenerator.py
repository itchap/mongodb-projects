import argparse
import datetime
import logging
import random
from dateutil.relativedelta import relativedelta
from pymongo import MongoClient, errors
from config import Config

# Configure logging: INFO for user-facing messages, DEBUG for development/troubleshooting
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def generate_random_timestamp() -> datetime.datetime:
    """
    Generate a random datetime within the past 6 months.

    Returns:
        datetime.datetime: A random timestamp between now and 6 months ago.
    """
    now = datetime.datetime.now()
    six_months_ago = now - relativedelta(months=6)
    random_epoch = random.uniform(six_months_ago.timestamp(), now.timestamp())
    return datetime.datetime.fromtimestamp(random_epoch)

def generate_system_log() -> dict:
    """
    Generate a simulated system log with a random log level, message, and timestamp.

    Returns:
        dict: A dictionary representing a synthetic system log entry.
    """
    log_levels = ["INFO", "WARNING", "ERROR"]
    log_messages = [
        "System startup",
        "Database connection established",
        "User login failed",
        "Insufficient disk space",
        "Network connection lost",
        "Critical error occurred"
    ]

    return {
        "level": random.choice(log_levels),
        "message": random.choice(log_messages),
        "timestamp": generate_random_timestamp()
    }

def insert_logs(collection, num_logs: int) -> None:
    """
    Insert a specified number of randomly generated logs into a MongoDB collection.

    Args:
        collection: The MongoDB collection object to insert into.
        num_logs (int): Number of log entries to generate and insert.
    """
    logging.info(f"Inserting {num_logs} system logs...")
    for i in range(1, num_logs + 1):
        log_entry = generate_system_log()
        try:
            collection.insert_one(log_entry)
            logging.debug(f"[{i}/{num_logs}] Inserted log: {log_entry}")
        except errors.PyMongoError as e:
            logging.error(f"Error inserting log #{i}: {e}")
    logging.info("All log entries inserted.")

def parse_arguments() -> int:
    """
    Parse the number of logs to insert from command-line arguments.

    Returns:
        int: Number of logs to insert (default: 10).
    """
    parser = argparse.ArgumentParser(description="Insert synthetic system logs into MongoDB.")
    parser.add_argument(
        "num_logs",
        type=int,
        nargs="?",
        default=10,
        help="Number of logs to insert (default: 10)"
    )
    return parser.parse_args().num_logs

def get_mongo_collection() -> object:
    """
    Connect to MongoDB and return the target collection.

    Returns:
        Collection: A MongoDB collection object ready for data insertion.
    """
    try:
        client = MongoClient(Config.MONGODB_URI)
        client.admin.command("ping")  # Ensure the connection is active
        logging.info("Connected to MongoDB successfully.")
        return client[Config.MONGODB_DATABASE][Config.MONGODB_COLLECTION]
    except errors.ConnectionFailure as e:
        logging.error(f"Could not connect to MongoDB: {e}")
        raise SystemExit("Terminating script due to MongoDB connection failure.")

def main() -> None:
    """
    Main script logic:
    - Parse arguments
    - Connect to MongoDB
    - Insert generated logs
    """
    num_logs = parse_arguments()
    collection = get_mongo_collection()
    insert_logs(collection, num_logs)

if __name__ == "__main__":
    main()