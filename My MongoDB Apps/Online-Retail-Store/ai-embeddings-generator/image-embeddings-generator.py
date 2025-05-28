from pymongo import MongoClient
from config import Config
import requests
from PIL import Image
from io import BytesIO
import torch
from transformers import CLIPProcessor, CLIPModel

# MongoDB connection details
client = MongoClient(Config.MONGODB_URI)
db = client[Config.MONGODB_DATABASE]
collection = db[Config.MONGODB_COLLECTION]

# Initialize CLIP model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Function to download and open an image from a URL
def download_image(url):
    response = requests.get(url)
    try:
        img = Image.open(BytesIO(response.content))
        img.verify()  # Verify the image file integrity
        img = Image.open(BytesIO(response.content))  # Reopen image after verify to reset file pointer
        # Convert image to RGBA if it has a palette with transparency
        if img.mode == 'P' and 'transparency' in img.info:
            img = img.convert('RGBA')
    except (IOError, SyntaxError) as e:
        print(f"Error processing image {url}: {e}")
        return None
    return img

# Function to generate image embedding using CLIP
def generate_image_embedding(image):
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        embeddings = model.get_image_features(**inputs)
    return embeddings.squeeze().tolist()

# Read documents, download images, generate embeddings, and update documents
for document in collection.find({'created_manually': True}):
    image_embeddings = []
    for image_url in document.get("images", []):
        try:
            image = download_image(image_url)
            if image is not None:
                embedding = generate_image_embedding(image)
                image_embeddings.append(embedding)
        except Exception as e:
            print(f"Error processing image {image_url}: {e}")
            continue
    collection.update_one({'_id': document['_id']}, {'$set': {'image_embeddings': image_embeddings}})

print("Image embeddings generated and updated successfully.")
