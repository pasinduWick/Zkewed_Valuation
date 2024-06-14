import pymongo
from pymongo import MongoClient
import ssl

uri = "mongodb+srv://zkewed:zkewed123A@vehicalevaluation.d9ufa.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(uri, tlsAllowInvalidCertificates=True)
    db = client['userDetails']
    # Attempt a connection
    client.admin.command('ping')
    print("MongoDB connection successful.")
except pymongo.errors.ConnectionError as e:
    print(f"Connection failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
