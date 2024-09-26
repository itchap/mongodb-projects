# config.py
import os

class Config:
    # MongoDB connection details
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_DATABASE = "retail_store"
    MONGODB_COLLECTION = "products"