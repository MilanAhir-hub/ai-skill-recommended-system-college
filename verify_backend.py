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

    print_step("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_verification()
