"""
app.py
------
Flask application exposing REST API endpoints for:
1. System status (GET /)
2. Career catalog (GET /api/careers)
3. User profile creation and retrieval (POST /api/users, GET /api/users/<id>)
4. Rule-based career recommendation & skill gap analysis (POST /api/recommend/<id>)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from career_data import CAREER_DATABASE
from database import init_db, create_user, get_user_by_id
from recommender import get_top_career_recommendations

# Initialize Flask application
app = Flask(__name__)
# Enable CORS for all routes so React frontend can communicate seamlessly
CORS(app)

# Automatically initialize the database and tables on startup
init_db()


# ==========================================
# Error Handlers
# ==========================================
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "status": "error",
        "message": getattr(error, "description", "Bad Request")
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": getattr(error, "description", "Resource Not Found")
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "status": "error",
        "message": "Method Not Allowed"
    }), 405


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal Server Error"
    }), 500


# ==========================================
# API Endpoints
# ==========================================

@app.route("/", methods=["GET"])
def index():
    """
    GET /
    Basic API status and sitemap.
    """
    return jsonify({
        "status": "online",
        "message": "AI-Powered Personalized Career and Skill Recommendation API is running",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "Basic API status",
            "GET /api/careers": "List available careers and their required skills",
            "POST /api/users": "Create and save a user profile",
            "GET /api/users/<user_id>": "Retrieve a saved user profile",
            "POST /api/recommend/<user_id>": "Generate top 3 career recommendations, missing skills & roadmap"
        }
    }), 200


@app.route("/api/careers", methods=["GET"])
def get_careers():
    """
    GET /api/careers
    List all available career paths and their required skills from the knowledge base.
    """
    return jsonify({
        "status": "success",
        "total_careers": len(CAREER_DATABASE),
        "careers": CAREER_DATABASE
    }), 200


@app.route("/api/users", methods=["POST"])
def register_user():
    """
    POST /api/users
    Create and save a new user profile in SQLite.
    Expected JSON body:
    {
        "name": "Alex",
        "education": "Bachelor of Technology in CS",
        "skills": ["Python", "SQL", "Git"],
        "interests": ["Machine Learning", "Data Analysis"],
        "career_goal": "Data Analyst" (optional)
    }
    """
    # Verify request content is JSON
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Request body must be valid JSON with 'Content-Type: application/json'"
        }), 400

    data = request.get_json() or {}

    # Validate required 'name' field
    name = data.get("name")
    if not name or not isinstance(name, str) or not name.strip():
        return jsonify({
            "status": "error",
            "message": "Validation error: 'name' is required and cannot be empty."
        }), 400

    education = data.get("education", "")
    skills = data.get("skills", [])
    interests = data.get("interests", [])
    career_goal = data.get("career_goal", "")

    # Validate types if supplied
    if not isinstance(skills, list):
        return jsonify({
            "status": "error",
            "message": "Validation error: 'skills' must be a list of strings."
        }), 400

    if not isinstance(interests, list):
        return jsonify({
            "status": "error",
            "message": "Validation error: 'interests' must be a list of strings."
        }), 400

    # Save to SQLite database
    new_user = create_user(
        name=name,
        education=education,
        skills=skills,
        interests=interests,
        career_goal=career_goal
    )

    return jsonify({
        "status": "success",
        "message": "User profile created successfully",
        "user": new_user
    }), 201


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """
    GET /api/users/<user_id>
    Retrieve a saved user profile by user_id.
    """
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": f"User with ID {user_id} was not found."
        }), 404

    return jsonify({
        "status": "success",
        "user": user
    }), 200


@app.route("/api/recommend/<int:user_id>", methods=["POST"])
def recommend_for_user(user_id):
    """
    POST /api/recommend/<user_id>
    Generates the top 3 career recommendations for a user:
    - Calculates matching score (0-100) using 50% skill, 30% interest, 20% education
    - Performs skill gap analysis to identify missing skills
    - Generates step-by-step learning roadmap for missing skills
    """
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": f"User with ID {user_id} was not found."
        }), 404

    # Run rule-based recommendation engine for top 3 careers
    recommendations = get_top_career_recommendations(user, top_n=3)

    return jsonify({
        "status": "success",
        "user_id": user["id"],
        "user_name": user["name"],
        "user_education": user["education"],
        "user_goal": user["career_goal"],
        "total_recommendations": len(recommendations),
        "recommendations": recommendations
    }), 200


if __name__ == "__main__":
    # Run development server on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
