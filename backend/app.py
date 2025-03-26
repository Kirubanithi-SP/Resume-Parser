# /backend/app.py

from flask import Flask, jsonify
from flask_cors import CORS

# Import config and initialization functions/blueprints
from config import AppConfig
from database import init_db, close_db_connection
from auth import auth_bp
from routes import main_bp

def create_app(config_class=AppConfig):
    """Creates and configures the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    print("Creating Flask app...")
    print(f"FLASK_ENV: {app.config.get('FLASK_ENV')}")

    # --- Initialize Database Connection ---
    try:
        with app.app_context(): # Ensure context for config access if needed within init_db
             init_db()
    except Exception as e:
        print(f"FATAL: Could not initialize database: {e}")
        # Decide how to handle this - exit, or let Flask start but DB routes will fail?
        # For now, we'll let it proceed but log the critical error.
        pass # Or raise the exception if DB is absolutely critical for startup

    # --- Initialize Extensions ---
    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}}) # Adjust origins for production

    # --- Register Blueprints ---
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # --- Basic Route ---
    @app.route('/')
    def health_check():
        """Basic health check endpoint."""
        # You could add a DB ping here if desired
        return jsonify({"status": "ok", "message": "Backend is running"})

    # --- Teardown Context ---
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """Closes the database connection when the app context tears down."""
        # This helps manage the connection lifecycle, although MongoClient
        # often manages pooling well on its own. Explicit close is good practice.
        # Note: This might close the connection frequently in development with reloading.
        # Consider if this is needed or if relying on MongoClient pooling is sufficient.
        # For simplicity in this example, let's keep it.
        # close_db_connection() # Uncomment if you want explicit closing on context teardown
        pass


    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    # Debug mode based on FLASK_ENV
    debug_mode = app.config.get('FLASK_ENV') == 'development'
    print(f"Running in debug mode: {debug_mode}")
    # Make sure host='0.0.0.0' if running in a container or need external access
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)