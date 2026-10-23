# CareerCompass AI — Personalized Career and Skill Recommendation System

A complete, full-stack, beginner-friendly application built with **React.js, Tailwind CSS, Python Flask, and SQLite**. The system uses a **rule-based expert system with heuristic scoring** (traditional explainable AI) to analyze student skills, interests, and educational background, recommending the top 3 career paths, identifying skill gaps, and generating personalized learning roadmaps.

---

## 📁 Project Structure

```text
ai-skill-recommended-system-college/
├── app.py                # Main Flask application and REST API endpoints (with CORS)
├── database.py           # SQLite database connection, table creation, and CRUD helpers
├── career_data.py        # Knowledge base of careers, scoring weights, and skill roadmaps
├── recommender.py        # Rule-based scoring engine, gap analysis, and roadmap generator
├── requirements.txt      # Python dependencies (Flask, flask-cors)
├── verify_backend.py     # End-to-end verification script with formatted JSON logs
├── README.md             # Comprehensive project documentation
├── tests/
│   └── test_api.py       # 18 automated unit and integration tests using unittest
└── frontend/             # React.js + Tailwind CSS Vite Application
    ├── .env.example      # Example environment variables (VITE_API_BASE_URL)
    ├── .env              # Local development environment configuration
    ├── package.json      # Node.js dependencies (React, Tailwind CSS v4, Lucide)
    ├── vite.config.js    # Vite configuration with Tailwind plugin & API proxy
    ├── index.html        # HTML entry point with metadata
    └── src/
        ├── App.jsx             # Main router & session state coordinator
        ├── index.css           # Tailwind CSS imports & global design tokens
        ├── main.jsx            # React root mount
        ├── components/
        │   ├── Navbar.jsx      # Top navigation with live backend connection badge
        │   ├── CareerCard.jsx  # Recommendation card with progress bar & roadmap
        │   ├── SkillList.jsx   # Status badges for matched/missing skills
        │   └── Loading.jsx     # Animated loading indicator
        ├── pages/
        │   ├── Home.jsx        # Hero landing page & 3-step explanation
        │   ├── ProfileForm.jsx # Student profile input form with validation
        │   └── Dashboard.jsx   # Top 3 recommendations & skill gap overview
        └── services/
            └── api.js          # Centralized Fetch API communication layer
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+** and **npm**

---

### 2. Backend Setup & Run

Open your first terminal in the project root directory:

```bash
# 1. Install backend dependencies
pip install -r requirements.txt

# 2. Run backend automated tests (18 test suites)
python -m unittest tests/test_api.py

# 3. Start the Flask backend server
python app.py
```

The Flask server will start on: **`http://127.0.0.1:5000`**  
The SQLite database `career_system.db` is initialized automatically on startup.

---

### 3. Frontend Setup & Run

Open a second terminal in the project root directory:

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Install frontend dependencies
npm install

# 3. Start the Vite development server
npm run dev
```

The frontend will start on: **`http://localhost:5173`**  
Open this URL in any web browser to use the application!

---

## 🧠 How the AI Recommendation Algorithm Works (Viva Guide)

This application implements a **Traditional AI Rule-Based Expert System** with **Heuristic Scoring**, rather than an opaque black-box machine learning model. This ensures 100% transparency, determinism, and explainability during college vivas and presentations.

### 1. The Knowledge Base (`career_data.py`)
The system maintains a domain knowledge base of 5 tech career tracks:
- **Software Developer**
- **Web Developer**
- **Data Analyst**
- **AI/ML Engineer**
- **Cybersecurity Analyst**

Each career defines:
- **Required Skills**: Core technical competencies.
- **Relevant Interests**: Passion areas aligning with the role.
- **Recommended Education & Degree Keywords**: Academic background criteria.

### 2. Configurable Weights (`MATCH_WEIGHTS`)
Weights are defined centrally in `career_data.py`:
- **Skill Match**: `50%` (`0.50`)
- **Interest Match**: `30%` (`0.30`)
- **Education Match**: `20%` (`0.20`)

### 3. The Heuristic Scoring Formula (`recommender.py`)
For each career, three independent ratios are calculated:

1. **Skill Ratio ($R_{skill}$)**:
   $$R_{skill} = \frac{\text{Matched Skills Count}}{\text{Total Required Skills for Career}}$$

2. **Interest Ratio ($R_{interest}$)**:
   $$R_{interest} = \frac{\text{Matched Interests Count}}{\text{Total Relevant Interests for Career}}$$

3. **Education Ratio ($R_{edu}$)**:
   - Full domain keyword match (e.g., Computer Science for Software Developer, Statistics for Data Analyst) = `1.0`.
   - General engineering or STEM degree = `0.75`.
   - Other degree = `0.40`.
   - Missing or empty = `0.00`.

4. **Composite Score (Normalized to 0–100)**:
   $$\text{Final Score} = \Big( (R_{skill} \times 0.50) + (R_{interest} \times 0.30) + (R_{edu} \times 0.20) \Big) \times 100$$

All scores are bounded between `0.0` and `100.0`. Missing or empty fields are handled safely without division by zero.

### 4. Skill Gap Analysis
For each recommended career, the system identifies the difference between the career's requirements and the user's current skillset:
$$\text{Missing Skills} = \text{Required Skills} - \text{User Skills}$$

### 6. AI Algorithm Explainability (`AI Algo:-`)
Immediately following the recommendation analysis, the application presents an **`AI Algo:-`** transparency card and per-career breakdown explaining how the prediction was computed in simple, human-friendly bullet points:
- **Profile Normalization:** Standardizes skills, interests, and degrees into clean tokens.
- **Skill Gap Analysis (50% Impact):** Compares user competencies with industry benchmarks to identify matched strengths and missing gaps.
- **Interest Alignment (30% Impact):** Evaluates semantic overlap between authentic interests and role domain focus areas.
- **Education Compatibility (20% Impact):** Matches academic degree against domain prerequisites.
- **Score Calculation & Ranking:** Aggregates weighted criteria into a 0–100% fit score and ranks the top career paths.
- **Roadmap Synthesis:** Constructs sequential milestones for every missing skill.

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API status and endpoint directory |
| `GET` | `/api/careers` | List available careers and required skills |
| `POST` | `/api/users` | Create and save user profile in SQLite |
| `GET` | `/api/users/<id>` | Retrieve saved profile by ID |
| `POST` | `/api/recommend/<id>` | Generate top 3 recommendations, AI Algo breakdown & roadmap |

### Sample `POST /api/users` Payload
```json
{
  "name": "Milan Gagiya",
  "education": "Bachelor of Technology in Computer Science",
  "skills": ["Python", "SQL", "Git", "Machine Learning"],
  "interests": ["Artificial Intelligence", "Machine Learning", "Problem Solving"],
  "career_goal": "AI/ML Engineer"
}
```

### Sample `POST /api/recommend/1` Response
```json
{
  "status": "success",
  "total_recommendations": 3,
  "user_id": 1,
  "user_name": "Milan Gagiya",
  "ai_algo": {
    "name": "Rule-Based Expert System (Weighted Multi-Criteria Decision Analysis)",
    "description": "An explainable heuristic algorithm that analyzes competencies, interests, and academic background to predict optimal career pathways and identify skill gaps.",
    "steps": [ ... ]
  },
  "recommendations": [
    {
      "career_id": "ai_ml_engineer",
      "career_title": "AI/ML Engineer",
      "matching_score": 68.33,
      "matches_career_goal": true,
      "score_breakdown": {
        "skill_match_percentage": 50.0,
        "interest_match_percentage": 75.0,
        "education_match_percentage": 100.0,
        "weights_used": { "skill": "50%", "interest": "30%", "education": "20%" }
      },
      "ai_algo_breakdown": {
        "algorithm": "Rule-Based Skill Gap Analysis & Heuristic MCDA",
        "bullets": [ ... ]
      },
      "matched_skills": ["Python", "Machine Learning"],
      "missing_skills": ["Deep Learning", "Mathematics", "Statistics", "SQL"],
      "learning_roadmap": { ... }
    }
  ]
}
```

---

## 📮 How to Test the Application

### 1. Automated Tests
Run the 19 automated backend test suites:
```bash
python -m unittest tests/test_api.py
```

### 2. Browser Verification
1. Start Flask (`python app.py`) and Vite (`npm run dev` inside `frontend/`).
2. Navigate to `http://localhost:5173`.
3. Check that the top navbar shows **API Online**.
4. Click **Find My Career**.
5. Test validation: Click **Generate Recommendations** without inputs to see required alerts.
6. Fill in your name, select education, choose skills & interests, and submit.
7. Inspect the top 3 cards, score progress bars, skill gap badges, and click **View Learning Roadmap** to expand your milestone plan.
