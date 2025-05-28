from flask import Blueprint, request, jsonify
from pymongo import MongoClient, errors
from bson import ObjectId
from config import Config
import structlog

# Initialize structured logging
logger = structlog.get_logger()

# Create blueprint
products_bp = Blueprint('products', __name__)

# Connect to MongoDB
try:
    client = MongoClient(Config.MONGODB_URI)
    db = client[Config.MONGODB_DATABASE]
    collection = db[Config.MONGODB_COLLECTION]
    logger.info("Connected to MongoDB")
except errors.ConnectionError as e:
    logger.error("Could not connect to MongoDB", error=str(e))
    raise

@products_bp.route('/products', methods=['GET'])
def get_products():
    try:
        search_query = request.args.get('q', '')
        filter_category = request.args.get('category', '')
        filter_sub_category = request.args.get('sub_category', '')
        filter_gender = request.args.get('gender', '')
        filter_brand = request.args.get('brand', '')
        filter_on_sale = request.args.get('on_sale', 'false') == 'true'
        page = int(request.args.get('page', 1))
        limit = 12
        skip = (page - 1) * limit

        must_clauses = []
        should_clauses = []

        if search_query:
            must_clauses.append({
                'text': {
                    'query': search_query,
                    'path': ['name', 'description', 'brand', 'sub_category', 'material', 'colors'],
                    "fuzzy": {"maxEdits": 2, "prefixLength": 3}
                }
            })

        if filter_category:
            must_clauses.append({
                'text': {
                    'query': filter_category,
                    'path': 'main_category'
                }
            })

        if filter_sub_category:
            must_clauses.append({
                'text': {
                    'query': filter_sub_category,
                    'path': 'sub_category'
                }
            })

        if filter_gender:
            must_clauses.append({
                'text': {
                    'query': filter_gender,
                    'path': 'gender'
                }
            })

        if filter_brand:
            must_clauses.append({
                'text': {
                    'query': filter_brand,
                    'path': 'brand'
                }
            })

        if filter_on_sale:
            must_clauses.append({
                'equals': {
                    'value': True,
                    'path': 'on_sale'
                }
            })

        if search_query or filter_category or filter_sub_category or filter_gender or filter_brand or filter_on_sale:
            should_clauses.append({
                "equals": {
                    "value": True,
                    "path": "sponsored",
                    "score": {"boost": {"value": 3}}
                }
            })

        pipeline = []

        if must_clauses or should_clauses:
            pipeline.append({
                '$search': {
                    'index': 'default',
                    'compound': {
                        'must': must_clauses,
                        'should': should_clauses
                    }
                }
            })
        else:
            pipeline.append({'$match': {'created_manually': True}})

        pipeline.extend([
            {'$sort': {'sponsored': -1}},
            {'$skip': skip},
            {'$limit': limit},
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
        ])

        results = collection.aggregate(pipeline)
        products = list(results)

        count_pipeline = [pipeline[0], {'$count': 'total'}] if (must_clauses or should_clauses) else [{'$match': {'created_manually': True}}, {'$count': 'total'}]
        total_result = list(collection.aggregate(count_pipeline))

        total_products = total_result[0]['total'] if total_result else 0

        for product in products:
            product['_id'] = str(product['_id'])

        total_pages = (total_products + limit - 1) // limit

        return jsonify({
            'products': products,
            'total_pages': total_pages,
            'current_page': page,
            'total_products': total_products
        })
    except Exception as e:
        logger.error("Error fetching products", error=str(e))
        return jsonify({'error': str(e), 'message': 'An error occurred while fetching products', 'status_code': 500}), 500

@products_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = collection.find_one({'_id': ObjectId(product_id)})
        if product:
            product['_id'] = str(product['_id'])
            return jsonify(product)
        else:
            return jsonify({'error': 'Product not found', 'message': 'The product with the specified ID does not exist', 'status_code': 404}), 404
    except Exception as e:
        logger.error("Error fetching product", error=str(e))
        return jsonify({'error': str(e), 'message': 'An error occurred while fetching the product', 'status_code': 500}), 500

@products_bp.route('/products', methods=['POST'])
def add_product():
    try:
        data = request.json
        data['created_manually'] = True
        result = collection.insert_one(data)
        return jsonify({'message': 'Product added', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        logger.error("Error adding product", error=str(e))
        return jsonify({'error': str(e), 'message': 'An error occurred while adding the product', 'status_code': 500}), 500

@products_bp.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        data = request.json
        result = collection.update_one({'_id': ObjectId(product_id)}, {'$set': data})
        if result.matched_count:
            return jsonify({'message': 'Product updated'})
        else:
            return jsonify({'error': 'Product not found', 'message': 'The product with the specified ID does not exist', 'status_code': 404}), 404
    except Exception as e:
        logger.error("Error updating product", error=str(e))
        return jsonify({'error': str(e), 'message': 'An error occurred while updating the product', 'status_code': 500}), 500

@products_bp.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        result = collection.delete_one({'_id': ObjectId(product_id)})
        if result.deleted_count:
            return jsonify({'message': 'Product deleted'})
        else:
            return jsonify({'error': 'Product not found', 'message': 'The product with the specified ID does not exist', 'status_code': 404}), 404
    except Exception as e:
        logger.error("Error deleting product", error=str(e))
        return jsonify({'error': str(e), 'message': 'An error occurred while deleting the product', 'status_code': 500}), 500

@products_bp.route('/products', methods=['DELETE'])
def delete_products():
    try:
        filter_query = request.json.get('filter', {})
        result = collection.delete_many(filter_query)
        return jsonify({'message': f'{result.deleted_count} products deleted'})
    except Exception as e:
        logger.error("Error deleting products", error=str(e))
        return jsonify({'error': str(e), 'message': 'An error occurred while deleting the products', 'status_code': 500}), 500

@products_bp.route('/products/<product_id>/recommendations', methods=['GET'])
def get_recommendations(product_id):
    try:
        product = collection.find_one({'_id': ObjectId(product_id)}, {'embeddings': 1})
        if not product or 'embeddings' not in product:
            return jsonify({'error': 'Product not found or missing embeddings', 'message': 'The product with the specified ID does not exist or is missing embeddings', 'status_code': 404}), 404

        embeddings = product['embeddings']

        search_stage = {
            "$vectorSearch": {
                "index": "vs_details",
                "queryVector": embeddings,
                "path": "embeddings",
                "numCandidates": 50,
                "limit": 10,
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

        return jsonify(recommendations)
    except Exception as e:
        logger.error("Error fetching recommendations", error=str(e))
        return jsonify({'error': str(e), 'message': 'An error occurred while fetching recommendations', 'status_code': 500}), 500