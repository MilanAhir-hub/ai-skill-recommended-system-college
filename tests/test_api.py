"""
tests/test_api.py
-----------------
Automated tests for the Career & Skill Recommendation System.
Uses Python's built-in unittest framework and Flask's test client.
"""

import os
import unittest
import json

# Point database to an isolated test SQLite file before importing app
import database
database.DEFAULT_DB_PATH = "test_career_system.db"

from app import app


class CareerRecommendationApiTestCase(unittest.TestCase):
    """
    Test suite verifying all API endpoints, database persistence,
    rule-based scoring bounds, skill gap analysis, and roadmaps.
    """

    def setUp(self):
        """Set up test environment before each test."""
        app.config["TESTING"] = True
        self.client = app.test_client()

        # Initialize fresh test database tables
        database.init_db("test_career_system.db")

    def tearDown(self):
        """Clean up test database file after each test."""
        if os.path.exists("test_career_system.db"):
            try:
                os.remove("test_career_system.db")
            except PermissionError:
                pass

    # ==========================================
    # 1. API Status and Catalog Tests
    # ==========================================
    def test_index_status_endpoint(self):
        """Test GET / returns online status and endpoint list."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data["status"], "online")
        self.assertIn("endpoints", data)

    def test_get_careers_catalog(self):
        """Test GET /api/careers returns available careers and required skills."""
        response = self.client.get("/api/careers")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreaterEqual(data["total_careers"], 5)

        # Check required fields in the first career item
        first_career = data["careers"][0]
        self.assertIn("title", first_career)
        self.assertIn("required_skills", first_career)
        self.assertIn("relevant_interests", first_career)
        self.assertIn("recommended_education", first_career)

    # ==========================================
    # 2. User Profile Creation & Retrieval Tests
    # ==========================================
    def test_create_user_valid(self):
        """Test POST /api/users with valid data saves user in SQLite."""
        payload = {
            "name": "Priya Patel",
            "education": "B.Tech in Computer Science",
            "skills": ["Python", "SQL", "Git"],
            "interests": ["Data Analysis", "Machine Learning"],
            "career_goal": "Data Analyst"
        }
        response = self.client.post(
            "/api/users",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("user", data)
        self.assertEqual(data["user"]["name"], "Priya Patel")
        self.assertEqual(data["user"]["skills"], ["Python", "SQL", "Git"])
        self.assertIn("id", data["user"])

    def test_create_user_empty_or_missing_optional_fields(self):
        """Test POST /api/users with only name, omitting optional fields."""
        payload = {
            "name": "Rahul Verma"
        }
        response = self.client.post(
            "/api/users",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

        data = response.get_json()
        self.assertEqual(data["user"]["name"], "Rahul Verma")
        self.assertEqual(data["user"]["skills"], [])
        self.assertEqual(data["user"]["interests"], [])
        self.assertEqual(data["user"]["education"], "")
        self.assertEqual(data["user"]["career_goal"], "")

    def test_create_user_missing_name(self):
        """Test POST /api/users without name returns 400 Bad Request."""
        payload = {
            "education": "BCA",
            "skills": ["HTML", "CSS"]
        }
        response = self.client.post(
            "/api/users",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["status"], "error")

    def test_create_user_empty_name(self):
        """Test POST /api/users with empty string for name returns 400."""
        payload = {
            "name": "   ",
            "skills": ["Python"]
        }
        response = self.client.post(
            "/api/users",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_json(self):
        """Test POST /api/users with non-JSON body returns 400."""
        response = self.client.post(
            "/api/users",
            data="not a json string",
            content_type="text/plain"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_skills_type(self):
        """Test POST /api/users with non-list skills returns 400."""
        payload = {
            "name": "Sneha",
            "skills": "Python, SQL"  # string instead of list
        }
        response = self.client.post(
            "/api/users",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_get_user_success(self):
        """Test GET /api/users/<user_id> retrieves profile from SQLite."""
        # Create user
        payload = {
            "name": "Vikram Singh",
            "education": "B.Sc Computer Science",
            "skills": ["HTML", "CSS", "JavaScript"],
            "interests": ["UI/UX Design"]
        }
        create_res = self.client.post(
            "/api/users",
            data=json.dumps(payload),
            content_type="application/json"
        )
        user_id = create_res.get_json()["user"]["id"]

        # Retrieve user
        get_res = self.client.get(f"/api/users/{user_id}")
        self.assertEqual(get_res.status_code, 200)

        data = get_res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["user"]["id"], user_id)
        self.assertEqual(data["user"]["name"], "Vikram Singh")
        self.assertEqual(data["user"]["skills"], ["HTML", "CSS", "JavaScript"])

    def test_get_user_not_found(self):
        """Test GET /api/users/<user_id> with non-existent id returns 404."""
        response = self.client.get("/api/users/99999")
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["status"], "error")

    # ==========================================
    # 3. Recommendation & Scoring Tests
    # ==========================================
    def test_recommendation_top_three_and_sorted(self):
        """
        Test POST /api/recommend/<user_id>:
        - Returns top 3 recommendations
        - Scores are between 0 and 100
        - Recommendations are sorted descending by score
        """
        # Create user with web development skills
        payload = {
            "name": "Ananya Roy",
            "education": "Diploma in Computer Science",
            "skills": ["HTML", "CSS", "JavaScript"],
            "interests": ["Frontend Development", "Web Applications"],
            "career_goal": "Web Developer"
        }
        create_res = self.client.post(
            "/api/users",
            data=json.dumps(payload),
            content_type="application/json"
        )
        user_id = create_res.get_json()["user"]["id"]

        # Request recommendations
        rec_res = self.client.post(f"/api/recommend/{user_id}")
        self.assertEqual(rec_res.status_code, 200)

        data = rec_res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["total_recommendations"], 3)
        self.assertEqual(len(data["recommendations"]), 3)

        recommendations = data["recommendations"]

        # Verify score bounds (0-100) and sorting
        for i in range(len(recommendations)):
            score = recommendations[i]["matching_score"]
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 100.0)

            # Check descending sort order
            if i > 0:
                prev_score = recommendations[i - 1]["matching_score"]
                self.assertGreaterEqual(prev_score, score)

        # For this profile, Web Developer should be the #1 recommendation
        top_career = recommendations[0]
        self.assertEqual(top_career["career_title"], "Web Developer")
        self.assertTrue(top_career["matches_career_goal"])

    def test_skill_gap_analysis_and_roadmap(self):
        """
        Verify missing skills identification and step-by-step roadmap generation.
        """
        # User has HTML and CSS, but lacks JavaScript, React, Node.js, Git
        payload = {
            "name": "Karan Mehra",
            "education": "B.Tech",
            "skills": ["HTML", "CSS"],
            "interests": ["Web Applications"]
        }
        create_res = self.client.post(
            "/api/users",
            data=json.dumps(payload),
            content_type="application/json"
        )
        user_id = create_res.get_json()["user"]["id"]

        rec_res = self.client.post(f"/api/recommend/{user_id}")
        recommendations = rec_res.get_json()["recommendations"]

        # Find Web Developer in recommendations
        web_dev_rec = next(
            (r for r in recommendations if r["career_title"] == "Web Developer"),
            None
        )
        self.assertIsNotNone(web_dev_rec)

        # Matched skills should contain HTML, CSS
        self.assertIn("HTML", web_dev_rec["matched_skills"])
        self.assertIn("CSS", web_dev_rec["matched_skills"])

        # Missing skills should contain React, Node.js
        self.assertIn("React", web_dev_rec["missing_skills"])
        self.assertIn("Node.js", web_dev_rec["missing_skills"])

        # Learning roadmap should provide steps for each missing skill
        roadmap = web_dev_rec["learning_roadmap"]
        self.assertIn("React", roadmap)
        self.assertIsInstance(roadmap["React"], list)
        self.assertGreaterEqual(len(roadmap["React"]), 2)

    def test_recommendation_empty_profile_scores_in_range(self):
        """
        Verify that a profile with empty skills and interests does not crash,
        and scores remain safely between 0 and 100.
        """
        payload = {
            "name": "Blank Profile User",
            "education": "",
            "skills": [],
            "interests": []
        }
        create_res = self.client.post(
            "/api/users",
            data=json.dumps(payload),
            content_type="application/json"
        )
        user_id = create_res.get_json()["user"]["id"]

        rec_res = self.client.post(f"/api/recommend/{user_id}")
        self.assertEqual(rec_res.status_code, 200)

        data = rec_res.get_json()
        recommendations = data["recommendations"]
        self.assertEqual(len(recommendations), 3)

        for rec in recommendations:
            self.assertGreaterEqual(rec["matching_score"], 0.0)
            self.assertLessEqual(rec["matching_score"], 100.0)
            self.assertEqual(rec["matched_skills"], [])

    def test_recommendation_user_not_found(self):
        """Test POST /api/recommend/<user_id> with non-existent id returns 404."""
        response = self.client.post("/api/recommend/88888")
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["status"], "error")

    def test_recommendation_data_analyst_profile(self):
        """Verify that a data-centric profile correctly scores Data Analyst highest with 100% match."""
        payload = {
            "name": "Rohan Gupta",
            "education": "B.Sc in Statistics",
            "skills": ["Python", "SQL", "Excel", "Data Visualization", "Power BI", "Statistics"],
            "interests": ["Data Analysis", "Business Intelligence", "Problem Solving", "Statistics"],
            "career_goal": "Data Analyst"
        }
        create_res = self.client.post("/api/users", data=json.dumps(payload), content_type="application/json")
        user_id = create_res.get_json()["user"]["id"]

        rec_res = self.client.post(f"/api/recommend/{user_id}")
        data = rec_res.get_json()
        top_rec = data["recommendations"][0]
        self.assertEqual(top_rec["career_title"], "Data Analyst")
        # 100% skill (50%) + 100% interest (30%) + 100% education (20%) = 100.0%
        self.assertEqual(top_rec["matching_score"], 100.0)
        self.assertEqual(len(top_rec["missing_skills"]), 0)

    def test_recommendation_ai_ml_profile(self):
        """Verify that an AI/ML profile correctly scores AI/ML Engineer highest."""
        payload = {
            "name": "Ishaan Sharma",
            "education": "Master in Data Science",
            "skills": ["Python", "Machine Learning", "Deep Learning", "Mathematics", "Statistics", "SQL"],
            "interests": ["Artificial Intelligence", "Machine Learning", "Data Science", "Research"],
            "career_goal": "AI/ML Engineer"
        }
        create_res = self.client.post("/api/users", data=json.dumps(payload), content_type="application/json")
        user_id = create_res.get_json()["user"]["id"]

        rec_res = self.client.post(f"/api/recommend/{user_id}")
        data = rec_res.get_json()
        top_rec = data["recommendations"][0]
        self.assertEqual(top_rec["career_title"], "AI/ML Engineer")
        self.assertEqual(top_rec["matching_score"], 100.0)

    def test_recommendation_cybersecurity_profile(self):
        """Verify that a security profile scores Cybersecurity Analyst highest with partial interest match."""
        payload = {
            "name": "Kavita Rao",
            "education": "B.Tech in Information Technology",
            "skills": ["Network Security", "Linux", "Ethical Hacking", "Cryptography", "Python", "SIEM"],
            "interests": ["Cybersecurity", "Network Defense"],  # 2 out of 4 interests = 50%
            "career_goal": "Cybersecurity Analyst"
        }
        create_res = self.client.post("/api/users", data=json.dumps(payload), content_type="application/json")
        user_id = create_res.get_json()["user"]["id"]

        rec_res = self.client.post(f"/api/recommend/{user_id}")
        data = rec_res.get_json()
        top_rec = data["recommendations"][0]
        self.assertEqual(top_rec["career_title"], "Cybersecurity Analyst")
        # 100% skill (50%) + 50% interest (15%) + 100% education (20%) = 85.0%
        self.assertEqual(top_rec["matching_score"], 85.0)

    def test_method_not_allowed_handlers(self):
        """Verify HTTP 405 Method Not Allowed handling."""
        # POST to /api/careers (which only accepts GET)
        res = self.client.post("/api/careers")
        self.assertEqual(res.status_code, 405)
        self.assertEqual(res.get_json()["status"], "error")


if __name__ == "__main__":
    unittest.main()

