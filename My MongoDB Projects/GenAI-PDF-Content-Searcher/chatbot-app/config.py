# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB connection details
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_DATABASE = "machine_technician_chatbot"
    MONGODB_COLLECTION = "wind_turbine_maintenance_guides"
    # OpenAI API Key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
