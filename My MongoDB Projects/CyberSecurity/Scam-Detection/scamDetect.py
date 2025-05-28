import structlog
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient
from openai import OpenAI
from pymongo.errors import PyMongoError
from config import Config
import sys

# Initialize logging
logger = structlog.get_logger()

# MongoDB setup
client = MongoClient(Config.MONGODB_URI)
db = client[Config.MONGODB_DATABASE]
collection = db[Config.MONGODB_COLLECTION]

# OpenAI setup
aiClient = OpenAI()

# Embedding generator
def get_embeddings(text, model="text-embedding-3-large"):
    try:
        logger.info("Generating OpenAI embedding", input_preview=text[:30])
        embedding = aiClient.embeddings.create(input=[text], model=model).data[0].embedding
        logger.info("Embedding generated", length=len(embedding))
        return embedding
    except Exception as e:
        logger.error("Error generating embedding", error=str(e))
        raise

# Vector Search
def vector_search(query_vector):
    try:
        logger.info("Starting vector search")
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "defaultVectorIndex",
                    "path": "contextVector",
                    "queryVector": query_vector,
                    "numCandidates": 100,
                    "limit": 10
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "messageText": 1,
                    "detectedScam.type": 1,
                    "detectedScam.confidence": 1,
                    "timestamp": 1,
                    "similarityScore": {"$meta": "vectorSearchScore"}
                }
            }
        ]

        results = list(collection.aggregate(pipeline))
        logger.info("Vector search successful", result_count=len(results))
        return results

    except PyMongoError as e:
        logger.error("MongoDB vector search failed", error=str(e))
        raise
    except Exception as e:
        logger.error("Unexpected error during vector search", error=str(e))
        raise

# Main
if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print("❌ Please provide a scam message as a command-line argument.")
            print("Usage: python scam_vector_search.py \"Your account is suspended. Click here to reactivate.\"")
            sys.exit(1)

        # Join all CLI arguments into one message string
        user_input = " ".join(sys.argv[1:])
        logger.info("Processing user input", message=user_input)

        # Embed and search
        query_vector = get_embeddings(user_input)
        results = vector_search(query_vector)

        print("\nTop Similar Scam Messages:")
        for i, doc in enumerate(results, 1):
            print(f"\nResult #{i}")
            print(f"Message: {doc['messageText']}")
            print(f"Scam Type: {doc['detectedScam']['type']}")
            print(f"Confidence: {doc['detectedScam']['confidence']}")
            print(f"Timestamp: {doc['timestamp']}")
            print(f"Similarity Score: {round(doc['similarityScore'], 4)}")

    except Exception as e:
        print("❌ Error:", str(e))