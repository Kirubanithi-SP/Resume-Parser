# /backend/routes.py

from flask import Blueprint, request, jsonify, g
import os

# Import the custom decorator
from decorators import token_required

# Placeholder imports for your logic (keep these)
# from .processing import parse_pdf, check_resume_material, calculate_ats, generate_suggestions

main_bp = Blueprint('main', __name__, url_prefix='/api')

@main_bp.route('/upload', methods=['POST'])
@token_required # Apply the JWT protection decorator
def upload_resume():
    """
    Handles resume PDF upload, processing, and scoring.
    Requires JWT authentication (verified by @token_required).
    Expects a file named 'resume' in the form-data.
    """
    # Access user ID from Flask's g object if needed
    current_user_id = g.get('current_user_id')
    print(f"Upload request received from user ID: {current_user_id}") # Logging

    if 'resume' not in request.files:
        return jsonify({"message": "No resume file part in the request"}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file and file.filename.lower().endswith('.pdf'):
        try:
            # --- Placeholder for your processing logic ---
            print(f"Processing file: {file.filename}")
            # extracted_text = parse_pdf(file.read()) # Pass file content
            extracted_text = "Placeholder text from PDF."
            # is_resume = check_resume_material(extracted_text)
            is_resume = True # Simulate

            if is_resume:
                # ats_score = calculate_ats(extracted_text)
                # suggestions = generate_suggestions(extracted_text)
                ats_score = 88 # Placeholder
                suggestions = "Keywords look good. Add measurable results." # Placeholder

                return jsonify({
                    "status": 200,
                    "ats_score": ats_score,
                    "suggestions": suggestions
                }), 200
            else:
                return jsonify({
                    "status": 200,
                    "message": "The uploaded PDF doesn't contain enough information to be identified as a resume."
                }), 200
        except Exception as e:
            print(f"Error processing file: {e}")
            return jsonify({"message": "An error occurred while processing the file"}), 500
    else:
        return jsonify({"message": "Invalid file type. Only PDF is allowed."}), 400