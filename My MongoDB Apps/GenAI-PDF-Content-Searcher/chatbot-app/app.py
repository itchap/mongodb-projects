import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import PyPDF2
import structlog
import hashlib
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from config import Config
from openai import OpenAI

# Initialize OpenAI client
aiClient = OpenAI()

# Initialize structured logging
logger = structlog.get_logger()

# Create a Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'  # Folder to store uploaded PDFs

# MongoDB connection setup
client = MongoClient(Config.MONGODB_URI)  # Use MongoDB URI from config
db = client[Config.MONGODB_DATABASE]      # Select the database
collection = db[Config.MONGODB_COLLECTION] # Select the collection

# Function to extract text from a PDF
def extract_pdf_content(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)  # Initialize PDF reader
            text = ""
            # Loop through all pages and extract text
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text  # Return the entire extracted text
    except Exception as e:
        logger.error("Error extracting PDF content", error=str(e), pdf_path=pdf_path)  # Log any errors during extraction
        raise

# Function to split the extracted text into chunks for easier processing
def split_text(text, chunk_size=500):
    words = text.split()  # Split the text into individual words
    # Create a list of chunks, each containing 'chunk_size' words
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# Function to get embeddings from OpenAI API for the given text input
def get_embeddings(text, model="text-embedding-3-large"):
    try:
        logger.info("Generating text embeddings")  # Log the text being processed
        embedding = aiClient.embeddings.create(input=[text], model=model).data[0].embedding
        logger.info("Embedding generated successfully", embedding_length=len(embedding))  # Log success and embedding size
        return embedding
    except Exception as e:
        logger.error("Error generating embedding", error=str(e), text=text)  # Log any errors during embedding generation
        raise

# Function to store the text chunks and their embeddings in MongoDB
def store_chunks_in_mongo(pdf_id, chunks):
    for i, chunk in enumerate(chunks):
        try:
            # Generate embedding for each chunk
            embedding = get_embeddings(chunk)
            # Create a document with the chunk's data and embedding
            document = {
                "pdf_id": pdf_id,
                "chunk_id": i,
                "content": chunk,
                "embedding": embedding
            }
            # Insert the document into MongoDB
            collection.insert_one(document)
            logger.info(f"Stored chunk {i} in MongoDB", chunk_id=i, pdf_id=pdf_id)  # Log success
        except PyMongoError as e:
            logger.error(f"Error storing chunk {i} in MongoDB", chunk_id=i, pdf_id=pdf_id, error=str(e))  # Log any MongoDB errors
            raise

# Main function to handle the entire PDF processing flow
def process_pdf(pdf_path, pdf_id):
    try:
        # Step 1: Extract text from the PDF
        logger.info("Extracting text from PDF...", pdf_id=pdf_id)
        pdf_text = extract_pdf_content(pdf_path)

        # Step 2: Split the text into smaller chunks
        logger.info("Splitting text into chunks...", pdf_id=pdf_id)
        chunks = split_text(pdf_text, chunk_size=500)  # Adjust the chunk size as necessary

        # Step 3: Store each chunk and its embedding in MongoDB
        logger.info("Storing chunks and embeddings in MongoDB...", pdf_id=pdf_id)
        store_chunks_in_mongo(pdf_id, chunks)

        # Log completion of processing
        logger.info("Processing complete!", pdf_id=pdf_id)
    except Exception as e:
        # Log any errors that occur during the process
        logger.error(f"Failed to process PDF: {pdf_id}", error=str(e))

# Function to query MongoDB vector search index using the question's embedding
def vector_search(question_embedding):
    try:
        logger.info("Starting vector search")  # Log the beginning of the vector search process
        query = {
            "$vectorSearch": {
                "index": "wt_pdf_embedding",  # Vector index for MongoDB
                "queryVector": question_embedding,  # Use the generated embedding for the search
                "path": "embedding",  # Path to the vector data in MongoDB
                "numCandidates": 50,  # Max number of candidates for the search
                "limit": 12,          # Return the top 10 results
            }
        }
        pipeline = [
            query,  # Perform the vector search
            {'$project': {
                'content': 1,  # Only project the content field from MongoDB
                '_id': 0       # Exclude the MongoDB ID field from the results
            }}
        ]
        results = collection.aggregate(pipeline)  # Execute the search query on MongoDB
        results_list = list(results)  # Convert the cursor to a list
        logger.info("Vector search successful", result_count=len(results_list))  # Log the number of search results
        return results_list
    except PyMongoError as e:
        logger.error("MongoDB error during vector search", error=str(e))  # Log MongoDB-specific errors
        raise
    except Exception as e:
        logger.error("Unexpected error during vector search", error=str(e))  # Log any other unexpected errors
        raise

# Function to get a ChatGPT response by providing the user's query and search results as context
def generate_chatgpt_response(query, context_documents):
    try:
        # Combine all content from search results into a single context string
        context = " ".join([doc['content'] for doc in context_documents])
        logger.info("Generating ChatGPT response", context_length=len(context_documents))  # Log context information

        # If no context was found, return a fallback response
        if not context.strip():
            return "I don't have enough information based on the provided context."

        # Define a conversation for ChatGPT to process
        conversation = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant for onsite mining hardware/machines technicians. To reduce hallucinations, you must use the information "
                    "contained in the context provided to answer the user's questions. Be as descriptive as possible."
                )
            },
            {"role": "assistant", "content": context},
            {"role": "user", "content": query},
        ]

        # Get a response from the ChatGPT model
        completion = aiClient.chat.completions.create(
            model="gpt-4o",  # Use the GPT-4o model
            messages=conversation
        )
        answer_content = completion.choices[0].message.content  # Extract the answer content
        logger.info("ChatGPT response generated successfully")  # Log successful response generation
        return answer_content
    except Exception as e:
        logger.error("Error generating chat response", error=str(e), query=query)  # Log any errors during ChatGPT processing
        raise

# Route to serve the chatbot's front-end HTML page
@app.route("/")
def index():
    logger.info("Serving the chatbot front-end")  # Log when the front-end is served
    return render_template("index.html")  # Render the HTML template for the chatbot UI

# Route to handle PDF upload and vectorization
@app.route("/upload", methods=["POST"])
def upload_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Save the uploaded PDF
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Generate a unique PDF ID using SHA-256
        hash_object = hashlib.sha256(filename.encode())
        pdf_id = hash_object.hexdigest()

        # Process the uploaded PDF
        process_pdf(filepath, pdf_id)

        return jsonify({"message": "PDF uploaded and processed successfully!"}), 200
    except Exception as e:
        logger.error("Error uploading or processing PDF", error=str(e))
        return jsonify({"error": "Failed to upload or process the PDF"}), 500


# API route for receiving a question and responding via ChatGPT
@app.route("/ask", methods=["POST"])
def ask_question():
    try:
        # Extract the user's question from the POST request
        data = request.get_json()
        question = data.get("question")

        logger.info("Received question", question=question)  # Log the received question

        # Step 1: Generate an embedding from the user's question
        logger.info("Vectorizing the question", question=question)
        question_embedding = get_embeddings(question)

        # Step 2: Perform a vector search on MongoDB to retrieve relevant context documents
        logger.info("Performing vector search", embedding_length=len(question_embedding))
        search_results = vector_search(question_embedding)

        # Step 3: Generate a ChatGPT response based on the retrieved context and the user's query
        logger.info("Generating ChatGPT response", results_found=len(search_results))
        answer = generate_chatgpt_response(question, search_results)

        return jsonify({"question": question, "answer": answer}), 200  # Return the original question and generated answer as JSON

    # Handle MongoDB-related errors
    except PyMongoError as e:
        logger.error("MongoDB error in chatbot flow", error=str(e))
        return jsonify({"error": "Database error occurred, please try again later"}), 500

    # Handle other unexpected errors
    except Exception as e:
        logger.error("Error in chatbot flow", error=str(e))
        return jsonify({"error": "Something went wrong"}), 500

# Run the Flask web app on port 8000
if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host="0.0.0.0", port=8000, debug=True)               # The app will be accessible on port 8000