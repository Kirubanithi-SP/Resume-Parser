# /backend/database.py

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

# Global client variable
client = None
db = None

def init_db():
    """Initializes the MongoDB connection using pymongo."""
    global client, db
    mongo_uri = os.getenv('MONGO_URI')
    if not mongo_uri:
        raise ValueError("MONGO_URI not found in environment variables.")

    try:
        print("Attempting to connect to MongoDB...")
        client = MongoClient(mongo_uri)
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        print("MongoDB connection successful.")
        # Extract database name from URI or set a default
        # Simple parsing, might need adjustment for complex URIs
        db_name = mongo_uri.split('/')[-1].split('?')[0]
        if not db_name:
            db_name = 'resume_parser_db' # Default DB name if not in URI
            print(f"Database name not found in URI, using default: {db_name}")
        db = client[db_name]
        print(f"Using database: {db_name}")

    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        raise
    except Exception as e:
        print(f"An error occurred during DB initialization: {e}")
        raise

def get_db():
    """Returns the database instance."""
    if db is None:
        # This might happen if accessed before init_db is called or if init failed
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return db

def close_db_connection():
    """Closes the MongoDB connection."""
    global client
    if client:
        print("Closing MongoDB connection.")
        client.close()