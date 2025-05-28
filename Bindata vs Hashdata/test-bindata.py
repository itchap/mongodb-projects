# Common Imports
import hashlib
import random
import string
from pymongo import MongoClient
from bson.binary import Binary
import datetime

# Connect to MongoDB
client = MongoClient('mongodb+srv://itchap:NokiaN900@democluster.0wrhw.mongodb.net/?retryWrites=true&w=majority&appName=BinDataCluster2')

db = client['test_db']
collection_binary = db['pii_hashed_bindata']
collection_binary.drop()  # Clean up existing data if re-running

def generate_random_pii():
    """Generates random PII data."""
    email = ''.join(random.choices(string.ascii_lowercase, k=7)) + '@example.com'
    name = ''.join(random.choices(string.ascii_lowercase, k=10)).capitalize()
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    dob = datetime.date(1970 + random.randint(0, 30), random.randint(1, 12), random.randint(1, 28))
    ssn = ''.join(random.choices(string.digits, k=9))
    credit_card = ''.join(random.choices(string.digits, k=16))
    return email, name, password, dob.isoformat(), ssn, credit_card

def hash_pii_as_binary(data):
    """Hashes PII fields and stores them as binary data."""
    hashed_data = {}
    for field, value in data.items():
        hashed_data[field] = Binary(hashlib.sha256(value.encode()).digest())
    return hashed_data

# Insert 10 million records
batch_size = 1000
for _ in range(10000):  # 10 million / 1000 = 10,000 batches
    docs = []
    for _ in range(batch_size):
        email, name, password, dob, ssn, credit_card = generate_random_pii()
        data = {
            'email': email,
            'name': name,
            'password': password,
            'dob': dob,
            'ssn': ssn,
            'credit_card': credit_card
        }
        hashed_data = hash_pii_as_binary(data)
        docs.append(hashed_data)
    collection_binary.insert_many(docs)
print("Inserted 10 million records with hashed PII as binary data.")
