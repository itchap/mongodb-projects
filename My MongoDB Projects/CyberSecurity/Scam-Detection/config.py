# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB connection details
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_DATABASE = "cyberSecurity"
    MONGODB_COLLECTION = "scamMessages"
