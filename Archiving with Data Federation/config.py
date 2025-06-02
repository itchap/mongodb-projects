# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB connection details
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_DATABASE = "system-logs"
    MONGODB_COLLECTION = "db-server-01"