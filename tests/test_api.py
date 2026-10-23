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
import career_data
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
        """
        Verify that a data-centric profile ranks Data Analyst first with every
        core skill matched. The benchmark skill set is wider than the student's
        six skills, so the remaining supporting skills must show up as gaps
        with a generated learning plan rather than a perfect 100% score.
        """
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
        # All four core skills matched -> 100% weighted-core coverage
        self.assertEqual(top_rec["missing_core_skills"], [])
        self.assertEqual(top_rec["score_breakdown"]["interest_match_percentage"], 100.0)
        self.assertEqual(top_rec["score_breakdown"]["education_match_percentage"], 100.0)
        self.assertGreaterEqual(top_rec["matching_score"], 90.0)
        self.assertLessEqual(top_rec["matching_score"], 100.0)
        # Supporting skills from the expanded benchmark remain as real gaps
        self.assertIn("Pandas", top_rec["missing_skills"])
        self.assertTrue(top_rec["career_path"]["learning_plan"]["phases"])

    def test_recommendation_ai_ml_profile(self):
        """Verify that an AI/ML profile ranks AI/ML Engineer first with all core skills covered."""
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
        self.assertEqual(top_rec["missing_core_skills"], [])
        self.assertTrue(top_rec["matches_career_goal"])
        self.assertGreaterEqual(top_rec["matching_score"], 80.0)
        self.assertLessEqual(top_rec["matching_score"], 100.0)
        # Readiness should reflect strong coverage
        self.assertIn(
            top_rec["career_path"]["readiness"]["level"],
            ("Job Ready", "Interview Ready")
        )

    def test_recommendation_cybersecurity_profile(self):
        """Verify that a security profile ranks Cybersecurity Analyst highest with partial interest match."""
        payload = {
            "name": "Kavita Rao",
            "education": "B.Tech in Information Technology",
            "skills": ["Network Security", "Linux", "Ethical Hacking", "Cryptography", "Python", "SIEM"],
            "interests": ["Cybersecurity", "Network Defense"],  # 2 out of 5 interests
            "career_goal": "Cybersecurity Analyst"
        }
        create_res = self.client.post("/api/users", data=json.dumps(payload), content_type="application/json")
        user_id = create_res.get_json()["user"]["id"]

        rec_res = self.client.post(f"/api/recommend/{user_id}")
        data = rec_res.get_json()
        top_rec = data["recommendations"][0]

        self.assertEqual(top_rec["career_title"], "Cybersecurity Analyst")
        self.assertEqual(top_rec["missing_core_skills"], [])
        self.assertEqual(top_rec["score_breakdown"]["education_match_percentage"], 100.0)
        # Partial interest coverage keeps this below a perfect score
        self.assertLess(top_rec["score_breakdown"]["interest_match_percentage"], 100.0)
        self.assertGreaterEqual(top_rec["matching_score"], 70.0)
        self.assertTrue(top_rec["matches_career_goal"])

    def test_method_not_allowed_handlers(self):
        """Verify HTTP 405 Method Not Allowed handling."""
        # POST to /api/careers (which only accepts GET)
        res = self.client.post("/api/careers")
        self.assertEqual(res.status_code, 405)
        self.assertEqual(res.get_json()["status"], "error")

    def test_ai_algo_in_recommendations(self):
        """Verify POST /api/recommend/<id> includes ai_algo details and human-friendly explanation."""
        payload = {
            "name": "Dev Test",
            "education": "B.Tech in Computer Science",
            "skills": ["Python", "SQL"],
            "interests": ["Data Analysis"]
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

        # Check top-level ai_algo
        self.assertIn("ai_algo", data)
        self.assertIn("name", data["ai_algo"])
        self.assertIn("Rule-Based", data["ai_algo"]["name"])
        self.assertIn("steps", data["ai_algo"])
        self.assertGreaterEqual(len(data["ai_algo"]["steps"]), 5)

        # Check career-level ai_algo_breakdown
        top_rec = data["recommendations"][0]
        self.assertIn("ai_algo_breakdown", top_rec)
        self.assertIn("bullets", top_rec["ai_algo_breakdown"])
        self.assertGreaterEqual(len(top_rec["ai_algo_breakdown"]["bullets"]), 4)


class KnowledgeBaseTestCase(unittest.TestCase):
    """
    Tests for the expanded static knowledge base in career_data.py.
    These run without the Flask client because they check the data itself.
    """

    def test_knowledge_base_is_internally_consistent(self):
        """Every career, skill, alias and ladder stage must cross-reference correctly."""
        problems = career_data.validate_knowledge_base()
        self.assertEqual(problems, [], "Knowledge base problems: {0}".format(problems))

    def test_knowledge_base_size(self):
        """The expanded knowledge base should cover many careers and skills."""
        stats = career_data.knowledge_base_stats()
        self.assertGreaterEqual(stats["total_careers"], 20)
        self.assertGreaterEqual(stats["total_skills"], 80)
        self.assertGreaterEqual(stats["total_career_stages"], 100)
        self.assertGreaterEqual(stats["total_skill_aliases"], 150)

    def test_every_career_has_five_progression_stages(self):
        """The role progression ladder powers the long-term career path."""
        for career in career_data.CAREER_DATABASE:
            stages = career["career_path"]
            self.assertEqual(
                len(stages), 5,
                "{0} should have 5 ladder stages".format(career["id"])
            )
            self.assertEqual([s["stage"] for s in stages], [1, 2, 3, 4, 5])

    def test_skill_alias_resolution(self):
        """Common short forms must resolve to canonical skill names."""
        cases = {
            "js": "JavaScript",
            " ReactJS ": "React",
            "ml": "Machine Learning",
            "k8s": "Kubernetes",
            "powerbi": "Power BI",
            "mysql": "SQL",
            "PYTHON": "Python"
        }
        for raw, expected in cases.items():
            self.assertEqual(career_data.canonical_skill(raw), expected)

        # Unknown skills are preserved rather than dropped
        self.assertEqual(career_data.canonical_skill("Quantum Welding"), "Quantum Welding")

    def test_career_goal_alias_resolution(self):
        """Job-title phrasings must map onto the right career id."""
        self.assertEqual(career_data.resolve_goal_to_career_id("ML Engineer"), "ai_ml_engineer")
        self.assertEqual(career_data.resolve_goal_to_career_id("full stack developer"), "web_developer")
        self.assertEqual(career_data.resolve_goal_to_career_id("SDET"), "qa_automation_engineer")
        self.assertIsNone(career_data.resolve_goal_to_career_id("astronaut"))


class CareerPathGenerationTestCase(unittest.TestCase):
    """Tests for the generated career path: ordering, phases, duration, ladder."""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        database.init_db("test_career_system.db")

    def tearDown(self):
        if os.path.exists("test_career_system.db"):
            try:
                os.remove("test_career_system.db")
            except PermissionError:
                pass

    def _create_user(self, payload):
        res = self.client.post(
            "/api/users",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 201)
        return res.get_json()["user"]["id"]

    def test_career_path_structure(self):
        """Each recommendation must carry a complete, usable career path."""
        user_id = self._create_user({
            "name": "Path Tester",
            "education": "B.Tech in Computer Science",
            "skills": ["HTML", "CSS"],
            "interests": ["Web Applications"],
            "career_goal": "Web Developer",
            "hours_per_week": 10
        })

        data = self.client.post(f"/api/recommend/{user_id}").get_json()
        path = data["recommendations"][0]["career_path"]

        for key in ("readiness", "learning_plan", "progression_ladder",
                    "next_actions", "market_insights", "entry_stage"):
            self.assertIn(key, path)

        plan = path["learning_plan"]
        self.assertGreater(plan["total_skills_to_learn"], 0)
        self.assertGreater(plan["total_learning_hours"], 0)
        self.assertGreater(plan["estimated_weeks"], 0)
        self.assertTrue(plan["estimated_duration"])
        self.assertLessEqual(len(plan["start_with"]), 3)

        # Phases are numbered 1..n with no gaps, and the last one is applied work
        display_numbers = [p["display_phase"] for p in plan["phases"]]
        self.assertEqual(display_numbers, list(range(1, len(display_numbers) + 1)))
        self.assertTrue(plan["phases"][-1]["portfolio_projects"])
        self.assertTrue(plan["phases"][-1]["action_steps"])

        # Every skill carries the data the UI needs to render it
        for phase in plan["phases"]:
            for skill in phase["skills"]:
                self.assertIn("difficulty", skill)
                self.assertIn("learning_hours", skill)
                self.assertTrue(skill["steps"])

    def test_learning_plan_respects_prerequisites(self):
        """A skill must never be scheduled before one of its prerequisites."""
        user_id = self._create_user({
            "name": "Prereq Tester",
            "education": "B.Tech in Computer Science",
            "skills": [],
            "interests": ["Frontend Development"],
            "career_goal": "Frontend Developer"
        })

        data = self.client.post(f"/api/recommend/{user_id}").get_json()
        rec = next(
            r for r in data["recommendations"]
            if r["career_id"] == "frontend_developer"
        )
        sequence = rec["career_path"]["learning_plan"]["skill_sequence"]
        position = {skill: index for index, skill in enumerate(sequence)}

        for skill in sequence:
            for prereq in career_data.get_skill_meta(skill)["prerequisites"]:
                if prereq in position:
                    self.assertLess(
                        position[prereq], position[skill],
                        "{0} must be scheduled before {1}".format(prereq, skill)
                    )

        # React depends on JavaScript, and CSS depends on HTML
        self.assertLess(position["JavaScript"], position["React"])
        self.assertLess(position["HTML"], position["CSS"])

    def test_missing_prerequisites_are_added_as_bridge_skills(self):
        """
        MLOps requires Docker and CI/CD, which are not AI/ML benchmark skills.
        The engine must pull them in instead of leaving an unreachable gap.
        """
        user_id = self._create_user({
            "name": "Bridge Tester",
            "education": "M.Tech in Data Science",
            "skills": ["Python", "Machine Learning", "Statistics", "Mathematics", "SQL"],
            "interests": ["Artificial Intelligence"],
            "career_goal": "ML Engineer"
        })

        res = self.client.post(f"/api/career-path/{user_id}/ai_ml_engineer")
        self.assertEqual(res.status_code, 200)
        plan = res.get_json()["evaluation"]["career_path"]["learning_plan"]

        self.assertIn("Docker", plan["bridge_skills"])
        self.assertIn("CI/CD", plan["bridge_skills"])
        # Bridge skills are scheduled before the skill that needed them
        sequence = plan["skill_sequence"]
        self.assertLess(sequence.index("Docker"), sequence.index("MLOps"))

    def test_study_pace_changes_duration_only(self):
        """More study hours per week must shorten the plan without changing its content."""
        user_id = self._create_user({
            "name": "Pace Tester",
            "education": "BCA",
            "skills": ["Python"],
            "interests": ["Data Analysis"]
        })

        slow = self.client.post(
            f"/api/recommend/{user_id}",
            data=json.dumps({"hours_per_week": 5}),
            content_type="application/json"
        ).get_json()["recommendations"][0]["career_path"]["learning_plan"]

        fast = self.client.post(
            f"/api/recommend/{user_id}",
            data=json.dumps({"hours_per_week": 20}),
            content_type="application/json"
        ).get_json()["recommendations"][0]["career_path"]["learning_plan"]

        self.assertEqual(slow["total_learning_hours"], fast["total_learning_hours"])
        self.assertEqual(slow["skill_sequence"], fast["skill_sequence"])
        self.assertGreater(slow["estimated_weeks"], fast["estimated_weeks"])

    def test_progression_ladder_marks_current_position(self):
        """The ladder must mark stage 1 as the target and later stages as future."""
        user_id = self._create_user({
            "name": "Ladder Tester",
            "education": "B.Tech in Computer Science",
            "skills": ["Python"],
            "interests": ["Coding"]
        })

        res = self.client.post(f"/api/career-path/{user_id}/software_developer")
        ladder = res.get_json()["evaluation"]["career_path"]["progression_ladder"]

        self.assertEqual(len(ladder), 5)
        self.assertIn(ladder[0]["status"], ("target", "entered"))
        self.assertEqual(ladder[1]["status"], "next")
        self.assertEqual(ladder[4]["status"], "future")
        for stage in ladder:
            self.assertTrue(stage["role"])
            self.assertTrue(stage["salary_inr"])
            self.assertTrue(stage["milestone"])

    def test_skill_aliases_count_as_matches(self):
        """Typing 'js' or 'reactjs' must score as JavaScript and React."""
        user_id = self._create_user({
            "name": "Alias Tester",
            "education": "BCA",
            "skills": ["html", "css", "js", "reactjs", "github"],
            "interests": ["Frontend Development"]
        })

        res = self.client.post(f"/api/career-path/{user_id}/frontend_developer")
        rec = res.get_json()["evaluation"]

        for skill in ("HTML", "CSS", "JavaScript", "React", "Git"):
            self.assertIn(skill, rec["matched_skills"])
        self.assertEqual(rec["missing_core_skills"], [])

    def test_prerequisites_of_known_skills_are_credited(self):
        """
        Knowing Network Security implies Computer Networking, so the engine
        must credit it instead of listing it as a gap to learn.
        """
        user_id = self._create_user({
            "name": "Implied Tester",
            "education": "B.Tech in Information Technology",
            "skills": ["Network Security", "Linux", "Ethical Hacking", "SIEM"],
            "interests": ["Cybersecurity"]
        })

        rec = self.client.post(
            f"/api/career-path/{user_id}/cybersecurity_analyst"
        ).get_json()["evaluation"]

        self.assertIn("Computer Networking", rec["matched_skills"])
        self.assertIn("Computer Networking", rec["implied_skills"])
        self.assertNotIn("Computer Networking", rec["missing_skills"])
        self.assertNotIn(
            "Computer Networking",
            rec["career_path"]["learning_plan"]["skill_sequence"]
        )

    def test_career_path_unknown_career_returns_404(self):
        """An unknown career id must return a clean 404."""
        user_id = self._create_user({"name": "X", "skills": ["Python"]})
        res = self.client.post(f"/api/career-path/{user_id}/astronaut")
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.get_json()["status"], "error")


class CatalogEndpointsTestCase(unittest.TestCase):
    """Tests for the new catalog, comparison and stateless analysis endpoints."""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        database.init_db("test_career_system.db")

    def tearDown(self):
        if os.path.exists("test_career_system.db"):
            try:
                os.remove("test_career_system.db")
            except PermissionError:
                pass

    def test_stats_endpoint(self):
        """GET /api/stats exposes knowledge base size and in-demand skills."""
        data = self.client.get("/api/stats").get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreaterEqual(data["knowledge_base"]["total_careers"], 20)
        self.assertEqual(data["consistency_problems"], [])
        self.assertTrue(data["most_in_demand_skills"])
        self.assertIn("required_by", data["most_in_demand_skills"][0])

    def test_skills_endpoint(self):
        """GET /api/skills returns skills grouped by category with metadata."""
        data = self.client.get("/api/skills").get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreaterEqual(data["total_skills"], 80)
        self.assertIn("Programming Languages", data["categories"])

        python_entry = next(
            s for s in data["categories"]["Programming Languages"]
            if s["skill"] == "Python"
        )
        self.assertEqual(python_entry["difficulty"], "Beginner")
        self.assertGreater(python_entry["learning_hours"], 0)
        self.assertGreater(python_entry["required_by_careers"], 1)

    def test_interests_and_education_endpoints(self):
        """The form catalogs must be served from the backend."""
        interests = self.client.get("/api/interests").get_json()
        self.assertGreaterEqual(interests["total_interests"], 30)
        self.assertIn("Data & AI", interests["groups"])

        education = self.client.get("/api/education-options").get_json()
        self.assertGreaterEqual(education["total_options"], 10)

    def test_career_detail_endpoint(self):
        """GET /api/careers/<id> returns one career with its full ladder."""
        data = self.client.get("/api/careers/data_engineer").get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["career"]["title"], "Data Engineer")
        self.assertEqual(len(data["career"]["career_path"]), 5)
        self.assertTrue(data["related_careers"])

        missing = self.client.get("/api/careers/not_a_career")
        self.assertEqual(missing.status_code, 404)

    def test_careers_summary_view_and_category_filter(self):
        """The catalog supports a light view and category filtering."""
        summary = self.client.get("/api/careers?view=summary").get_json()
        self.assertGreaterEqual(summary["total_careers"], 20)
        self.assertIn("top_role", summary["careers"][0])
        self.assertNotIn("career_path", summary["careers"][0])

        filtered = self.client.get("/api/careers?category=Cybersecurity").get_json()
        self.assertGreaterEqual(filtered["total_careers"], 1)
        for career in filtered["careers"]:
            self.assertEqual(career["category"], "Cybersecurity")

    def test_analyze_endpoint_without_saving(self):
        """POST /api/analyze scores a profile without creating a user row."""
        payload = {
            "education": "B.Tech in Computer Science",
            "skills": ["Python", "SQL"],
            "interests": ["Data Analysis"],
            "top_n": 5,
            "hours_per_week": 15
        }
        res = self.client.post(
            "/api/analyze",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertFalse(data["saved"])
        self.assertEqual(len(data["recommendations"]), 5)
        self.assertEqual(data["hours_per_week"], 15)
        self.assertIn("career_path", data["recommendations"][0])

    def test_analyze_endpoint_requires_input(self):
        """An empty profile is rejected with a clear validation error."""
        res = self.client.post(
            "/api/analyze",
            data=json.dumps({"skills": [], "interests": []}),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 400)

    def test_compare_endpoint(self):
        """POST /api/compare/<id> ranks the requested careers for one profile."""
        create_res = self.client.post(
            "/api/users",
            data=json.dumps({
                "name": "Compare Tester",
                "education": "B.Sc in Statistics",
                "skills": ["Python", "SQL", "Statistics"],
                "interests": ["Data Analysis"]
            }),
            content_type="application/json"
        )
        user_id = create_res.get_json()["user"]["id"]

        res = self.client.post(
            f"/api/compare/{user_id}",
            data=json.dumps({"career_ids": ["data_analyst", "data_scientist", "game_developer"]}),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["total_compared"], 3)

        scores = [c["matching_score"] for c in data["comparisons"]]
        self.assertEqual(scores, sorted(scores, reverse=True))

        bad = self.client.post(
            f"/api/compare/{user_id}",
            data=json.dumps({"career_ids": []}),
            content_type="application/json"
        )
        self.assertEqual(bad.status_code, 400)

    def test_recommend_accepts_top_n(self):
        """The number of returned careers is configurable."""
        create_res = self.client.post(
            "/api/users",
            data=json.dumps({"name": "TopN Tester", "skills": ["Python"]}),
            content_type="application/json"
        )
        user_id = create_res.get_json()["user"]["id"]

        data = self.client.post(
            f"/api/recommend/{user_id}",
            data=json.dumps({"top_n": 7}),
            content_type="application/json"
        ).get_json()

        self.assertEqual(len(data["recommendations"]), 7)
        self.assertGreaterEqual(data["careers_evaluated"], 20)


if __name__ == "__main__":
    unittest.main()

