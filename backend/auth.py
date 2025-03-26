# /backend/auth.py

from flask import Blueprint, request, jsonify, current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from bson import ObjectId # Import ObjectId to query by _id if needed

# Import the get_db function and the decorator
from database import get_db
from decorators import token_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    User registration endpoint using pymongo.
    Expects JSON: { "username": "user", "password": "password" }
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    db = get_db()
    users_collection = db.users

    # Check if user already exists
    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        return jsonify({"message": "Username already exists"}), 409 # Conflict

    try:
        # Create new user document
        hashed_password = generate_password_hash(password)
        new_user_doc = {
            "username": username,
            "password_hash": hashed_password,
            "created_at": datetime.datetime.utcnow()
        }
        result = users_collection.insert_one(new_user_doc)

        if result.inserted_id:
            return jsonify({"message": "User registered successfully"}), 201
        else:
            # This case should ideally not happen if insert_one doesn't raise error
            return jsonify({"message": "User registration failed"}), 500

    except Exception as e:
        # Log the exception e here if needed
        print(f"Registration error: {e}")
        return jsonify({"message": "An error occurred during registration"}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint using pymongo and PyJWT.
    Expects JSON: { "username": "user", "password": "password" }
    Returns JWT access token upon successful login.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    db = get_db()
    users_collection = db.users
    user_doc = users_collection.find_one({"username": username})

    if user_doc and check_password_hash(user_doc.get('password_hash'), password):
        try:
            # Prepare JWT payload
            token_payload = {
                'sub': str(user_doc['_id']), # User identity (convert ObjectId to string)
                'iat': datetime.datetime.utcnow(), # Issued at time
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24) # Expiration time
            }

            # Create JWT token using PyJWT
            access_token = jwt.encode(
                token_payload,
                current_app.config['JWT_SECRET_KEY'],
                algorithm="HS256"
            )

            return jsonify(access_token=access_token), 200

        except Exception as e:
            print(f"Token generation error: {e}")
            return jsonify({"message": "Error generating authentication token"}), 500
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@auth_bp.route('/me', methods=['GET'])
@token_required # Use the custom decorator
def get_current_user():
    """Gets the username of the currently logged-in user."""
    # The user ID is stored in g by the token_required decorator
    current_user_id_str = g.get('current_user_id')

    if not current_user_id_str:
         # Should ideally be caught by decorator, but belts and suspenders
         return jsonify({"message": "User identity not found in token"}), 401

    try:
        # Convert string ID back to ObjectId for querying MongoDB
        current_user_oid = ObjectId(current_user_id_str)
    except Exception:
        return jsonify({"message": "Invalid user ID format"}), 400

    db = get_db()
    users_collection = db.users
    user = users_collection.find_one({"_id": current_user_oid}, {"username": 1}) # Fetch only username

    if user:
        return jsonify({"username": user.get('username')}), 200
    else:
        # Should not happen if token is valid unless user was deleted
        return jsonify({"message": "User not found"}), 404