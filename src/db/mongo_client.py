import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


def get_mongo_client():
    try:
        mongo_uri = os.getenv("MONGO_URI")

        if not mongo_uri:
            raise ValueError("MONGO_URI not found in the .env file.")

        client = MongoClient(mongo_uri)
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


class MongoDBClient:
    def __enter__(self):
        self.client = get_mongo_client()
        self.db = self.client["news-predicter"]
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()