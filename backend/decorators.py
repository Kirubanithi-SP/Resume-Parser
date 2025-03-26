# /backend/decorators.py

from functools import wraps
from flask import request, jsonify, current_app, g
import jwt

def token_required(f):
    """
    Decorator to ensure a valid JWT is present in the Authorization header.
    Stores the decoded user identity in flask.g.current_user_id.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        # Check for 'Authorization: Bearer <token>' header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]

        if not token:
            return jsonify({"message": "Authentication Token is missing!"}), 401

        try:
            # Decode the token using the secret key
            # PyJWT expects the key directly
            # 'sub' is a common claim for subject/identity
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=["HS256"] # Specify the algorithm used for encoding
            )
            # Store the identity (e.g., user ID) in Flask's request context global `g`
            g.current_user_id = payload.get('sub') # Assuming you store user ID in 'sub' claim
            if not g.current_user_id:
                 return jsonify({"message": "Invalid Token: Missing user identity ('sub' claim)!"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError as e:
             print(f"Invalid token error: {e}") # Log the specific error
             return jsonify({"message": "Invalid Token!"}), 401
        except Exception as e:
             print(f"Unexpected error during token decoding: {e}")
             return jsonify({"message": "Token processing error"}), 500

        # Proceed with the original route function
        return f(*args, **kwargs)
    return decorated_function