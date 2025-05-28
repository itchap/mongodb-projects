import random
import string
import datetime
from pymongo import MongoClient
from config import Config

# Connect to MongoDB
client = MongoClient(Config.MONGODB_URI)
db = client[Config.MONGODB_DATABASE]
collection = db[Config.MONGODB_COLLECTION]

# Sample data for attributes
categories = {
    'Women': {
        'Clothing': ['Dresses', 'T-shirts & tops', 'Trousers', 'Jeans', 'Shirts & Blouses', 'Jackets & Blazers', 'Sweatshirts & Hoodies', 'Skirts', 'Coats'],
        'Shoes': ['Sneakers', 'Sandals', 'Pumps', 'High heels', 'Flat shoes', 'Mules', 'Ankle boots', 'Ballerinas', 'Boots', 'Sports shoes', 'Beach shoes', 'Bridal shoes', 'House Shoes', 'Outdoor shoes'],
        'Accessories': ['Bags & cases', 'Jewellery', 'Sunglasses', 'Hats & headscarves', 'Belts', 'Watches', 'Wallets & card holders', 'Scarves', 'Blue-light glasses', 'Gloves', 'Umbrellas']
    },
    'Men': {
        'Clothing': ['T-shirts & Polos', 'Shirts', 'Sweatshirts & Hoodies', 'Trousers', 'Jeans', 'Shorts', 'Jackets', 'Suits & Tailoring', 'Coats'],
        'Shoes': ['Sneakers', 'Open shoes', 'Lace-up shoes', 'Loafers', 'Business shoes', 'Boots', 'Sports shoes', 'Outdoor shoes', 'Slippers'],
        'Accessories': ['Bags & cases', 'Jewellery', 'Sunglasses', 'Hats & headscarves', 'Belts', 'Watches', 'Wallets & card holders', 'Scarves', 'Blue-light glasses', 'Gloves', 'Umbrellas']
    }
}

brands = {
    'Men': ['Carhartt', 'Polo Ralph Lauren', 'Armani', 'Calvin Klein', 'Diesel', 'G-Star', 'GAP', 'Helly Hansen', 'Hugo Boss', 'Lacoste', 'Levi\'s', 'Ted Baker', 'The North Face', 'Timberland', 'Tommy Hilfiger'],
    'Women': ['Anna Field', 'Levi\'s®', 'The North Face', 'Hoka', 'Rapha', 'Ciele', 'Polo Ralph Lauren', 'ARKET', 'Missoni', 'Proenza Schouler', 'The Kooples', 'MM6 Maison Margiela']
}

designer_brands = {
    'Men': ['Dolce&Gabbana', 'Mont Blanc', 'Paul Smith', 'Prada', 'rag & bone', 'Versace', 'Vivienne Westwood'],
    'Women': ['Alexander McQueen', 'Gucci', 'Loren Stewart', 'Victoria Beckham', 'Vivienne Westwood']
}

materials = ['Cashmere', 'Chiffon', 'Cord', 'Cotton', 'Denim', 'Fleece', 'Leather', 'Lace', 'Linen', 'Polyester', 'Satin', 'Silk', 'Synthetic', 'Wool']

conditions = ['Average', 'Good', 'Great', 'Like New', 'New']

# Function to generate a random SKU
def generate_sku():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Function to generate a random date within the last 6 months
def generate_random_date():
    now = datetime.datetime.now()
    six_months_ago = now - datetime.timedelta(days=6*30)
    return six_months_ago + datetime.timedelta(seconds=random.randint(0, int((now - six_months_ago).total_seconds())))

# Function to generate a random review
def generate_review():
    return {
        'author': f"user{random.randint(1000, 9999)}",
        'comment': 'This is a sample review.',
        'date': generate_random_date(),
        'rating': random.randint(1, 5)
    }

# Function to generate a random product
def generate_product(gender, main_category, sub_category):
    brand = random.choice(brands[gender] + designer_brands[gender])
    is_designer = brand in designer_brands[gender]
    pre_owned = random.choice([True, False])
    created_at = generate_random_date()
    updated_at = generate_random_date()

    product = {
        'gender': gender,
        'main_category': main_category,
        'sub_category': sub_category,
        'sku': generate_sku(),
        'name': f"{brand} Product {random.randint(1000, 9999)}",
        'price': round(random.uniform(10, 500), 2),
        'description': f"A high-quality {sub_category.lower()} from {brand}.",
        'sizes': random.sample(['XS', 'S', 'M', 'L', 'XL'], random.randint(1, 5)),
        'colors': random.sample(['Red', 'Blue', 'Green', 'Yellow', 'Orange', 'Purple', 'Pink', 'Brown', 'Black', 'Grey', 'White'], random.randint(1, 5)),
        'brand': brand,
        'designer': is_designer,
        'material': random.choice(materials),
        'images': [f"https://img.freepik.com/free-vector/summer-clothes-set_74855-446.jpg" for _ in range(random.randint(1, 3))],
        'stock': random.randint(1, 100),
        'availability': 'In Stock' if random.random() > 0.1 else 'Out of Stock',
        'rating': round(random.uniform(1, 5), 1),
        'reviews': [generate_review() for _ in range(random.randint(0, 10))],
        'on_sale': random.choice([True, False]),
        'pre_owned': pre_owned,
        'condition': random.choice(conditions) if pre_owned else None,
        'sponsored': random.choice([True, False]),
        'new_in': random.choice([True, False]),
        'created_at': created_at,
        'updated_at': updated_at
    }
    return product

# Generate and insert 1000 products for each gender and category
products = []
for gender in ['Men', 'Women']:
    for main_category in categories[gender]:
        for sub_category in categories[gender][main_category]:
            for _ in range(1000):
                products.append(generate_product(gender, main_category, sub_category))

collection.insert_many(products)

print("Inserted products into the MongoDB collection.")
