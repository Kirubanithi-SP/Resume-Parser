# /backend/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'a_default_secret_key_for_dev') # Flask still uses SECRET_KEY for sessions etc.
    MONGO_URI = os.getenv('MONGO_URI')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')

    # Ensure critical variables are set
    if not MONGO_URI:
        raise ValueError("No MONGO_URI set for Flask application")
    if not JWT_SECRET_KEY:
        raise ValueError("No JWT_SECRET_KEY set for Flask application")

AppConfig = Config