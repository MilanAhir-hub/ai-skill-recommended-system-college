"""
recommender.py
--------------
Rule-based recommendation engine for career matching, skill gap analysis,
and learning roadmap generation.

Scoring Formula:
----------------
Total Score (0 - 100) = (
    (Skill Match Ratio * 0.50) +
    (Interest Match Ratio * 0.30) +
    (Education Match Ratio * 0.20)
) * 100

Where:
- Skill Match Ratio     = (Number of matched skills) / (Total required skills for career)
- Interest Match Ratio  = (Number of matched interests) / (Total relevant interests for career)
- Education Match Ratio = Heuristic match based on relevant degree/field keywords (0.0 to 1.0)
- The weights (0.50, 0.30, 0.20) are imported from career_data.MATCH_WEIGHTS.
"""

from career_data import CAREER_DATABASE, MATCH_WEIGHTS, SKILL_ROADMAPS


def normalize_string_list(items):
    """
    Cleans and normalizes a list of strings:
    - Trims whitespace
    - Converts to lowercase for case-insensitive matching
    - Filters out empty or non-string items
    """
    if not items or not isinstance(items, list):
        return []

    normalized = []
    for item in items:
        if isinstance(item, str) and item.strip():
            normalized.append(item.strip().lower())
    return normalized


def calculate_skill_match(user_skills, required_skills):
    """
    Compares user skills against career required skills.
    Returns:
    - match_ratio (float between 0.0 and 1.0)
    - matched_skills (list of exact required skill names matched)
    - missing_skills (list of required skill names missing)
    """
    if not required_skills:
        return 0.0, [], []

    # Prepare lowercased sets for case-insensitive comparison
    user_skills_clean = set(normalize_string_list(user_skills))

    matched_skills = []
    missing_skills = []

    for req_skill in required_skills:
        if req_skill.lower() in user_skills_clean:
            matched_skills.append(req_skill)
        else:
            missing_skills.append(req_skill)

    # Calculate fraction of required skills the user possesses
    match_ratio = len(matched_skills) / len(required_skills)
    return match_ratio, matched_skills, missing_skills


def calculate_interest_match(user_interests, relevant_interests):
    """
    Compares user interests with career relevant interests.
    Supports flexible substring and exact matching.
    Returns:
    - match_ratio (float between 0.0 and 1.0)
    - matched_interests (list of career interests matched)
    """
    if not relevant_interests or not user_interests:
        return 0.0, []

    user_interests_clean = normalize_string_list(user_interests)
    matched_interests = []

    for career_interest in relevant_interests:
        ci_lower = career_interest.lower()
        # Match if exact match or if user interest is a substring/superset
        is_matched = any(
            ci_lower == ui or ci_lower in ui or ui in ci_lower
            for ui in user_interests_clean
        )
        if is_matched:
            matched_interests.append(career_interest)

    match_ratio = len(matched_interests) / len(relevant_interests)
    # Ensure ratio doesn't exceed 1.0
    match_ratio = min(1.0, match_ratio)
    return match_ratio, matched_interests


def calculate_education_match(user_education, career):
    """
    Evaluates education compatibility heuristically.
    Checks if user education contains relevant degrees or field keywords.
    Returns:
    - match_ratio (float between 0.0 and 1.0)
    """
    if not user_education or not isinstance(user_education, str):
        return 0.0

    edu_lower = user_education.strip().lower()
    if not edu_lower:
        return 0.0

    keywords = career.get("education_keywords", [])

    # Direct keyword match for the career's domain (e.g., Computer Science, Statistics, Web)
    for kw in keywords:
        if kw in edu_lower:
            return 1.0

    # General technical / engineering degree mentions
    general_tech_terms = [
        "engineering", "tech", "technology", "stem", "bachelor",
        "master", "b.tech", "b.e", "b.sc", "bca", "mca", "diploma"
    ]
    if any(term in edu_lower for term in general_tech_terms):
        return 0.75

    # Any other education mentioned
    return 0.40


def generate_roadmap(missing_skills):
    """
    Generates a structured learning roadmap for missing skills.
    Looks up predefined steps from SKILL_ROADMAPS.
    If a skill is not predefined, generates beginner-friendly default steps.
    """
    roadmap = {}

    for skill in missing_skills:
        # Check predefined roadmaps
        if skill in SKILL_ROADMAPS:
            roadmap[skill] = SKILL_ROADMAPS[skill]
        else:
            # Fallback roadmap if an unknown skill is encountered
            roadmap[skill] = [
                f"Step 1: Learn fundamental concepts and syntax of {skill}.",
                f"Step 2: Practice hands-on exercises and mini challenges with {skill}.",
                f"Step 3: Build a small portfolio project applying {skill} to solve a real problem."
            ]

    return roadmap


def evaluate_career_for_user(user, career, weights=None):
    """
    Calculates the matching score and detailed analysis for one career.
    Parameters:
    - user: dict with keys 'skills', 'interests', 'education', 'career_goal'
    - career: dict from CAREER_DATABASE
    - weights: dict of weights, defaults to MATCH_WEIGHTS
    """
    if weights is None:
        weights = MATCH_WEIGHTS

    user_skills = user.get("skills", [])
    user_interests = user.get("interests", [])
    user_education = user.get("education", "")
    user_goal = user.get("career_goal", "")

    # 1. Skill Match Calculation (50% default)
    skill_ratio, matched_skills, missing_skills = calculate_skill_match(
        user_skills, career["required_skills"]
    )

    # 2. Interest Match Calculation (30% default)
    interest_ratio, matched_interests = calculate_interest_match(
        user_interests, career["relevant_interests"]
    )

    # 3. Education Match Calculation (20% default)
    education_ratio = calculate_education_match(user_education, career)

    # 4. Weighted Heuristic Scoring Formula
    skill_weight = weights.get("skill", 0.50)
    interest_weight = weights.get("interest", 0.30)
    education_weight = weights.get("education", 0.20)

    raw_score = (
        (skill_ratio * skill_weight) +
        (interest_ratio * interest_weight) +
        (education_ratio * education_weight)
    )

    # Normalize to 0 - 100 range and round to 2 decimal places
    normalized_score = round(max(0.0, min(100.0, raw_score * 100)), 2)

    # 5. Check if user's optional career goal matches this career
    is_goal_match = False
    if user_goal and isinstance(user_goal, str):
        ug_lower = user_goal.strip().lower()
        title_lower = career["title"].lower()
        if ug_lower in title_lower or title_lower in ug_lower:
            is_goal_match = True

    # 6. Generate roadmap for missing skills
    roadmap = generate_roadmap(missing_skills)

    return {
        "career_id": career["id"],
        "career_title": career["title"],
        "description": career["description"],
        "recommended_education": career["recommended_education"],
        "matching_score": normalized_score,
        "score_breakdown": {
            "skill_match_percentage": round(skill_ratio * 100, 2),
            "interest_match_percentage": round(interest_ratio * 100, 2),
            "education_match_percentage": round(education_ratio * 100, 2),
            "weights_used": {
                "skill": f"{int(skill_weight * 100)}%",
                "interest": f"{int(interest_weight * 100)}%",
                "education": f"{int(education_weight * 100)}%"
            }
        },
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_interests": matched_interests,
        "matches_career_goal": is_goal_match,
        "learning_roadmap": roadmap
    }


def get_top_career_recommendations(user, careers=None, top_n=3, weights=None):
    """
    Evaluates all careers in the knowledge base for a given user profile.
    Returns the top 'top_n' careers sorted by matching_score in descending order.
    """
    if careers is None:
        careers = CAREER_DATABASE

    results = []
    for career in careers:
        scored_career = evaluate_career_for_user(user, career, weights)
        results.append(scored_career)

    # Sort descending by matching score
    results.sort(key=lambda item: item["matching_score"], reverse=True)

    # Return top N recommendations (default 3)
    return results[:top_n]
