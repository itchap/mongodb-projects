from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime
from config import Config

# MongoDB connection
client = MongoClient(Config.MONGODB_URI)
db = client[Config.MONGODB_DATABASE]

fake = Faker()

# Clear existing data
for collection in ["devices", "users", "vulnerabilities", "threat_actors", "domains"]:
    db[collection].drop()

# --- Generate Users ---
users = []
for _ in range(10):
    user = {
        "username": fake.user_name(),
        "email": fake.email(),
        "department": random.choice(["Engineering", "Finance", "HR", "Security"]),
        "devices": [],
        "roles": random.sample(["admin", "dev", "user", "analyst"], k=2)
    }
    users.append(user)
user_ids = db.users.insert_many(users).inserted_ids

# --- Generate Vulnerabilities ---
vulns = []
for i in range(10):
    vuln = {
        "cveId": f"CVE-2024-{random.randint(1000, 9999)}",
        "severity": random.choice(["low", "medium", "high", "critical"]),
        "description": fake.sentence(),
        "exploitedBy": [],
        "patched": random.choice([True, False])
    }
    vulns.append(vuln)
vuln_ids = db.vulnerabilities.insert_many(vulns).inserted_ids

# --- Generate Threat Actors ---
actors = []
for name in ["APT29", "Lazarus Group", "Conti", "FIN7"]:
    actor = {
        "name": name,
        "aliases": [f"{name}_alias"],
        "knownExploits": random.sample(vuln_ids, k=2),
        "campaigns": [fake.bs(), fake.bs()],
        "tags": random.sample(["state-sponsored", "APT", "ransomware"], k=2)
    }
    actors.append(actor)
actor_ids = db.threat_actors.insert_many(actors).inserted_ids

# Link threat actors to vulnerabilities
for vuln_id in vuln_ids:
    actor = random.choice(actor_ids)
    db.vulnerabilities.update_one(
        {"_id": vuln_id},
        {"$addToSet": {"exploitedBy": actor}}
    )

# --- Generate Devices ---
devices = []
for i in range(20):
    owner_id = random.choice(user_ids)
    device = {
        "hostname": fake.hostname(),
        "ip": fake.ipv4(),
        "os": random.choice(["Windows 10", "macOS", "Ubuntu 20.04"]),
        "owner": {"type": "user", "id": owner_id},
        "vulnerabilities": random.sample(vuln_ids, k=random.randint(1, 3)),
        "tags": random.sample(["internal", "dmz", "laptop", "server"], k=2),
        "lastSeen": datetime.utcnow()
    }
    devices.append(device)

device_ids = db.devices.insert_many(devices).inserted_ids

# Update users with device links
for device in devices:
    db.users.update_one(
        {"_id": device["owner"]["id"]},
        {"$addToSet": {"devices": device["_id"]}}
    )

# --- Generate Domains ---
domains = []
for _ in range(8):
    domain = {
        "domainName": fake.domain_name(),
        "resolvedIPs": [fake.ipv4(), fake.ipv4()],
        "associatedThreatActors": random.sample(actor_ids, k=1),
        "relatedDevices": random.sample(device_ids, k=2)
    }
    domains.append(domain)
db.domains.insert_many(domains)

print("✅ Sample data inserted.")