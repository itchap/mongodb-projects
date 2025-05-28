from pymongo import MongoClient
from config import Config
from openai import OpenAI
aiClient = OpenAI()

# MongoDB connection details
client = MongoClient(Config.MONGODB_URI)
db = client[Config.MONGODB_DATABASE]
collection = db[Config.MONGODB_COLLECTION]

# Function to concatenate the specified fields
def concatenate_fields(document):
    concatenated_text = 'Sub Category: ' + document["sub_category"] + '; Product Name: ' + document["name"]+ '; Product Description: ' + document["description"] + '; Product Materials:  ' + document["material"] + '; '
    concatenated_text += 'Available Colours: ' + ' '.join(document["colors"]) + '; '
    return concatenated_text

# Function to generate vector embedding using OpenAI
def generate_embedding(text, model="text-embedding-3-large"):
   return aiClient.embeddings.create(input = [text], model=model).data[0].embedding

# Read documents, concatenate fields, generate embeddings, and update documents
for document in collection.find({'created_manually': True}):
    concatenated_text = concatenate_fields(document)
    embedding = generate_embedding(concatenated_text)
    collection.update_one({'_id': document['_id']}, {'$set': {'embeddings': embedding}})

print("Embeddings generated and updated successfully.")