# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB connection details
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_DATABASE = "system-logs"
    MONGODB_COLLECTION = "db-server-01"
    FEDERATED_URI = os.getenv("FEDERATED_MONGODB_URI")
    FEDERATED_DATABASE = "virtual-db-system-logs"
    FEDERATED_COLLECTION = "virtual-coll-db-server-01"