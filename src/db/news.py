import os

from dotenv import load_dotenv

from db.mongo_client import MongoDBClient

load_dotenv()

MAX_TICKERS = int(os.environ.get("MAX_TICKERS", 0))


def get_tickers_in_db():
    with MongoDBClient() as db:
        collection = db["ticker"]
        result = collection.find()
    return result is not None


def is_ticker_in_db(ticker: str):
    with MongoDBClient() as db:
        collection = db["ticker"]
        result = collection.find_one({"ticker": ticker})
    return result is not None


def add_ticker_to_watch(ticker: str):
    with MongoDBClient() as db:
        collection = db["ticker"]

        if is_ticker_in_db(ticker):
            raise Exception("Ticker already in the database.")

        if collection.count_documents({}) >= MAX_TICKERS:
            raise Exception(f"Max tickers reached. Limit of {MAX_TICKERS}. Watching currently: {collection.find()}")

        result = collection.insert_one({"ticker": ticker})
    return result.inserted_id


def remove_ticker_to_watch(ticker: str):
    with MongoDBClient() as db:
        collection = db["ticker"]

        if not is_ticker_in_db(ticker):
            raise Exception("Ticker not found in the database.")

        result = collection.delete_one({"ticker": ticker})
    return result.deleted_count


def is_news_in_db(url: str):
    with MongoDBClient() as db:
        collection = db["news"]
        result = collection.find_one({"url": url})
    return result is not None


def add_news_to_db(url: str):
    with MongoDBClient() as db:
        collection = db["news"]
        result = collection.insert_one(url)
    return result.inserted_id


def clear_all_data():
    with MongoDBClient() as db:
        ticker_collection = db["ticker"]
        news_collection = db["news"]

        ticker_collection.delete_many({})
        news_collection.delete_many({})
