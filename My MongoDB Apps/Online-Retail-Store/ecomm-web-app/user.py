from flask import Blueprint, request, jsonify
from pymongo import MongoClient, errors
from bson import ObjectId
from config import Config
import structlog
from openai import OpenAI

# Initialize structured logging
logger = structlog.get_logger()

# Create blueprint
user_bp = Blueprint('user', __name__)

# Initialize the OpenAI client
aiClient = OpenAI()

# Connect to MongoDB
try:
    client = MongoClient(Config.MONGODB_URI)
    db = client[Config.MONGODB_DATABASE]
    collection = db[Config.MONGODB_COLLECTION]
    logger.info("Connected to MongoDB")
except errors.ConnectionError as e:
    logger.error("Could not connect to MongoDB", error=str(e))
    raise

def generate_embedding(text, model="text-embedding-3-large"):
    try:
        return aiClient.embeddings.create(input=[text], model=model).data[0].embedding
    except Exception as e:
        logger.error("Error generating embedding", error=str(e))
        raise

@user_bp.route('/fashionbot', methods=['POST'])
def fashionbot():
    try:
        data = request.json
        logger.debug("Received request data", data=data)

        product_id = data.get('product_id')
        question = data.get('question')

        if not product_id or not question:
            logger.error("Product ID and question are required")
            return jsonify({'error': 'Product ID and question are required', 'status_code': 400}), 400

        product = collection.find_one({'_id': ObjectId(product_id)}, {'embeddings': 1, 'images': 1})
        if not product or 'embeddings' not in product or 'images' not in product:
            logger.error("Product not found or missing embeddings/images")
            return jsonify({'error': 'Product not found or missing embeddings or images', 'status_code': 404}), 404

        image_url = product['images'][0]  # Assuming there's at least one image

        conversation = [
            {"role": "system", "content": "You are a helpful fashion assistant from the Zalando retail store."},
            {"role": "assistant", "content": "Include this text at the end of the message: I have listed some recommendations below for their consideration based on the image and what they asked for."},
            {"role": "user", "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]},
        ]

        completion = aiClient.chat.completions.create(
            model="gpt-4o",
            messages=conversation,
        )
        answer_content = completion.choices[0].message.content

        combined_input = f"Question: {question}\nAnswer: {answer_content}"
        question_embedding = generate_embedding(combined_input)

        search_stage = {
            "$vectorSearch": {
                "index": "vs_details",
                "queryVector": question_embedding,
                "path": "embeddings",
                "numCandidates": 50,
                "limit": 7,
            }
        }

        pipeline = [
            search_stage,
            {'$match': {'_id': {'$ne': ObjectId(product_id)}}},
            {'$project': {
                'name': 1,
                'price': 1,
                'description': 1,
                'brand': 1,
                'main_category': 1,
                'sub_category': 1,
                'images': 1,
                'sponsored': 1,
                'on_sale': 1,
                'created_manually': 1,
                'score': {'$meta': 'searchScore'}
            }}
        ]

        results = collection.aggregate(pipeline)
        recommendations = list(results)

        for recommendation in recommendations:
            recommendation['_id'] = str(recommendation['_id'])

        logger.debug("Answer content", answer_content=answer_content)
        logger.debug("Recommendations", recommendations=recommendations)

        return jsonify({'answer': answer_content, 'recommendations': recommendations})
    except Exception as e:
        logger.error("General Error", error=str(e))
        return jsonify({'error': 'An unexpected error occurred. Please try again later.', 'status_code': 500}), 500

@user_bp.route('/autocomplete', methods=['GET'])
def autocomplete():
    try:
        search_query = request.args.get('q', '')
        if not search_query:
            return jsonify([])

        pipeline = [
            {
                '$search': {
                    'index': 'name_ac',
                    'autocomplete': {
                        'query': search_query,
                        'path': 'name',
                        'fuzzy': {'maxEdits': 1}
                    }
                }
            },
            {'$limit': 5},
            {'$project': {
                '_id': 1,
                'name': 1
            }}
        ]

        results = collection.aggregate(pipeline)
        suggestions = [{'id': str(result['_id']), 'name': result['name']} for result in results]
        return jsonify(suggestions)
    except Exception as e:
        logger.error("Error fetching autocomplete suggestions", error=str(e))
        return jsonify({'error': str(e), 'message': 'An error occurred while fetching autocomplete suggestions', 'status_code': 500}), 500