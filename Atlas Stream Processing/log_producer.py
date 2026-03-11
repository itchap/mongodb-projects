from kafka import KafkaProducer
from faker import Faker
import json
import time
import random

# Setup
fake = Faker()
producer = KafkaProducer(
    bootstrap_servers='itchap.com:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC = 'logs'

# Fake log generator
def generate_log():
    return {
        "user_id": fake.uuid4(),
        "timestamp": fake.iso8601(),
        "action": random.choice(["login", "logout", "purchase", "view"]),
        "ip": fake.ipv4(),
        "device": random.choice(["mobile", "desktop", "tablet"]),
        "location": fake.country()
    }

# Main loop
print(f"Sending logs to Kafka topic '{TOPIC}'...")
try:
    while True:
        log = generate_log()
        producer.send(TOPIC, value=log)
        print("Sent:", log)
        time.sleep(1)  # 1 second between messages
except KeyboardInterrupt:
    print("\nStopped by user.")
finally:
    producer.close()