# CareerCompass AI — Personalized Career and Skill Recommendation System

A complete, full-stack, beginner-friendly application built with **React.js, Tailwind CSS, Python Flask, and SQLite**. The system uses a **rule-based expert system** (traditional explainable AI) to analyze student skills, interests, and educational background, rank career matches, identify skill gaps, and **generate a complete career path**: a prerequisite-ordered, phased learning plan with week-by-week timelines, plus a five-stage role progression ladder.

### Five algorithms, and you choose

The system offers a choice at two independent points, then shows you what each choice would change:

| Pick one to rank careers | Pick one to order the learning |
| :--- | :--- |
| **Weighted MCDA** — 50% skills + 30% interests + 20% education *(default)* | **Topological Sort (Kahn)** — dependency order grouped into difficulty phases *(default)* |
| **Decision Tree** — walks a declared question tree: interests, then strongest skill family, then degree | **Breadth-First Search** — dependency levels: what you can start today, and what each level unlocks |
| **Naive Bayes** — P(career \| your evidence) from declared priors and likelihoods | |

`POST /api/compare-algorithms/<user_id>` runs all of them on one profile and reports which career each picks, whether they agree, and which choice suits which situation. The originals remain the defaults: a request that names no algorithm behaves exactly as it always did.

**No machine learning model, no training data, no API keys and no external AI service are used anywhere.** Every number the UI shows is produced by deterministic arithmetic and graph traversal over the static knowledge base, so the same input always produces the same output and every result can be traced to a rule.

## Knowledge base at a glance

| Item | Count |
| :--- | :--- |
| Career tracks | **21** |
| Skills mapped (difficulty, hours, prerequisites, resources) | **92** |
| Skill aliases understood (`js`, `ml`, `k8s`, `mern`...) | **242** |
| Role progression stages (5 per career) | **105** |
| Step-by-step roadmap steps | **294** |
| Career-goal job-title synonyms | **86** |
| Automated tests | **56** |

---

## 📁 Project Structure

```text
ai-skill-recommended-system-college/
├── app.py                # Main Flask application and 12 REST API endpoints (with CORS)
├── database.py           # SQLite connection, schema migration, and CRUD helpers
├── career_data.py        # Knowledge base: 21 careers, 92 skills, aliases, role ladders
├── recommender.py        # Scoring engine, gap analysis, and career path generator
├── algorithms.py         # The added engines: Decision Tree, Naive Bayes, BFS path
├── requirements.txt      # Python dependencies (Flask, flask-cors)
├── verify_backend.py     # End-to-end verification script with formatted JSON logs
├── README.md             # Comprehensive project documentation
├── tests/
│   └── test_api.py       # 56 automated unit and integration tests using unittest
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
        │   ├── CareerCard.jsx  # Recommendation card with score, gaps & career path
        │   ├── CareerPath.jsx  # Readiness meter, phase timeline, role ladder, insights
        │   ├── SkillList.jsx   # Status badges for matched/missing skills
        │   └── Loading.jsx     # Animated loading indicator
        ├── pages/
        │   ├── Home.jsx        # Landing page with live KB counters & career catalog
        │   ├── ProfileForm.jsx # Searchable categorised skill picker & study pace
        │   └── Dashboard.jsx   # Ranked matches, path controls & career explorer
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

# 2. Run backend automated tests (56 tests)
python -m unittest discover -s tests

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
The system maintains a domain knowledge base of **21 career tracks** across 10 categories:

| Category | Careers |
| :--- | :--- |
| Software Engineering | Software Developer, Frontend Developer, Backend Developer, Web Developer, Mobile App Developer, Game Developer |
| Data & Analytics | Data Analyst, Data Scientist, Data Engineer, Database Administrator |
| AI & Machine Learning | AI/ML Engineer |
| Cybersecurity | Cybersecurity Analyst |
| Cloud & Infrastructure | DevOps Engineer, Cloud Engineer, Network Engineer |
| Design & Product | UI/UX Designer |
| Quality Engineering | QA / Test Automation Engineer |
| Business & Product | Business Analyst (IT), Technical Product Manager |
| Emerging Technology | Blockchain Developer |
| Hardware & Embedded | Embedded / IoT Engineer |

Each career defines:
- **Required Skills**: the full benchmark skill set used for gap analysis.
- **Core Skills**: the must-have subset, weighted double during scoring.
- **Relevant Interests**: passion areas aligning with the role.
- **Recommended Education & Degree Keywords**: academic background criteria (including commerce, design and electronics degrees, not only CS).
- **Market data**: demand level, entry salary band (INR), growth outlook, hiring industries, everyday tools, soft skills.
- **Certifications & Portfolio Projects**: concrete proof-of-work suggestions.
- **`career_path`**: a **five-stage role progression ladder** (entry → mid → senior → lead → principal) with experience ranges, salary bands, focus, the skills each stage expects, and a milestone.

#### The Skill Library (`SKILL_LIBRARY`)
Each of the **92 skills** carries the data that makes path generation possible:
- `category`, `difficulty` (Beginner / Intermediate / Advanced)
- `learning_hours` — focused study hours needed
- `prerequisites` — **the dependency graph** the career path is built from (e.g. React → JavaScript, MLOps → Machine Learning + Docker + CI/CD)
- `resources` — free learning sources
- `roadmap` — 3-4 concrete step-by-step milestones

#### Alias Normalisation (`SKILL_ALIASES`, `CAREER_GOAL_ALIASES`)
Students never type skills the way a catalog spells them, so **242 skill aliases** and **86 job-title synonyms** are resolved before matching: `js → JavaScript`, `ml → Machine Learning`, `k8s → Kubernetes`, `mysql → SQL`, `SDET → QA / Test Automation Engineer`, `MERN developer → Web Developer`.

`validate_knowledge_base()` cross-checks the whole file (every core skill exists in its required set, every prerequisite and alias resolves, every ladder stage is complete) and is asserted by the test suite, so a typo in the data fails a test instead of silently producing a wrong roadmap.

### 2. Configurable Weights (`MATCH_WEIGHTS`)
Weights are defined centrally in `career_data.py`:
- **Skill Match**: `50%` (`0.50`)
- **Interest Match**: `30%` (`0.30`)
- **Education Match**: `20%` (`0.20`)

### 3. Algorithm 1 — Weighted Multi-Criteria Scoring (`recommender.py`)
For each career, three independent ratios are calculated:

1. **Weighted Skill Ratio ($R_{skill}$)** — core skills count `2.0`, supporting skills count `1.0`:
   $$R_{skill} = \frac{\sum \text{weights of matched required skills}}{\sum \text{weights of all required skills}}$$

2. **Interest Ratio ($R_{interest}$)**:
   $$R_{interest} = \frac{\text{Matched Interests Count}}{\text{Total Relevant Interests for Career}}$$

3. **Education Ratio ($R_{edu}$)**:
   - Full domain keyword match (e.g., Computer Science for Software Developer, Statistics for Data Analyst) = `1.0`.
   - General engineering or STEM degree = `0.75`.
   - Other degree = `0.40`.
   - Missing or empty = `0.00`.

4. **Composite Score (Normalized to 0–100)** with a `+5` bonus when the career matches the student's stated goal:
   $$\text{Final Score} = \Big( (R_{skill} \times 0.50) + (R_{interest} \times 0.30) + (R_{edu} \times 0.20) \Big) \times 100 + \text{goal bonus}$$

All scores are bounded between `0.0` and `100.0`. Missing or empty fields are handled safely without division by zero. Ties break on weighted skill coverage, then career title, so ranking is reproducible.

### 4. Skill Gap Analysis
For each career, the system identifies the difference between the career's requirements and the user's current skillset:
$$\text{Missing Skills} = \text{Required Skills} - (\text{User Skills} \cup \text{Implied Skills})$$

**Implied skills** are inferred by walking the prerequisite graph *upward* from what the student listed: someone who knows React necessarily knows JavaScript, and someone who lists Network Security has already covered Computer Networking. Without this step the engine would report those prerequisites as gaps and put them in the learning plan, which reads as nonsense to the student. Implied credits are reported separately (`implied_skills`) so the explanation stays honest.

### 5. Algorithm 2 — Career Path Generation (Prerequisite Graph Traversal)
This is what turns a score into an actionable plan:

1. **Prerequisite closure** — for every gap skill, any prerequisite the student lacks is pulled in as a **bridge skill**. Example: AI/ML Engineer requires MLOps, which needs Docker and CI/CD even though those are not AI/ML benchmark skills, so Docker, CI/CD, Linux and Git are added automatically.
2. **Topological sort** (Kahn's algorithm) — a skill never appears before its prerequisites. Ties break on `(difficulty, learning_hours, name)`, so easier, shorter wins come first and the output is deterministic.
3. **Phase assignment** — Beginner → Phase 1 (Foundations), Intermediate → Phase 2 (Core Role Skills), Advanced → Phase 3 (Specialisation), pushed later if a prerequisite landed in a later phase. Phase 4 is always applied work: portfolio projects, certifications and interview prep.
4. **Duration estimate** — `estimated_weeks = ceil(total_hours / hours_per_week)` using the pace the student chose, giving each phase a real week range (e.g. "Week 4-14").
5. **Readiness band** — weighted coverage maps onto Explorer → Foundation Builder → Developing → Interview Ready → Job Ready, with blocking core-skill gaps called out.
6. **Role progression ladder** — the career's five stages are attached, with the current position marked and the skills the student already has for each future stage ticked off.

### 6. Where the student can go next
The same engine powers three extra flows: generating the path for **any** career on demand (`/api/career-path`), **comparing** several careers side by side (`/api/compare`), and a **stateless instant analysis** that scores a profile without saving it (`/api/analyze`).

### 7. AI Algorithm Explainability (`AI Algo:-`)
Immediately following the recommendation analysis, the application presents an **`AI Algo:-`** transparency card and per-career breakdown explaining how the prediction was computed in simple, human-friendly bullet points:
- **Profile Normalization:** Standardizes skills through 242 aliases into canonical knowledge-base tokens.
- **Weighted Skill Gap Analysis (50% Impact):** Compares competencies against each benchmark set, counting must-have core skills double.
- **Interest Alignment (30% Impact):** Evaluates overlap between authentic interests and role domain focus areas.
- **Education Compatibility (20% Impact):** Matches academic degree against domain prerequisites with partial credit.
- **Score Prediction & Ranking:** Aggregates weighted criteria (plus the goal bonus) into a 0–100% fit score and ranks all 21 careers.
- **Prerequisite Graph Traversal:** Pulls in missing prerequisites as bridge skills, then topologically orders every needed skill.
- **Career Path Generation:** Groups ordered skills into phases, estimates weeks from the study pace, and attaches the role ladder.

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API status, knowledge base size and endpoint directory |
| `GET` | `/api/stats` | Knowledge base counts, algorithm description, most in-demand skills |
| `GET` | `/api/algorithms` | The 5 selectable algorithms with how each works, strengths and limits |
| `GET` | `/api/careers` | List all 21 career tracks (`?view=summary`, `?category=Cybersecurity`) |
| `GET` | `/api/careers/<career_id>` | Full detail and role progression ladder for one career |
| `GET` | `/api/skills` | 92 skills grouped by category with difficulty, hours, prerequisites |
| `GET` | `/api/interests` | Grouped interest catalog used by the profile form |
| `GET` | `/api/education-options` | Education dropdown values (kept in sync with scoring keywords) |
| `POST` | `/api/users` | Create and save user profile in SQLite |
| `GET` | `/api/users/<id>` | Retrieve saved profile by ID |
| `POST` | `/api/recommend/<id>` | Ranked recommendations with generated career paths (`top_n`, `hours_per_week`, `scoring_algorithm`, `path_algorithm`) |
| `POST` | `/api/career-path/<id>/<career_id>` | Generate the full career path for any chosen career |
| `POST` | `/api/compare/<id>` | Compare several careers side by side for the same profile |
| `POST` | `/api/compare-algorithms/<id>` | Run every algorithm on one profile and report what each choice changes |
| `POST` | `/api/analyze` | Instant analysis without saving a profile |

### Sample `POST /api/users` Payload
```json
{
  "name": "Milan Gagiya",
  "education": "Bachelor of Computer Applications (BCA)",
  "skills": ["html", "css", "js", "github"],
  "interests": ["Frontend Development", "Web Applications", "UI/UX Design"],
  "career_goal": "full stack developer",
  "hours_per_week": 15
}
```

> Note the deliberately sloppy input: `html`, `css`, `js` and `github` are resolved to **HTML, CSS, JavaScript and Git**, and the goal `full stack developer` resolves to the **Web Developer** track.

### Sample `POST /api/recommend/1` Response (trimmed)
```json
{
  "status": "success",
  "user_id": 1,
  "user_name": "Milan Gagiya",
  "hours_per_week": 15,
  "careers_evaluated": 21,
  "total_recommendations": 3,
  "scoring_weights": { "skill": 0.5, "interest": 0.3, "education": 0.2 },
  "ai_algo": {
    "name": "Rule-Based Expert System (Weighted MCDA + Prerequisite Graph)",
    "description": "An explainable heuristic algorithm ... Fully deterministic: no trained model and no external AI service is used.",
    "steps": [ "...7 steps..." ]
  },
  "recommendations": [
    {
      "career_id": "web_developer",
      "career_title": "Web Developer",
      "career_category": "Software Engineering",
      "matching_score": 80.83,
      "matches_career_goal": true,
      "score_breakdown": {
        "skill_match_percentage": 66.67,
        "interest_match_percentage": 75.0,
        "education_match_percentage": 100.0,
        "base_score": 75.83,
        "goal_bonus_points": 5.0,
        "weights_used": { "skill": "50%", "interest": "30%", "education": "20%" },
        "note": "Core skills are weighted 2x against supporting skills in the skill match."
      },
      "matched_skills": ["HTML", "CSS", "JavaScript", "Git"],
      "missing_skills": ["React", "Node.js", "MongoDB", "REST APIs"],
      "missing_core_skills": [],
      "implied_skills": [],
      "skill_gap_summary": {
        "total_required_skills": 8,
        "matched_count": 4,
        "missing_count": 4,
        "weighted_coverage_percentage": 66.67
      },
      "learning_roadmap": { "React": ["Step 1: ...", "Step 2: ..."] },
      "career_path": {
        "readiness": {
          "level": "Interview Ready",
          "skill_coverage_percentage": 66.67,
          "entry_ready": true,
          "blocking_core_skills": [],
          "message": "You have the core of this role. Close the last gaps and start applying in parallel."
        },
        "learning_plan": {
          "hours_per_week": 15,
          "total_skills_to_learn": 4,
          "skill_sequence": ["MongoDB", "REST APIs", "Node.js", "React"],
          "bridge_skills": [],
          "start_with": ["MongoDB", "REST APIs", "Node.js"],
          "total_learning_hours": 200,
          "estimated_weeks": 14,
          "estimated_months": 3.2,
          "estimated_duration": "About 3.2 months",
          "phases": [
            {
              "display_phase": 1,
              "name": "Phase 1 - Foundations",
              "goal": "Close the basic gaps so the harder topics actually make sense.",
              "starts_week": 1,
              "ends_week": 3,
              "estimated_hours": 35,
              "skills": [
                {
                  "skill": "MongoDB",
                  "difficulty": "Beginner",
                  "learning_hours": 35,
                  "prerequisites": [],
                  "is_core_skill": false,
                  "is_bridge_skill": false,
                  "steps": ["Step 1: Understand documents, collections, BSON types, and CRUD operations."],
                  "resources": ["MongoDB University M001 (free)", "MongoDB Docs"]
                }
              ]
            }
          ]
        },
        "progression_ladder": [
          {
            "stage": 1,
            "status": "entered",
            "level": "Entry",
            "role": "Junior Web Developer",
            "experience": "0 - 2 years",
            "salary_inr": "3 - 7.5 LPA",
            "focus": "Build and deploy complete small sites and features.",
            "milestone": "Deploy 3 live full-stack projects with public URLs.",
            "skills_to_add": ["React", "Node.js", "Git"],
            "skills_already_acquired": ["Git"]
          }
        ],
        "next_actions": ["Start MongoDB (Beginner, ~35 hrs): Step 1: ..."],
        "market_insights": {
          "demand": "Very High",
          "entry_salary_inr": "3 - 7.5 LPA",
          "remote_friendly": true,
          "industries": ["Digital Agencies", "Startups", "E-commerce"],
          "tools": ["VS Code", "Git & GitHub", "Vite"]
        },
        "certifications": ["Meta Full-Stack Developer (Coursera)"],
        "portfolio_projects": ["Full-stack MERN app with authentication, image upload and deployment"]
      }
    }
  ]
}
```

---

## 📮 How to Test the Application

### 1. Automated Tests
Run the 56 automated backend tests (API endpoints, scoring bounds, knowledge base consistency, prerequisite ordering, alias resolution, career path structure):
```bash
python -m unittest discover -s tests
```

### 2. End-to-End Verification Script
Prints every endpoint's response, the generated phases, the role ladder, and asserts the prerequisite ordering of the whole skill sequence:
```bash
python verify_backend.py
```

### 3. Browser Verification
1. Start Flask (`python app.py`) and Vite (`npm run dev` inside `frontend/`).
2. Navigate to `http://localhost:5173`.
3. Check that the top navbar shows **API Online**, and that the landing page counters read live from the backend (21 tracks, 92 skills, 105 role stages). Search the dark career catalog for a skill like `python` or `figma`.
4. Click **Generate My Career Path**.
5. Test validation: submit with no inputs to see the required-field alerts.
6. Fill in your name and degree, then use the skill picker: try the **search box**, the **category tabs**, and the **most in demand** quick picks. Pick interests, optionally a goal (try `SDET` or `ML Engineer`), and a **study pace**.
7. On the dashboard, inspect the fit score breakdown and skill gaps, then expand **View Generated Career Path** to see the readiness meter, the phase timeline with week ranges, the role ladder with salary bands, and field insights.
8. Change the **study pace** dropdown and confirm every timeline recalculates while the skill order stays identical.
9. Scroll to **Explore Any Other Career** and generate the path for a career outside your top matches.
