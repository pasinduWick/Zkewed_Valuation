# test_mongodb_connection.py
from pymongo import MongoClient
import ssl

uri = "mongodb+srv://zkewed:zkewed123A@vehicalevaluation.d9ufa.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

try:
    client.admin.command('ping')
    print("MongoDB connection successful!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
