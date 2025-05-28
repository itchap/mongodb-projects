# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB connection details
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_DATABASE = "retail_store"
    MONGODB_COLLECTION = "products"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
