"""
app.py
------
Flask application exposing REST API endpoints for:
1.  System status                       (GET  /)
2.  Knowledge base stats                (GET  /api/stats)
3.  Career catalog                      (GET  /api/careers)
4.  Single career detail + ladder       (GET  /api/careers/<career_id>)
5.  Skill catalog + demand ranking      (GET  /api/skills)
6.  Interest & education catalogs       (GET  /api/interests, /api/education-options)
7.  User profile create / fetch         (POST /api/users, GET /api/users/<id>)
8.  Ranked recommendations + paths      (POST /api/recommend/<id>)
9.  Career path for any chosen career   (POST /api/career-path/<id>/<career_id>)
10. Side-by-side career comparison      (POST /api/compare/<id>)
11. Stateless instant analysis          (POST /api/analyze)

Everything is computed by the rule-based engine in recommender.py from the
static knowledge base in career_data.py: no ML model, no API key, no network
call is involved at any point.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from career_data import (
    CAREER_DATABASE,
    MATCH_WEIGHTS,
    SKILL_LIBRARY,
    SKILL_CATEGORIES,
    SKILL_ALIASES,
    INTEREST_LIBRARY,
    EDUCATION_OPTIONS,
    ALL_INTERESTS,
    ALGORITHM_CATALOG,
    ALGORITHM_COMBOS,
    DECISION_TREE,
    BAYES_PARAMS,
    DEFAULT_HOURS_PER_WEEK,
    get_career_by_id,
    knowledge_base_stats,
    validate_knowledge_base,
)
from database import init_db, create_user, get_user_by_id
from recommender import (
    get_top_career_recommendations,
    recommend_single_career,
    compare_careers,
    compare_algorithms,
    summarize_skill_demand,
    clamp_hours_per_week,
)
import algorithms

API_VERSION = "3.0.0"

# Initialize Flask application
app = Flask(__name__)
# Enable CORS for all routes so React frontend can communicate seamlessly
CORS(app)

# Automatically initialize the database and tables on startup
init_db()


# ==========================================
# Algorithm description (shared with the UI)
# ==========================================
AI_ALGO_INFO = {
    "name": "Rule-Based Expert System (Weighted MCDA + Prerequisite Graph)",
    "short_name": "Rule-Based Expert System & MCDA",
    "description": (
        "An explainable heuristic algorithm that scores competencies, interests and academic "
        "background to rank career pathways, then traverses a skill prerequisite graph to "
        "generate an ordered, time-estimated career path. Fully deterministic: no trained "
        "model and no external AI service is used."
    ),
    "steps": [
        {
            "title": "Profile Normalization",
            "desc": "Standardized entered skills through 242 aliases (js, ml, k8s) into canonical knowledge-base tokens."
        },
        {
            "title": "Weighted Skill Gap Analysis (50%)",
            "desc": "Compared your skills against each career's benchmark set, counting must-have core skills double."
        },
        {
            "title": "Interest Alignment (30%)",
            "desc": "Measured overlap between your selected interests and each career's day-to-day domain focus."
        },
        {
            "title": "Education Compatibility (20%)",
            "desc": "Matched your degree against each career's accepted academic keywords, with a partial-credit fallback."
        },
        {
            "title": "Score Prediction & Ranking",
            "desc": "Aggregated the weighted factors (plus a goal bonus) into a 0-100 fit score and ranked all 21 careers."
        },
        {
            "title": "Prerequisite Graph Traversal",
            "desc": "Pulled in missing prerequisites as bridge skills, then topologically ordered every skill you need."
        },
        {
            "title": "Career Path Generation",
            "desc": "Grouped the ordered skills into phases, estimated weeks from your study pace, and attached the 5-stage role ladder."
        }
    ]
}


# ==========================================
# Request helpers
# ==========================================
def get_request_payload():
    """Returns the JSON body as a dict, tolerating an empty or non-JSON body."""
    if not request.is_json:
        return {}
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def resolve_hours_per_week(payload, user=None):
    """
    Study pace resolution order: request body/query -> saved profile -> default.
    Always clamped to a sane range by the recommender.
    """
    raw = payload.get("hours_per_week", request.args.get("hours_per_week"))
    if raw in (None, ""):
        raw = (user or {}).get("hours_per_week", DEFAULT_HOURS_PER_WEEK)
    return clamp_hours_per_week(raw)


def resolve_algorithms(payload):
    """
    Reads the chosen algorithms from the request body or query string and falls
    back to the original defaults (Weighted MCDA + topological sort) whenever
    the caller asks for nothing, or asks for something unknown.
    """
    scoring = payload.get("scoring_algorithm", request.args.get("scoring_algorithm"))
    path = payload.get("path_algorithm", request.args.get("path_algorithm"))
    return (
        algorithms.resolve_scoring_algorithm(scoring),
        algorithms.resolve_path_algorithm(path)
    )


def algorithm_echo(scoring_algorithm, path_algorithm):
    """The algorithm block echoed back on every scored response."""
    scoring = algorithms.algorithm_info(scoring_algorithm, "scoring") or {}
    path = algorithms.algorithm_info(path_algorithm, "path") or {}
    return {
        "scoring": {
            "id": scoring_algorithm,
            "name": scoring.get("name", scoring_algorithm),
            "family": scoring.get("family", ""),
            "one_line": scoring.get("one_line", ""),
            "score_label": scoring.get("score_label", "Score"),
            "score_scale": scoring.get("score_scale", ""),
            "how_it_works": scoring.get("how_it_works", [])
        },
        "path": {
            "id": path_algorithm,
            "name": path.get("name", path_algorithm),
            "family": path.get("family", ""),
            "one_line": path.get("one_line", ""),
            "phase_label": path.get("phase_label", "Phase"),
            "how_it_works": path.get("how_it_works", [])
        },
        "defaults": {
            "scoring": algorithms.DEFAULT_SCORING_ALGORITHM,
            "path": algorithms.DEFAULT_PATH_ALGORITHM
        },
        "using_defaults": (
            scoring_algorithm == algorithms.DEFAULT_SCORING_ALGORITHM
            and path_algorithm == algorithms.DEFAULT_PATH_ALGORITHM
        )
    }


def career_summary(career):
    """Lighter career record for list views and the catalog UI."""
    return {
        "id": career["id"],
        "title": career["title"],
        "category": career.get("category", "General"),
        "description": career["description"],
        "required_skills": career["required_skills"],
        "core_skills": career.get("core_skills", []),
        "relevant_interests": career["relevant_interests"],
        "recommended_education": career["recommended_education"],
        "demand": career.get("demand", "Moderate"),
        "entry_salary_inr": career.get("entry_salary_inr", ""),
        "remote_friendly": career.get("remote_friendly", False),
        "total_stages": len(career.get("career_path", [])),
        "top_role": career.get("career_path", [{}])[-1].get("role", "")
    }


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
# 1. Status & Knowledge Base
# ==========================================
@app.route("/", methods=["GET"])
def index():
    """
    GET /
    Basic API status and sitemap.
    """
    stats = knowledge_base_stats()
    return jsonify({
        "status": "online",
        "message": "AI-Powered Personalized Career and Skill Recommendation API is running",
        "version": API_VERSION,
        "engine": "Rule-based expert system (no ML model, no external API)",
        "algorithms": {
            "scoring": [a["id"] for a in ALGORITHM_CATALOG["scoring"]],
            "path": [a["id"] for a in ALGORITHM_CATALOG["path"]],
            "defaults": {
                "scoring": algorithms.DEFAULT_SCORING_ALGORITHM,
                "path": algorithms.DEFAULT_PATH_ALGORITHM
            }
        },
        "knowledge_base": {
            "careers": stats["total_careers"],
            "skills": stats["total_skills"],
            "career_stages": stats["total_career_stages"]
        },
        "endpoints": {
            "GET /": "Basic API status",
            "GET /api/stats": "Knowledge base size and scoring weights",
            "GET /api/careers": "List all career paths (add ?view=summary for a lighter payload)",
            "GET /api/careers/<career_id>": "Full detail and role progression ladder for one career",
            "GET /api/skills": "Skill catalog grouped by category, with demand ranking",
            "GET /api/interests": "Grouped interest catalog for the profile form",
            "GET /api/education-options": "Education dropdown options",
            "POST /api/users": "Create and save a user profile",
            "GET /api/users/<user_id>": "Retrieve a saved user profile",
            "GET /api/algorithms": "The selectable algorithms: 3 scoring, 2 path, with strengths and limits",
            "POST /api/recommend/<user_id>": "Top career recommendations with generated career paths (accepts scoring_algorithm, path_algorithm)",
            "POST /api/career-path/<user_id>/<career_id>": "Generate the career path for any chosen career",
            "POST /api/compare/<user_id>": "Compare several careers side by side",
            "POST /api/compare-algorithms/<user_id>": "Run every algorithm on one profile and report what changes",
            "POST /api/analyze": "Instant analysis without saving a profile"
        }
    }), 200


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """
    GET /api/stats
    Knowledge base size, scoring weights and the top in-demand skills.
    Used by the landing page to show what the engine actually knows.
    """
    stats = knowledge_base_stats()
    demand = summarize_skill_demand()

    return jsonify({
        "status": "success",
        "version": API_VERSION,
        "knowledge_base": stats,
        "ai_algo": AI_ALGO_INFO,
        "most_in_demand_skills": demand[:12],
        "consistency_problems": validate_knowledge_base()
    }), 200


# ==========================================
# 2. Career catalog
# ==========================================
@app.route("/api/careers", methods=["GET"])
def get_careers():
    """
    GET /api/careers
    Lists all available career paths and their required skills.
    Optional query params:
      ?view=summary          lighter records for list/catalog views
      ?category=Cybersecurity filter by career category
    """
    careers = CAREER_DATABASE

    category = request.args.get("category")
    if category:
        needle = category.strip().lower()
        careers = [c for c in careers if c.get("category", "").lower() == needle]

    view = (request.args.get("view") or "").strip().lower()
    payload = [career_summary(c) for c in careers] if view == "summary" else careers

    return jsonify({
        "status": "success",
        "total_careers": len(payload),
        "categories": sorted({c.get("category", "General") for c in CAREER_DATABASE}),
        "careers": payload
    }), 200


@app.route("/api/careers/<career_id>", methods=["GET"])
def get_career_detail(career_id):
    """
    GET /api/careers/<career_id>
    Full knowledge-base record for one career, including its 5-stage role
    progression ladder, tools, certifications and portfolio project ideas.
    """
    career = get_career_by_id(career_id)
    if not career:
        return jsonify({
            "status": "error",
            "message": "Career '{0}' was not found in the knowledge base.".format(career_id)
        }), 404

    related = [
        {"id": rid, "title": get_career_by_id(rid)["title"]}
        for rid in career.get("related_careers", [])
        if get_career_by_id(rid)
    ]

    return jsonify({
        "status": "success",
        "career": career,
        "related_careers": related
    }), 200


# ==========================================
# 3. Skill / interest / education catalogs
# ==========================================
@app.route("/api/skills", methods=["GET"])
def get_skills():
    """
    GET /api/skills
    Skill catalog grouped by category with difficulty, learning hours and
    prerequisites, plus how many careers require each skill.
    """
    demand_lookup = {item["skill"]: item["required_by"] for item in summarize_skill_demand()}

    grouped = {}
    for category, skills in SKILL_CATEGORIES.items():
        grouped[category] = [
            {
                "skill": skill,
                "difficulty": SKILL_LIBRARY[skill]["difficulty"],
                "learning_hours": SKILL_LIBRARY[skill]["learning_hours"],
                "prerequisites": SKILL_LIBRARY[skill]["prerequisites"],
                "required_by_careers": demand_lookup.get(skill, 0)
            }
            for skill in sorted(skills)
        ]

    return jsonify({
        "status": "success",
        "total_skills": len(SKILL_LIBRARY),
        "total_aliases": len(SKILL_ALIASES),
        "categories": grouped,
        "most_in_demand_skills": summarize_skill_demand()[:12]
    }), 200


@app.route("/api/interests", methods=["GET"])
def get_interests():
    """
    GET /api/interests
    Grouped interest catalog used by the profile form.
    """
    return jsonify({
        "status": "success",
        "total_interests": len(ALL_INTERESTS),
        "groups": INTEREST_LIBRARY
    }), 200


@app.route("/api/education-options", methods=["GET"])
def get_education_options():
    """
    GET /api/education-options
    Education dropdown values, kept server-side so the form options and the
    education scoring keywords never drift apart.
    """
    return jsonify({
        "status": "success",
        "total_options": len(EDUCATION_OPTIONS),
        "options": EDUCATION_OPTIONS
    }), 200


# ==========================================
# 4. User profiles
# ==========================================
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
        "career_goal": "Data Analyst",   (optional)
        "hours_per_week": 10             (optional study pace, 2 - 60)
    }
    """
    # Verify request content is JSON
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Request body must be valid JSON with 'Content-Type: application/json'"
        }), 400

    data = request.get_json(silent=True) or {}

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

    hours_per_week = clamp_hours_per_week(data.get("hours_per_week", DEFAULT_HOURS_PER_WEEK))

    # Save to SQLite database
    new_user = create_user(
        name=name,
        education=education,
        skills=skills,
        interests=interests,
        career_goal=career_goal,
        hours_per_week=hours_per_week
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
            "message": "User with ID {0} was not found.".format(user_id)
        }), 404

    return jsonify({
        "status": "success",
        "user": user
    }), 200


# ==========================================
# 5. Recommendations & career paths
# ==========================================
@app.route("/api/recommend/<int:user_id>", methods=["POST"])
def recommend_for_user(user_id):
    """
    POST /api/recommend/<user_id>
    Generates ranked career recommendations for a saved user:
    - Matching score (0-100) using 50% skill, 30% interest, 20% education
    - Weighted skill gap analysis (core skills count double)
    - A generated career path per career: phased learning plan ordered by the
      skill prerequisite graph, duration estimate, and the 5-stage role ladder

    Optional JSON body / query params:
      top_n          number of careers to return (default 3, max 21)
      hours_per_week study pace used for duration estimates
    """
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": "User with ID {0} was not found.".format(user_id)
        }), 404

    payload = get_request_payload()
    hours_per_week = resolve_hours_per_week(payload, user)
    scoring_algorithm, path_algorithm = resolve_algorithms(payload)

    raw_top_n = payload.get("top_n", request.args.get("top_n", 3))
    try:
        top_n = int(raw_top_n)
    except (TypeError, ValueError):
        top_n = 3
    top_n = max(1, min(top_n, len(CAREER_DATABASE)))

    recommendations = get_top_career_recommendations(
        user, top_n=top_n, hours_per_week=hours_per_week,
        scoring_algorithm=scoring_algorithm, path_algorithm=path_algorithm
    )

    return jsonify({
        "status": "success",
        "user_id": user["id"],
        "user_name": user["name"],
        "user_education": user["education"],
        "user_goal": user["career_goal"],
        "hours_per_week": hours_per_week,
        "careers_evaluated": len(CAREER_DATABASE),
        "total_recommendations": len(recommendations),
        "scoring_weights": MATCH_WEIGHTS,
        "algorithm": algorithm_echo(scoring_algorithm, path_algorithm),
        "ai_algo": AI_ALGO_INFO,
        "recommendations": recommendations
    }), 200


@app.route("/api/career-path/<int:user_id>/<career_id>", methods=["POST", "GET"])
def career_path_for_user(user_id, career_id):
    """
    POST /api/career-path/<user_id>/<career_id>
    Generates the full career path for one specific career, even when it is not
    in the student's top matches. Lets the UI offer "explore any career".
    """
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": "User with ID {0} was not found.".format(user_id)
        }), 404

    payload = get_request_payload()
    hours_per_week = resolve_hours_per_week(payload, user)
    scoring_algorithm, path_algorithm = resolve_algorithms(payload)

    evaluation = recommend_single_career(
        user, career_id, hours_per_week=hours_per_week,
        scoring_algorithm=scoring_algorithm, path_algorithm=path_algorithm
    )
    if not evaluation:
        return jsonify({
            "status": "error",
            "message": "Career '{0}' was not found in the knowledge base.".format(career_id)
        }), 404

    return jsonify({
        "status": "success",
        "user_id": user["id"],
        "user_name": user["name"],
        "hours_per_week": hours_per_week,
        "algorithm": algorithm_echo(scoring_algorithm, path_algorithm),
        "evaluation": evaluation
    }), 200


@app.route("/api/compare/<int:user_id>", methods=["POST"])
def compare_for_user(user_id):
    """
    POST /api/compare/<user_id>
    Compares several careers side by side for the same profile.
    Body: {"career_ids": ["data_analyst", "data_scientist"], "hours_per_week": 12}
    """
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": "User with ID {0} was not found.".format(user_id)
        }), 404

    payload = get_request_payload()
    career_ids = payload.get("career_ids", [])

    if not isinstance(career_ids, list) or not career_ids:
        return jsonify({
            "status": "error",
            "message": "Validation error: 'career_ids' must be a non-empty list of career ids."
        }), 400

    hours_per_week = resolve_hours_per_week(payload, user)
    scoring_algorithm, path_algorithm = resolve_algorithms(payload)
    evaluations = compare_careers(
        user, career_ids, hours_per_week=hours_per_week,
        scoring_algorithm=scoring_algorithm, path_algorithm=path_algorithm
    )

    if not evaluations:
        return jsonify({
            "status": "error",
            "message": "None of the supplied career ids exist in the knowledge base."
        }), 404

    return jsonify({
        "status": "success",
        "user_id": user["id"],
        "hours_per_week": hours_per_week,
        "algorithm": algorithm_echo(scoring_algorithm, path_algorithm),
        "total_compared": len(evaluations),
        "comparisons": evaluations
    }), 200


@app.route("/api/analyze", methods=["POST"])
def analyze_profile():
    """
    POST /api/analyze
    Stateless analysis: scores a profile and generates career paths without
    saving anything to the database. Useful for a quick "try it" flow.
    Body: {"education": "...", "skills": [...], "interests": [...],
           "career_goal": "...", "top_n": 3, "hours_per_week": 10}
    """
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Request body must be valid JSON with 'Content-Type: application/json'"
        }), 400

    data = request.get_json(silent=True) or {}

    skills = data.get("skills", [])
    interests = data.get("interests", [])

    if not isinstance(skills, list) or not isinstance(interests, list):
        return jsonify({
            "status": "error",
            "message": "Validation error: 'skills' and 'interests' must be lists of strings."
        }), 400

    if not skills and not interests:
        return jsonify({
            "status": "error",
            "message": "Validation error: provide at least one skill or interest to analyze."
        }), 400

    profile = {
        "name": (data.get("name") or "Guest").strip() or "Guest",
        "education": data.get("education", ""),
        "skills": skills,
        "interests": interests,
        "career_goal": data.get("career_goal", "")
    }

    hours_per_week = resolve_hours_per_week(data)
    scoring_algorithm, path_algorithm = resolve_algorithms(data)

    try:
        top_n = int(data.get("top_n", 3))
    except (TypeError, ValueError):
        top_n = 3
    top_n = max(1, min(top_n, len(CAREER_DATABASE)))

    recommendations = get_top_career_recommendations(
        profile, top_n=top_n, hours_per_week=hours_per_week,
        scoring_algorithm=scoring_algorithm, path_algorithm=path_algorithm
    )

    return jsonify({
        "status": "success",
        "saved": False,
        "user_name": profile["name"],
        "hours_per_week": hours_per_week,
        "careers_evaluated": len(CAREER_DATABASE),
        "total_recommendations": len(recommendations),
        "algorithm": algorithm_echo(scoring_algorithm, path_algorithm),
        "ai_algo": AI_ALGO_INFO,
        "recommendations": recommendations
    }), 200


# ==========================================
# 6. Algorithm choice and comparison
# ==========================================
@app.route("/api/algorithms", methods=["GET"])
def get_algorithms():
    """
    GET /api/algorithms
    The catalog of selectable algorithms: three ways to score careers and two
    ways to order the learning path, with how each one works, what it is good
    at and where it falls short. Powers the algorithm picker in the UI.
    """
    return jsonify({
        "status": "success",
        "defaults": {
            "scoring": algorithms.DEFAULT_SCORING_ALGORITHM,
            "path": algorithms.DEFAULT_PATH_ALGORITHM
        },
        "combos": ALGORITHM_COMBOS,
        "scoring_algorithms": ALGORITHM_CATALOG["scoring"],
        "path_algorithms": ALGORITHM_CATALOG["path"],
        "knowledge": {
            "decision_tree_questions": [
                DECISION_TREE["question"],
                "Which skill family is strongest?"
            ],
            "decision_tree_branches": sorted(
                b for b in DECISION_TREE["branches"] if b != "_default"
            ),
            "bayes_parameters": BAYES_PARAMS
        }
    }), 200


@app.route("/api/compare-algorithms/<int:user_id>", methods=["POST", "GET"])
def compare_algorithms_for_user(user_id):
    """
    POST /api/compare-algorithms/<user_id>
    Runs every algorithm over the same profile and reports what changes:
    which career each scoring algorithm puts first, whether they agree, how
    the two path algorithms shape the same set of skills, and which choice
    suits which situation. This answers "if we choose this one, then what?".
    """
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": "User with ID {0} was not found.".format(user_id)
        }), 404

    payload = get_request_payload()
    hours_per_week = resolve_hours_per_week(payload, user)

    try:
        top_n = int(payload.get("top_n", request.args.get("top_n", 3)))
    except (TypeError, ValueError):
        top_n = 3
    top_n = max(1, min(top_n, len(CAREER_DATABASE)))

    comparison = compare_algorithms(user, hours_per_week=hours_per_week, top_n=top_n)

    return jsonify({
        "status": "success",
        "user_id": user["id"],
        "user_name": user["name"],
        "hours_per_week": hours_per_week,
        "careers_evaluated": len(CAREER_DATABASE),
        "comparison": comparison
    }), 200


if __name__ == "__main__":
    # Run development server on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
