"""
verify_backend.py
-----------------
Direct verification script testing all requirements and outputting
formatted JSON responses for every API endpoint.
"""

import json
from app import app


def print_step(title):
    print("\n" + "=" * 65)
    print(f"  {title}")
    print("=" * 65)


def run_verification():
    client = app.test_client()

    # -------------------------------------------------------------
    # 1. Test GET / (API Status)
    # -------------------------------------------------------------
    print_step("1. Testing GET / (API Status)")
    res = client.get("/")
    print(f"Status Code: {res.status_code}")
    print("Response JSON:")
    print(json.dumps(res.get_json(), indent=2))
    assert res.status_code == 200

    # -------------------------------------------------------------
    # 2. Test GET /api/careers (Available Careers Catalog)
    # -------------------------------------------------------------
    print_step("2. Testing GET /api/careers (Available Careers)")
    res = client.get("/api/careers")
    print(f"Status Code: {res.status_code}")
    data = res.get_json()
    print(f"Total Careers Found: {data['total_careers']}")
    for career in data["careers"]:
        print(f" - {career['title']}: {len(career['required_skills'])} required skills")
    assert res.status_code == 200

    # -------------------------------------------------------------
    # 3. Test POST /api/users (Create User Profile)
    # -------------------------------------------------------------
    print_step("3. Testing POST /api/users (Create User Profile)")
    payload_user = {
        "name": "Aarav Sharma",
        "education": "Bachelor of Technology in Computer Science",
        "skills": ["Python", "SQL", "Git"],
        "interests": ["Machine Learning", "Data Analysis", "Artificial Intelligence"],
        "career_goal": "AI/ML Engineer"
    }
    res = client.post("/api/users", json=payload_user)
    print(f"Status Code: {res.status_code}")
    user_data = res.get_json()
    print("Response JSON:")
    print(json.dumps(user_data, indent=2))
    assert res.status_code == 201
    user_id = user_data["user"]["id"]

    # -------------------------------------------------------------
    # 4. Test GET /api/users/<user_id> (Retrieve Saved Profile)
    # -------------------------------------------------------------
    print_step(f"4. Testing GET /api/users/{user_id} (Retrieve Profile)")
    res = client.get(f"/api/users/{user_id}")
    print(f"Status Code: {res.status_code}")
    print("Response JSON:")
    print(json.dumps(res.get_json(), indent=2))
    assert res.status_code == 200

    # -------------------------------------------------------------
    # 5. Test POST /api/recommend/<user_id> (Generate Recommendations)
    # -------------------------------------------------------------
    print_step(f"5. Testing POST /api/recommend/{user_id} (AI Recommendation)")
    res = client.post(f"/api/recommend/{user_id}")
    print(f"Status Code: {res.status_code}")
    rec_data = res.get_json()
    print("Response JSON:")
    print(json.dumps(rec_data, indent=2))
    assert res.status_code == 200
    assert len(rec_data["recommendations"]) == 3

    # Check score bounds and order
    scores = [r["matching_score"] for r in rec_data["recommendations"]]
    print(f"\nTop 3 Recommendation Scores: {scores}")
    assert all(0.0 <= s <= 100.0 for s in scores)
    assert scores == sorted(scores, reverse=True), "Recommendations must be sorted descending by score"

    # -------------------------------------------------------------
    # 6. Test Profile with Empty / Missing Optional Fields
    # -------------------------------------------------------------
    print_step("6. Testing POST /api/users with Minimal/Empty Fields")
    minimal_user = {
        "name": "Pooja V."
    }
    res = client.post("/api/users", json=minimal_user)
    print(f"Status Code: {res.status_code}")
    min_user_data = res.get_json()
    print("Response JSON:")
    print(json.dumps(min_user_data, indent=2))
    assert res.status_code == 201
    min_user_id = min_user_data["user"]["id"]

    # Recommend for minimal profile
    res_min_rec = client.post(f"/api/recommend/{min_user_id}")
    assert res_min_rec.status_code == 200
    min_scores = [r["matching_score"] for r in res_min_rec.get_json()["recommendations"]]
    print(f"Minimal Profile Recommendation Scores: {min_scores}")
    assert all(0.0 <= s <= 100.0 for s in min_scores)

    # -------------------------------------------------------------
    # 7. Test Validation & Error Handling (400, 404)
    # -------------------------------------------------------------
    print_step("7. Testing Validation & Error Handling")
    # Missing name
    res_err1 = client.post("/api/users", json={"skills": ["Python"]})
    print(f"Missing Name -> Status: {res_err1.status_code}, Msg: {res_err1.get_json()['message']}")
    assert res_err1.status_code == 400

    # User not found (404)
    res_err2 = client.get("/api/users/999999")
    print(f"Get Invalid User -> Status: {res_err2.status_code}, Msg: {res_err2.get_json()['message']}")
    assert res_err2.status_code == 404

    # Recommend invalid user (404)
    res_err3 = client.post("/api/recommend/999999")
    print(f"Recommend Invalid User -> Status: {res_err3.status_code}, Msg: {res_err3.get_json()['message']}")
    assert res_err3.status_code == 404

    # -------------------------------------------------------------
    # 8. Knowledge base integrity & size
    # -------------------------------------------------------------
    print_step("8. Testing GET /api/stats (Knowledge Base Integrity)")
    res = client.get("/api/stats")
    stats_data = res.get_json()
    kb = stats_data["knowledge_base"]
    print(f"Careers            : {kb['total_careers']}")
    print(f"Skills             : {kb['total_skills']}")
    print(f"Skill aliases      : {kb['total_skill_aliases']}")
    print(f"Career path stages : {kb['total_career_stages']}")
    print(f"Roadmap steps      : {kb['total_roadmap_steps']}")
    print(f"Consistency issues : {stats_data['consistency_problems']}")
    print("\nMost in-demand skills across all careers:")
    for item in stats_data["most_in_demand_skills"][:6]:
        print(f" - {item['skill']}: required by {item['required_by']} careers ({item['difficulty']})")
    assert res.status_code == 200
    assert stats_data["consistency_problems"] == [], "Knowledge base has consistency problems"

    # -------------------------------------------------------------
    # 9. Skill catalog
    # -------------------------------------------------------------
    print_step("9. Testing GET /api/skills (Skill Catalog)")
    res = client.get("/api/skills")
    skills_data = res.get_json()
    print(f"Total skills: {skills_data['total_skills']} across {len(skills_data['categories'])} categories")
    for category, skills in list(skills_data["categories"].items())[:5]:
        print(f" - {category}: {len(skills)} skills")
    assert res.status_code == 200

    # -------------------------------------------------------------
    # 10. Generated career path detail
    # -------------------------------------------------------------
    print_step(f"10. Testing POST /api/career-path/{user_id}/ai_ml_engineer (Career Path)")
    res = client.post(f"/api/career-path/{user_id}/ai_ml_engineer", json={"hours_per_week": 12})
    assert res.status_code == 200
    evaluation = res.get_json()["evaluation"]
    path = evaluation["career_path"]
    plan = path["learning_plan"]

    print(f"Career          : {evaluation['career_title']} ({evaluation['matching_score']}% fit)")
    print(f"Readiness       : {path['readiness']['level']} ({path['readiness']['skill_coverage_percentage']}% coverage)")
    print(f"Skills to learn : {plan['total_skills_to_learn']} ({plan['total_learning_hours']} hrs, {plan['estimated_duration']})")
    print(f"Bridge skills   : {plan['bridge_skills']}")
    print("\nGenerated learning phases:")
    for phase in plan["phases"]:
        skills = ", ".join(s["skill"] for s in phase["skills"]) or "portfolio & interview work"
        print(f" {phase['name']} (weeks {phase['starts_week']}-{phase['ends_week']}): {skills}")

    print("\nRole progression ladder:")
    for stage in path["progression_ladder"]:
        print(f" Stage {stage['stage']} [{stage['status']}] {stage['role']} | {stage['experience']} | {stage['salary_inr']}")

    print("\nImmediate next actions:")
    for action in path["next_actions"]:
        print(f" - {action}")

    # Verify the plan never schedules a skill before its prerequisites
    import career_data
    sequence = plan["skill_sequence"]
    position = {skill: index for index, skill in enumerate(sequence)}
    for skill in sequence:
        for prereq in career_data.get_skill_meta(skill)["prerequisites"]:
            if prereq in position:
                assert position[prereq] < position[skill], (
                    f"{prereq} must come before {skill}"
                )
    print("\nPrerequisite ordering verified for the full skill sequence.")

    # -------------------------------------------------------------
    # 11. Career comparison & stateless analysis
    # -------------------------------------------------------------
    print_step(f"11. Testing POST /api/compare/{user_id} and POST /api/analyze")
    res = client.post(
        f"/api/compare/{user_id}",
        json={"career_ids": ["data_analyst", "data_scientist", "ai_ml_engineer"]}
    )
    assert res.status_code == 200
    print("Comparison results:")
    for item in res.get_json()["comparisons"]:
        print(f" - {item['career_title']}: {item['matching_score']}% fit, "
              f"{item['skill_gap_summary']['missing_count']} gaps, "
              f"{item['career_path']['learning_plan']['estimated_duration']}")

    res = client.post("/api/analyze", json={
        "name": "Guest Student",
        "education": "BCA",
        "skills": ["html", "css", "js"],
        "interests": ["Frontend Development"],
        "top_n": 3
    })
    assert res.status_code == 200
    analyze_data = res.get_json()
    print(f"\nStateless analysis (saved={analyze_data['saved']}) using skill aliases html/css/js:")
    for item in analyze_data["recommendations"]:
        print(f" - {item['career_title']}: {item['matching_score']}% | matched {item['matched_skills']}")

    print_step("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_verification()
