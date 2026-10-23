"""
career_data.py
--------------
Static knowledge base for the AI-powered career & skill recommendation system.

Contents
--------
1. Tuning constants   : matching weights, goal bonus, study pace, phase blueprint
2. SKILL_LIBRARY      : ~85 skills with category, difficulty, learning hours,
                        prerequisites, free resources and step-by-step roadmaps
3. SKILL_ALIASES      : common spellings/short forms mapped to canonical skills
4. CAREER_DATABASE    : 20 career tracks, each with required/core skills,
                        interests, education keywords, market data, tools,
                        certifications, portfolio projects and a 5-stage
                        role progression ladder (career_path)
5. INTEREST_LIBRARY   : grouped interest catalog used by the profile form
6. Derived lookups    : SKILL_ROADMAPS, SKILL_CATEGORIES, CAREER_INDEX, ...

Notes
-----
* Salary figures are indicative India-market ranges (LPA = lakh per annum) and
  are meant for guidance inside this academic project, not as hiring advice.
* `prerequisites` drive the generated career path: the recommender orders the
  learning plan so that a skill never appears before the skills it depends on.
"""

# ==========================================
# 1. Tuning Constants
# ==========================================
# Skill match = 50%, Interest match = 30%, Education match = 20%
# All weights sum up to 1.0 (100%)
MATCH_WEIGHTS = {
    "skill": 0.50,
    "interest": 0.30,
    "education": 0.20
}

# A career that matches the student's stated goal gets a small nudge so that
# an explicitly chosen target is not buried behind a near-identical track.
GOAL_BONUS_POINTS = 5.0

# Core skills are non-negotiable for a role, supporting skills are "nice to
# have". Weighted skill matching makes the fit score far more realistic.
CORE_SKILL_WEIGHT = 2.0
SUPPORTING_SKILL_WEIGHT = 1.0

# Study pace assumed when converting learning hours into weeks/months.
DEFAULT_HOURS_PER_WEEK = 10
MIN_HOURS_PER_WEEK = 2
MAX_HOURS_PER_WEEK = 60

# Difficulty is used to sequence the generated learning phases.
DIFFICULTY_ORDER = {
    "Beginner": 1,
    "Intermediate": 2,
    "Advanced": 3
}

# Blueprint for the generated learning path. Beginner skills land in phase 1,
# intermediate in phase 2, advanced in phase 3; phase 4 is always applied work.
PHASE_BLUEPRINT = [
    {
        "phase": 1,
        "name": "Phase 1 - Foundations",
        "difficulty": "Beginner",
        "goal": "Close the basic gaps so the harder topics actually make sense."
    },
    {
        "phase": 2,
        "name": "Phase 2 - Core Role Skills",
        "difficulty": "Intermediate",
        "goal": "Build the day-to-day working skills this role is hired for."
    },
    {
        "phase": 3,
        "name": "Phase 3 - Specialisation",
        "difficulty": "Advanced",
        "goal": "Add the depth that separates an intern from a hireable junior."
    },
    {
        "phase": 4,
        "name": "Phase 4 - Portfolio & Job Readiness",
        "difficulty": None,
        "goal": "Turn the new skills into proof: projects, certificates, interviews."
    }
]

# Generic job-readiness steps appended as the final phase of every career path.
JOB_READINESS_STEPS = [
    "Ship 2-3 portfolio projects from the list below and host them publicly (GitHub + live demo).",
    "Write a one-page README per project explaining the problem, your approach and the result.",
    "Rebuild your resume around the matched skills and quantified project outcomes.",
    "Practise 40-50 role-specific interview questions plus 15 DSA/aptitude problems.",
    "Apply to internships and entry roles weekly, and ask for feedback on every rejection."
]


# ==========================================
# 2. Skill Library (single source of truth)
# ==========================================
# Every entry: category, difficulty, learning_hours (focused study hours),
# prerequisites (other skills in this library), free resources, roadmap steps.
SKILL_LIBRARY = {

    # ---------- Programming Languages ----------
    "Python": {
        "category": "Programming Languages",
        "difficulty": "Beginner",
        "learning_hours": 60,
        "prerequisites": [],
        "resources": ["Official Python Tutorial (docs.python.org)", "freeCodeCamp Python Course", "HackerRank Python Track"],
        "roadmap": [
            "Step 1: Master Python fundamentals (variables, loops, conditionals, functions, lists/dictionaries).",
            "Step 2: Learn Object-Oriented Programming (classes, objects, inheritance) and file I/O operations.",
            "Step 3: Practise standard library modules (json, datetime, os, re) and virtual environments with pip.",
            "Step 4: Build a practical CLI project (e.g., student management system or web scraper)."
        ]
    },
    "Java": {
        "category": "Programming Languages",
        "difficulty": "Beginner",
        "learning_hours": 80,
        "prerequisites": [],
        "resources": ["Oracle Java Tutorials", "Java Brains (YouTube)", "Codewars Java kata"],
        "roadmap": [
            "Step 1: Learn Java syntax, primitive types, and control flow.",
            "Step 2: Understand core OOP principles, Java Collections Framework (ArrayList, HashMap), and exception handling.",
            "Step 3: Learn generics, streams, lambda expressions, and multithreading basics.",
            "Step 4: Build a console application and explore build tools like Maven or Gradle."
        ]
    },
    "JavaScript": {
        "category": "Programming Languages",
        "difficulty": "Beginner",
        "learning_hours": 70,
        "prerequisites": [],
        "resources": ["MDN JavaScript Guide", "javascript.info", "freeCodeCamp JS Algorithms"],
        "roadmap": [
            "Step 1: Learn JavaScript syntax, variables (let/const), functions, arrays, and objects.",
            "Step 2: Master DOM manipulation, event handling, and ES6+ features (arrow functions, destructuring, promises).",
            "Step 3: Learn Fetch API / async-await, modules, and error handling.",
            "Step 4: Build an interactive project like a Weather App or expense tracker without any framework."
        ]
    },
    "TypeScript": {
        "category": "Programming Languages",
        "difficulty": "Intermediate",
        "learning_hours": 40,
        "prerequisites": ["JavaScript"],
        "resources": ["TypeScript Handbook (typescriptlang.org)", "Total TypeScript free tutorials"],
        "roadmap": [
            "Step 1: Learn primitive type annotations, union types, arrays, and type inference.",
            "Step 2: Master interfaces, type aliases, generics, and utility types (Partial, Pick, Record).",
            "Step 3: Configure tsconfig.json with strict mode and migrate an existing JS project to TypeScript."
        ]
    },
    "C++": {
        "category": "Programming Languages",
        "difficulty": "Intermediate",
        "learning_hours": 90,
        "prerequisites": [],
        "resources": ["learncpp.com", "cppreference.com", "GeeksforGeeks C++ STL"],
        "roadmap": [
            "Step 1: Learn C++ syntax, data types, pointers, references, and memory layout.",
            "Step 2: Master classes, constructors/destructors, operator overloading, and RAII.",
            "Step 3: Learn the STL (vector, map, set, algorithms) and practise competitive problems.",
            "Step 4: Build a performance-sensitive project (e.g., 2D game loop or file compression tool)."
        ]
    },
    "C#": {
        "category": "Programming Languages",
        "difficulty": "Intermediate",
        "learning_hours": 70,
        "prerequisites": [],
        "resources": ["Microsoft Learn C# Path", "C# Yellow Book (free PDF)"],
        "roadmap": [
            "Step 1: Learn C# syntax, value vs reference types, and .NET project structure.",
            "Step 2: Master OOP in C#, LINQ queries, collections, and async/await.",
            "Step 3: Build a small .NET console tool or Unity script library applying these concepts."
        ]
    },
    "Kotlin": {
        "category": "Programming Languages",
        "difficulty": "Intermediate",
        "learning_hours": 60,
        "prerequisites": ["Java"],
        "resources": ["Kotlin Docs (kotlinlang.org)", "Android Basics with Compose (free)"],
        "roadmap": [
            "Step 1: Learn Kotlin syntax, null safety, data classes, and extension functions.",
            "Step 2: Understand coroutines for asynchronous work and the Kotlin collections API.",
            "Step 3: Build an Android screen with Jetpack Compose and a ViewModel."
        ]
    },
    "Embedded C": {
        "category": "Hardware & Embedded",
        "difficulty": "Intermediate",
        "learning_hours": 80,
        "prerequisites": [],
        "resources": ["Embedded C Coding Standard (Barr Group)", "Modern Embedded Systems Programming (YouTube)"],
        "roadmap": [
            "Step 1: Learn C fundamentals with emphasis on pointers, bit manipulation, and fixed-width types.",
            "Step 2: Understand memory-mapped registers, volatile, interrupts (ISR), and polling vs interrupt design.",
            "Step 3: Write bare-metal GPIO/UART/timer drivers for a development board without using libraries."
        ]
    },
    "Solidity": {
        "category": "Blockchain & Web3",
        "difficulty": "Advanced",
        "learning_hours": 70,
        "prerequisites": ["JavaScript", "Blockchain Fundamentals"],
        "resources": ["CryptoZombies", "Solidity Docs", "ethereum.org developer portal"],
        "roadmap": [
            "Step 1: Learn Solidity syntax, state variables, functions, modifiers, and events.",
            "Step 2: Understand gas costs, storage vs memory, mappings, and inheritance patterns.",
            "Step 3: Write and unit-test contracts with Hardhat/Foundry and deploy to a public testnet."
        ]
    },

    # ---------- Computer Science Fundamentals ----------
    "Data Structures & Algorithms": {
        "category": "Computer Science Fundamentals",
        "difficulty": "Intermediate",
        "learning_hours": 120,
        "prerequisites": [],
        "resources": ["NeetCode roadmap", "LeetCode Top Interview 150", "GeeksforGeeks DSA self-paced"],
        "roadmap": [
            "Step 1: Study linear data structures (arrays, linked lists, stacks, queues).",
            "Step 2: Learn non-linear structures (trees, binary search trees, heaps, graphs) and Big-O notation.",
            "Step 3: Practise sorting, searching, two pointers, and recursion problems on LeetCode/HackerRank.",
            "Step 4: Learn dynamic programming and graph traversal patterns (BFS, DFS, Dijkstra)."
        ]
    },
    "Operating Systems": {
        "category": "Computer Science Fundamentals",
        "difficulty": "Intermediate",
        "learning_hours": 50,
        "prerequisites": [],
        "resources": ["Operating Systems: Three Easy Pieces (free book)", "Neso Academy OS playlist"],
        "roadmap": [
            "Step 1: Understand processes vs threads, context switching, and CPU scheduling algorithms.",
            "Step 2: Learn memory management (paging, virtual memory) and concurrency (mutex, semaphore, deadlock).",
            "Step 3: Relate theory to practice by inspecting live processes and memory usage on Linux."
        ]
    },
    "Computer Networking": {
        "category": "Computer Science Fundamentals",
        "difficulty": "Beginner",
        "learning_hours": 50,
        "prerequisites": [],
        "resources": ["Computer Networking: A Top-Down Approach", "Cisco Networking Basics (free)"],
        "roadmap": [
            "Step 1: Learn the OSI/TCP-IP layers, IP addressing, subnetting, and common ports.",
            "Step 2: Understand DNS, DHCP, NAT, HTTP/HTTPS, and TCP vs UDP behaviour.",
            "Step 3: Capture and read real traffic in Wireshark, and trace one request end-to-end."
        ]
    },
    "System Design": {
        "category": "Computer Science Fundamentals",
        "difficulty": "Advanced",
        "learning_hours": 90,
        "prerequisites": ["REST APIs", "SQL"],
        "resources": ["System Design Primer (GitHub)", "ByteByteGo blog", "Designing Data-Intensive Applications"],
        "roadmap": [
            "Step 1: Learn the building blocks: load balancers, caching, queues, replication, sharding.",
            "Step 2: Understand CAP theorem, consistency models, idempotency, and rate limiting.",
            "Step 3: Practise designing 8-10 systems end to end (URL shortener, feed, chat, ride hailing).",
            "Step 4: Document one design with capacity estimates and trade-offs you can defend in an interview."
        ]
    },
    "Mathematics": {
        "category": "Computer Science Fundamentals",
        "difficulty": "Intermediate",
        "learning_hours": 80,
        "prerequisites": [],
        "resources": ["3Blue1Brown Linear Algebra", "Khan Academy Multivariable Calculus", "MIT 18.06 lectures"],
        "roadmap": [
            "Step 1: Review Linear Algebra fundamentals (vectors, matrices, matrix multiplication, dot products).",
            "Step 2: Understand Multivariable Calculus (derivatives, partial derivatives, gradients, gradient descent).",
            "Step 3: Study Probability Theory and basic optimization techniques used in ML."
        ]
    },
    "Statistics": {
        "category": "Data & Analytics",
        "difficulty": "Beginner",
        "learning_hours": 60,
        "prerequisites": [],
        "resources": ["Khan Academy Statistics", "StatQuest (YouTube)", "OpenIntro Statistics (free book)"],
        "roadmap": [
            "Step 1: Study descriptive statistics (mean, median, mode, variance, standard deviation).",
            "Step 2: Understand probability distributions (normal distribution, binomial) and central limit theorem.",
            "Step 3: Learn inferential statistics: hypothesis testing (p-value, t-test, chi-square test, A/B testing)."
        ]
    },

    # ---------- Web & Frontend ----------
    "HTML": {
        "category": "Web & Frontend",
        "difficulty": "Beginner",
        "learning_hours": 25,
        "prerequisites": [],
        "resources": ["MDN HTML Basics", "web.dev Learn HTML"],
        "roadmap": [
            "Step 1: Learn HTML5 document structure, semantic tags (header, nav, section, footer), and text elements.",
            "Step 2: Master forms, input validation types, tables, and multimedia tags (audio, video).",
            "Step 3: Build a semantic, accessible multi-page personal portfolio skeleton."
        ]
    },
    "CSS": {
        "category": "Web & Frontend",
        "difficulty": "Beginner",
        "learning_hours": 40,
        "prerequisites": ["HTML"],
        "resources": ["MDN CSS Guide", "CSS-Tricks Flexbox & Grid guides", "Flexbox Froggy"],
        "roadmap": [
            "Step 1: Understand the CSS box model, selectors, specificity, typography, and colors.",
            "Step 2: Master Flexbox and CSS Grid layout systems for responsive design.",
            "Step 3: Learn CSS transitions, custom properties, media queries, and style your portfolio beautifully."
        ]
    },
    "Tailwind CSS": {
        "category": "Web & Frontend",
        "difficulty": "Beginner",
        "learning_hours": 20,
        "prerequisites": ["CSS"],
        "resources": ["Tailwind CSS Docs", "Tailwind Play sandbox"],
        "roadmap": [
            "Step 1: Learn the utility-first approach, spacing/colour scales, and responsive prefixes.",
            "Step 2: Master layout utilities, state variants (hover, focus), and dark mode.",
            "Step 3: Rebuild one existing CSS page in Tailwind and extract reusable component patterns."
        ]
    },
    "React": {
        "category": "Web & Frontend",
        "difficulty": "Intermediate",
        "learning_hours": 70,
        "prerequisites": ["JavaScript"],
        "resources": ["react.dev Learn", "Scrimba Learn React (free)"],
        "roadmap": [
            "Step 1: Understand React JSX syntax, components, props, and component state.",
            "Step 2: Master React Hooks (useState, useEffect, useContext) and handling events.",
            "Step 3: Learn lists/keys, conditional rendering, forms, and data fetching patterns.",
            "Step 4: Build a full single-page application with routing and component-driven architecture."
        ]
    },
    "Accessibility (a11y)": {
        "category": "Web & Frontend",
        "difficulty": "Intermediate",
        "learning_hours": 25,
        "prerequisites": ["HTML"],
        "resources": ["WAI-ARIA Authoring Practices", "web.dev Accessibility course", "WAVE browser extension"],
        "roadmap": [
            "Step 1: Learn WCAG principles, semantic landmarks, alt text, and colour contrast rules.",
            "Step 2: Master keyboard navigation, focus management, labels, and ARIA roles for custom widgets.",
            "Step 3: Audit a real page with WAVE/Lighthouse and a screen reader, then fix every finding."
        ]
    },
    "React Native": {
        "category": "Mobile Development",
        "difficulty": "Intermediate",
        "learning_hours": 60,
        "prerequisites": ["React"],
        "resources": ["React Native Docs", "Expo Docs & tutorial"],
        "roadmap": [
            "Step 1: Set up Expo, understand core components (View, Text, FlatList) and native styling.",
            "Step 2: Learn navigation, device APIs (camera, storage, notifications), and platform differences.",
            "Step 3: Build and publish a two-screen app to an internal test track on the Play Store."
        ]
    },
    "Flutter": {
        "category": "Mobile Development",
        "difficulty": "Intermediate",
        "learning_hours": 70,
        "prerequisites": [],
        "resources": ["Flutter Docs codelabs", "Dart language tour", "Flutter Apprentice (free chapters)"],
        "roadmap": [
            "Step 1: Learn Dart basics (null safety, futures, classes) and the widget tree model.",
            "Step 2: Master stateful widgets, layout widgets, navigation, and a state solution (Provider/Riverpod).",
            "Step 3: Connect to a REST API, handle offline storage, and build a release APK."
        ]
    },

    # ---------- Backend & APIs ----------
    "Node.js": {
        "category": "Backend & APIs",
        "difficulty": "Intermediate",
        "learning_hours": 60,
        "prerequisites": ["JavaScript"],
        "resources": ["Node.js Docs", "Express Guide", "The Odin Project Node path"],
        "roadmap": [
            "Step 1: Understand the Node.js runtime, npm, the event loop, and asynchronous programming.",
            "Step 2: Build RESTful APIs using Express.js with routing, middleware, and validation.",
            "Step 3: Connect Express to a database (MongoDB or SQLite) and implement full CRUD with error handling."
        ]
    },
    "REST APIs": {
        "category": "Backend & APIs",
        "difficulty": "Intermediate",
        "learning_hours": 35,
        "prerequisites": [],
        "resources": ["restfulapi.net tutorial", "Swagger/OpenAPI docs", "Postman Learning Center"],
        "roadmap": [
            "Step 1: Learn HTTP verbs, status codes, resource naming, and request/response structure.",
            "Step 2: Design paginated, filterable endpoints with proper error payloads and versioning.",
            "Step 3: Document an API with OpenAPI/Swagger and test every endpoint in Postman."
        ]
    },
    "Spring Boot": {
        "category": "Backend & APIs",
        "difficulty": "Advanced",
        "learning_hours": 70,
        "prerequisites": ["Java", "REST APIs"],
        "resources": ["spring.io guides", "Spring Boot Reference Docs"],
        "roadmap": [
            "Step 1: Learn dependency injection, Spring Boot starters, and application configuration.",
            "Step 2: Build REST controllers with Spring Data JPA repositories and bean validation.",
            "Step 3: Add Spring Security (JWT), global exception handling, and JUnit + MockMvc tests."
        ]
    },
    "Microservices": {
        "category": "Backend & APIs",
        "difficulty": "Advanced",
        "learning_hours": 60,
        "prerequisites": ["REST APIs", "Docker"],
        "resources": ["microservices.io patterns", "Microsoft .NET Microservices e-book (free)"],
        "roadmap": [
            "Step 1: Understand service boundaries, API gateways, and service discovery.",
            "Step 2: Learn inter-service communication (sync REST vs async events) and resilience patterns.",
            "Step 3: Split one monolith project into two services with a gateway and shared observability."
        ]
    },
    "Authentication & Authorization": {
        "category": "Backend & APIs",
        "difficulty": "Intermediate",
        "learning_hours": 30,
        "prerequisites": ["REST APIs"],
        "resources": ["OWASP Authentication Cheat Sheet", "jwt.io introduction", "OAuth 2.0 Simplified"],
        "roadmap": [
            "Step 1: Learn password hashing (bcrypt/argon2), sessions vs tokens, and secure cookie flags.",
            "Step 2: Implement JWT access/refresh token flows and role-based access control.",
            "Step 3: Add OAuth2/social login and protect endpoints against the OWASP authentication failures."
        ]
    },

    # ---------- Databases ----------
    "SQL": {
        "category": "Databases",
        "difficulty": "Beginner",
        "learning_hours": 50,
        "prerequisites": [],
        "resources": ["SQLBolt", "Mode SQL Tutorial", "PostgreSQL Tutorial"],
        "roadmap": [
            "Step 1: Learn relational database basics and basic SQL queries (SELECT, WHERE, ORDER BY, LIMIT).",
            "Step 2: Master aggregate functions, GROUP BY, HAVING, and table JOINs (INNER, LEFT, RIGHT).",
            "Step 3: Learn subqueries, CTEs, and window functions (ROW_NUMBER, RANK, running totals).",
            "Step 4: Practise schema design and indexing with SQLite or PostgreSQL on a real dataset."
        ]
    },
    "Database Design": {
        "category": "Databases",
        "difficulty": "Intermediate",
        "learning_hours": 40,
        "prerequisites": ["SQL"],
        "resources": ["Database Design for Mere Mortals", "Vertabelo ER modelling articles"],
        "roadmap": [
            "Step 1: Learn entity-relationship modelling, primary/foreign keys, and cardinality.",
            "Step 2: Apply normalisation (1NF-3NF) and know when denormalisation is the right call.",
            "Step 3: Design and implement a 10+ table schema with constraints, indexes, and sample queries."
        ]
    },
    "MongoDB": {
        "category": "Databases",
        "difficulty": "Beginner",
        "learning_hours": 35,
        "prerequisites": [],
        "resources": ["MongoDB University M001 (free)", "MongoDB Docs"],
        "roadmap": [
            "Step 1: Understand documents, collections, BSON types, and CRUD operations.",
            "Step 2: Learn schema design patterns (embed vs reference), indexes, and the aggregation pipeline.",
            "Step 3: Connect MongoDB Atlas to an application and model one real feature end to end."
        ]
    },
    "Data Warehousing": {
        "category": "Data Engineering",
        "difficulty": "Advanced",
        "learning_hours": 50,
        "prerequisites": ["SQL"],
        "resources": ["The Data Warehouse Toolkit (Kimball)", "dbt Learn (free)"],
        "roadmap": [
            "Step 1: Learn OLTP vs OLAP, star/snowflake schemas, facts, and dimensions.",
            "Step 2: Understand slowly changing dimensions, partitioning, and columnar storage.",
            "Step 3: Build a small warehouse layer (staging to marts) with dbt on BigQuery or PostgreSQL."
        ]
    },
    "Database Administration": {
        "category": "Databases",
        "difficulty": "Advanced",
        "learning_hours": 70,
        "prerequisites": ["SQL", "Linux"],
        "resources": ["PostgreSQL Administration Docs", "Use The Index, Luke!"],
        "roadmap": [
            "Step 1: Learn installation, configuration, users/roles, and privilege management.",
            "Step 2: Master backup & restore, point-in-time recovery, replication, and high availability.",
            "Step 3: Practise performance tuning: EXPLAIN plans, index strategy, vacuum/statistics, slow query logs."
        ]
    },

    # ---------- Data & Analytics ----------
    "Excel": {
        "category": "Data & Analytics",
        "difficulty": "Beginner",
        "learning_hours": 30,
        "prerequisites": [],
        "resources": ["Microsoft Excel Training Center", "ExcelJet formula reference"],
        "roadmap": [
            "Step 1: Master basic Excel formulas (SUM, AVERAGE, COUNTIF) and data formatting.",
            "Step 2: Learn lookup functions (VLOOKUP, XLOOKUP, INDEX/MATCH) and conditional formatting.",
            "Step 3: Build dynamic Pivot Tables and interactive summary dashboards."
        ]
    },
    "Data Visualization": {
        "category": "Data & Analytics",
        "difficulty": "Beginner",
        "learning_hours": 40,
        "prerequisites": [],
        "resources": ["Storytelling with Data", "Matplotlib & Seaborn galleries", "Financial Times Visual Vocabulary"],
        "roadmap": [
            "Step 1: Learn data visualization principles (choosing the right chart for the data type).",
            "Step 2: Practise creating bar charts, line plots, heatmaps, and scatter plots in Matplotlib and Seaborn.",
            "Step 3: Learn labelling, colour, and annotation choices that make a chart readable without explanation.",
            "Step 4: Build an end-to-end exploratory data visualization report on an open dataset."
        ]
    },
    "Power BI": {
        "category": "Data & Analytics",
        "difficulty": "Intermediate",
        "learning_hours": 45,
        "prerequisites": ["Excel"],
        "resources": ["Microsoft Learn Power BI path", "SQLBI DAX guide"],
        "roadmap": [
            "Step 1: Learn the Power BI Desktop interface and importing data from CSV/Excel/SQL.",
            "Step 2: Perform data cleaning with Power Query and write basic DAX measures.",
            "Step 3: Design interactive business intelligence dashboards with drill-downs, slicers, and bookmarks."
        ]
    },
    "Tableau": {
        "category": "Data & Analytics",
        "difficulty": "Intermediate",
        "learning_hours": 35,
        "prerequisites": ["Data Visualization"],
        "resources": ["Tableau Public free training videos", "Makeover Monday challenges"],
        "roadmap": [
            "Step 1: Learn Tableau Public, data connections, dimensions vs measures, and shelves.",
            "Step 2: Build calculated fields, parameters, sets, and level-of-detail expressions.",
            "Step 3: Publish an interactive dashboard to Tableau Public and add it to your portfolio."
        ]
    },
    "Pandas": {
        "category": "Data & Analytics",
        "difficulty": "Intermediate",
        "learning_hours": 40,
        "prerequisites": ["Python"],
        "resources": ["Pandas User Guide", "Kaggle Pandas micro-course"],
        "roadmap": [
            "Step 1: Learn Series/DataFrame creation, indexing, selection, and reading CSV/Excel/SQL sources.",
            "Step 2: Master cleaning (missing values, dtypes, duplicates), groupby, merge, and pivot operations.",
            "Step 3: Do a full exploratory data analysis notebook on a messy real-world dataset."
        ]
    },
    "NumPy": {
        "category": "Data & Analytics",
        "difficulty": "Intermediate",
        "learning_hours": 25,
        "prerequisites": ["Python"],
        "resources": ["NumPy Absolute Beginners Guide", "Kaggle intro notebooks"],
        "roadmap": [
            "Step 1: Learn ndarray creation, dtypes, shape, indexing, and slicing.",
            "Step 2: Master vectorised operations, broadcasting, and aggregation along axes.",
            "Step 3: Re-implement a loop-heavy computation as vectorised NumPy and compare the runtime."
        ]
    },
    "A/B Testing": {
        "category": "Data & Analytics",
        "difficulty": "Intermediate",
        "learning_hours": 25,
        "prerequisites": ["Statistics"],
        "resources": ["Trustworthy Online Controlled Experiments", "Evan Miller's A/B tools"],
        "roadmap": [
            "Step 1: Learn hypothesis framing, metric selection (primary vs guardrail), and randomisation.",
            "Step 2: Understand sample size, statistical power, p-values, confidence intervals, and peeking bias.",
            "Step 3: Analyse a public experiment dataset and write a go/no-go recommendation memo."
        ]
    },
    "Business Requirement Analysis": {
        "category": "Business & Product",
        "difficulty": "Intermediate",
        "learning_hours": 40,
        "prerequisites": [],
        "resources": ["BABOK Guide overview", "IIBA free webinars"],
        "roadmap": [
            "Step 1: Learn elicitation techniques: interviews, workshops, document analysis, observation.",
            "Step 2: Write clear functional/non-functional requirements, user stories, and acceptance criteria.",
            "Step 3: Produce a complete BRD/SRS for a real campus process and get it reviewed by a stakeholder."
        ]
    },
    "Process Modeling (BPMN)": {
        "category": "Business & Product",
        "difficulty": "Intermediate",
        "learning_hours": 30,
        "prerequisites": [],
        "resources": ["BPMN 2.0 Quick Guide (Camunda)", "bpmn.io free modeller"],
        "roadmap": [
            "Step 1: Learn BPMN core elements: events, activities, gateways, pools, and lanes.",
            "Step 2: Model an as-is process, find bottlenecks, and design the to-be process.",
            "Step 3: Document one process improvement with before/after metrics and effort estimates."
        ]
    },
    "Stakeholder Management": {
        "category": "Business & Product",
        "difficulty": "Intermediate",
        "learning_hours": 25,
        "prerequisites": [],
        "resources": ["Atlassian Team Playbook", "Harvard Business Review communication articles"],
        "roadmap": [
            "Step 1: Learn stakeholder mapping (power/interest grid) and RACI responsibility matrices.",
            "Step 2: Practise running structured meetings, written status updates, and conflict resolution.",
            "Step 3: Lead one college/club project end to end and keep a written decision log."
        ]
    },
    "Agile & Scrum": {
        "category": "Business & Product",
        "difficulty": "Beginner",
        "learning_hours": 20,
        "prerequisites": [],
        "resources": ["Scrum Guide (free)", "Atlassian Agile Coach"],
        "roadmap": [
            "Step 1: Learn the Agile manifesto, Scrum roles, artefacts, and the five ceremonies.",
            "Step 2: Understand backlog refinement, story points, velocity, and burndown charts.",
            "Step 3: Run a two-week sprint with your project team, including a real retrospective."
        ]
    },
    "Jira": {
        "category": "Business & Product",
        "difficulty": "Beginner",
        "learning_hours": 12,
        "prerequisites": [],
        "resources": ["Atlassian Jira free tier + tutorials"],
        "roadmap": [
            "Step 1: Set up a free Jira project with issue types, workflows, and a Scrum board.",
            "Step 2: Learn epics, sprints, JQL filters, and dashboard gadgets.",
            "Step 3: Track an actual project in Jira for one month and export a sprint report."
        ]
    },
    "Product Roadmapping": {
        "category": "Business & Product",
        "difficulty": "Intermediate",
        "learning_hours": 30,
        "prerequisites": ["Agile & Scrum"],
        "resources": ["Inspired (Marty Cagan)", "Product School free resources"],
        "roadmap": [
            "Step 1: Learn outcome-based roadmaps, now/next/later framing, and prioritisation (RICE, MoSCoW).",
            "Step 2: Practise writing PRDs with problem statements, success metrics, and scope boundaries.",
            "Step 3: Build a one-page roadmap for a real product idea and defend the sequencing."
        ]
    },

    # ---------- AI & Machine Learning ----------
    "Machine Learning": {
        "category": "AI & Machine Learning",
        "difficulty": "Advanced",
        "learning_hours": 100,
        "prerequisites": ["Python", "Statistics", "Mathematics"],
        "resources": ["Andrew Ng ML Specialisation", "Hands-On ML with Scikit-Learn", "Kaggle Learn"],
        "roadmap": [
            "Step 1: Learn supervised learning algorithms (Linear Regression, Logistic Regression, Decision Trees, Random Forests).",
            "Step 2: Learn unsupervised learning (K-Means Clustering, PCA) and model evaluation metrics (accuracy, precision, recall, F1, ROC-AUC).",
            "Step 3: Master the practical workflow: train/test split, cross-validation, feature engineering, overfitting control.",
            "Step 4: Build an end-to-end ML classification or prediction pipeline with scikit-learn."
        ]
    },
    "Scikit-learn": {
        "category": "AI & Machine Learning",
        "difficulty": "Intermediate",
        "learning_hours": 40,
        "prerequisites": ["Python", "Pandas"],
        "resources": ["scikit-learn User Guide", "Kaggle Intro to ML"],
        "roadmap": [
            "Step 1: Learn the estimator API: fit, predict, transform, and train_test_split.",
            "Step 2: Master Pipelines, ColumnTransformer, encoders/scalers, and GridSearchCV tuning.",
            "Step 3: Package one trained model with joblib and serve predictions from a small script or API."
        ]
    },
    "Deep Learning": {
        "category": "AI & Machine Learning",
        "difficulty": "Advanced",
        "learning_hours": 110,
        "prerequisites": ["Machine Learning"],
        "resources": ["DeepLearning.AI specialisation", "fast.ai Practical Deep Learning", "Dive into Deep Learning (free)"],
        "roadmap": [
            "Step 1: Understand artificial neural networks, activation functions, loss functions, and backpropagation.",
            "Step 2: Learn Convolutional Neural Networks (CNN) for image tasks and RNN/Transformers for sequence data.",
            "Step 3: Learn regularisation, batch normalisation, learning-rate schedules, and transfer learning.",
            "Step 4: Train and evaluate a deep learning model using PyTorch or TensorFlow on a real dataset."
        ]
    },
    "PyTorch": {
        "category": "AI & Machine Learning",
        "difficulty": "Advanced",
        "learning_hours": 60,
        "prerequisites": ["Deep Learning"],
        "resources": ["PyTorch official tutorials", "PyTorch Lightning docs"],
        "roadmap": [
            "Step 1: Learn tensors, autograd, nn.Module, optimisers, and the manual training loop.",
            "Step 2: Build custom Datasets/DataLoaders and train on GPU with checkpointing.",
            "Step 3: Fine-tune a pretrained model from torchvision/Hugging Face and export it for inference."
        ]
    },
    "Natural Language Processing": {
        "category": "AI & Machine Learning",
        "difficulty": "Advanced",
        "learning_hours": 70,
        "prerequisites": ["Deep Learning"],
        "resources": ["Hugging Face NLP Course (free)", "Speech and Language Processing (Jurafsky, free)"],
        "roadmap": [
            "Step 1: Learn text preprocessing, tokenisation, embeddings (Word2Vec, TF-IDF), and classical text classification.",
            "Step 2: Understand attention and transformer architecture, then fine-tune BERT-style models.",
            "Step 3: Build an NLP application (sentiment analysis, resume parser, or question answering) with evaluation."
        ]
    },
    "Computer Vision": {
        "category": "AI & Machine Learning",
        "difficulty": "Advanced",
        "learning_hours": 70,
        "prerequisites": ["Deep Learning"],
        "resources": ["OpenCV Python tutorials", "Stanford CS231n lectures (free)"],
        "roadmap": [
            "Step 1: Learn image representation, filtering, edge detection, and OpenCV basics.",
            "Step 2: Train CNNs for classification, then learn detection (YOLO) and segmentation (U-Net).",
            "Step 3: Deploy a vision model on live webcam input and measure accuracy plus latency."
        ]
    },
    "Large Language Models (LLM)": {
        "category": "AI & Machine Learning",
        "difficulty": "Advanced",
        "learning_hours": 60,
        "prerequisites": ["Deep Learning"],
        "resources": ["Hugging Face Transformers docs", "Prompt Engineering Guide (free)"],
        "roadmap": [
            "Step 1: Understand tokenisation, context windows, temperature, and how transformers generate text.",
            "Step 2: Learn prompt patterns, retrieval-augmented generation (RAG), embeddings, and vector search.",
            "Step 3: Learn evaluation and guardrails: hallucination checks, grounding, and cost/latency trade-offs.",
            "Step 4: Build a document-question-answering tool over your own notes with a local or open model."
        ]
    },
    "MLOps": {
        "category": "AI & Machine Learning",
        "difficulty": "Advanced",
        "learning_hours": 70,
        "prerequisites": ["Machine Learning", "Docker", "CI/CD"],
        "resources": ["Made With ML (free)", "MLflow docs", "Google MLOps whitepaper"],
        "roadmap": [
            "Step 1: Learn experiment tracking and model registry with MLflow or Weights & Biases.",
            "Step 2: Containerise a model as a REST service and automate training/deployment in CI/CD.",
            "Step 3: Add monitoring for data drift, latency, and accuracy decay, with an automated retrain trigger."
        ]
    },

    # ---------- Data Engineering ----------
    "ETL & Data Pipelines": {
        "category": "Data Engineering",
        "difficulty": "Intermediate",
        "learning_hours": 50,
        "prerequisites": ["Python", "SQL"],
        "resources": ["Fundamentals of Data Engineering", "dbt & Airbyte free docs"],
        "roadmap": [
            "Step 1: Learn extract/transform/load stages, batch vs streaming, and idempotent reloads.",
            "Step 2: Build a Python pipeline with incremental loads, schema validation, and retry logic.",
            "Step 3: Add data quality tests and alerting, then document lineage for every table you produce."
        ]
    },
    "Apache Spark": {
        "category": "Data Engineering",
        "difficulty": "Advanced",
        "learning_hours": 70,
        "prerequisites": ["Python", "SQL"],
        "resources": ["Spark: The Definitive Guide", "Databricks Community Edition (free)"],
        "roadmap": [
            "Step 1: Understand distributed execution, RDDs vs DataFrames, and lazy evaluation.",
            "Step 2: Master PySpark DataFrame API, Spark SQL, joins, and partitioning strategy.",
            "Step 3: Tune a real job: broadcast joins, caching, skew handling, and read the Spark UI."
        ]
    },
    "Apache Airflow": {
        "category": "Data Engineering",
        "difficulty": "Advanced",
        "learning_hours": 40,
        "prerequisites": ["Python", "ETL & Data Pipelines"],
        "resources": ["Airflow docs tutorial", "Astronomer Airflow guides"],
        "roadmap": [
            "Step 1: Learn DAGs, operators, task dependencies, scheduling, and backfills.",
            "Step 2: Master XComs, sensors, hooks, connections, and retries/SLA configuration.",
            "Step 3: Orchestrate a 5-task daily pipeline locally with Docker Compose and alerting on failure."
        ]
    },
    "Apache Kafka": {
        "category": "Data Engineering",
        "difficulty": "Advanced",
        "learning_hours": 45,
        "prerequisites": ["REST APIs"],
        "resources": ["Kafka Docs quickstart", "Confluent free developer courses"],
        "roadmap": [
            "Step 1: Learn topics, partitions, offsets, producers, consumers, and consumer groups.",
            "Step 2: Understand delivery guarantees, replication, retention, and schema registry.",
            "Step 3: Build a producer/consumer pair that streams events into a database in near real time."
        ]
    },

    # ---------- Cloud & DevOps ----------
    "Git": {
        "category": "Cloud & DevOps",
        "difficulty": "Beginner",
        "learning_hours": 20,
        "prerequisites": [],
        "resources": ["Pro Git book (free)", "Learn Git Branching (interactive)"],
        "roadmap": [
            "Step 1: Understand version control concepts and configure Git with GitHub/GitLab.",
            "Step 2: Master basic commands: git init, add, commit, push, pull, and status.",
            "Step 3: Learn branch management, merging, pull requests, and resolving merge conflicts.",
            "Step 4: Learn rebase, stash, cherry-pick, tags, and writing a readable commit history."
        ]
    },
    "Linux": {
        "category": "Cloud & DevOps",
        "difficulty": "Beginner",
        "learning_hours": 40,
        "prerequisites": [],
        "resources": ["Linux Journey", "The Linux Command Line (free book)", "OverTheWire Bandit"],
        "roadmap": [
            "Step 1: Master Linux directory navigation, file permissions (chmod, chown), and basic shell commands.",
            "Step 2: Learn process management (ps, top, kill), package managers (apt), systemd, and SSH.",
            "Step 3: Learn text processing (grep, sed, awk, pipes) and log inspection under /var/log.",
            "Step 4: Configure a small VPS or VM with a firewall, users, and a running service."
        ]
    },
    "Shell Scripting": {
        "category": "Cloud & DevOps",
        "difficulty": "Intermediate",
        "learning_hours": 30,
        "prerequisites": ["Linux"],
        "resources": ["Bash Guide (mywiki.wooledge.org)", "ShellCheck linter"],
        "roadmap": [
            "Step 1: Learn variables, conditionals, loops, functions, and exit codes in Bash.",
            "Step 2: Master argument parsing, redirection, traps, and safe defaults (set -euo pipefail).",
            "Step 3: Automate a real chore (backup, log rotation, deployment) and schedule it with cron."
        ]
    },
    "Docker": {
        "category": "Cloud & DevOps",
        "difficulty": "Intermediate",
        "learning_hours": 35,
        "prerequisites": ["Linux"],
        "resources": ["Docker Docs Get Started", "Play with Docker labs"],
        "roadmap": [
            "Step 1: Understand images vs containers, registries, and the container lifecycle.",
            "Step 2: Write Dockerfiles with layer caching, multi-stage builds, volumes, and networks.",
            "Step 3: Containerise a full-stack app with Docker Compose (app + database) in one command."
        ]
    },
    "Kubernetes": {
        "category": "Cloud & DevOps",
        "difficulty": "Advanced",
        "learning_hours": 70,
        "prerequisites": ["Docker"],
        "resources": ["Kubernetes Docs tutorials", "killercoda free scenarios"],
        "roadmap": [
            "Step 1: Learn pods, deployments, services, ConfigMaps, and Secrets on a local kind/minikube cluster.",
            "Step 2: Master scaling, rolling updates, probes, resource limits, and Ingress routing.",
            "Step 3: Deploy a multi-service app with Helm and practise debugging a failing pod."
        ]
    },
    "CI/CD": {
        "category": "Cloud & DevOps",
        "difficulty": "Intermediate",
        "learning_hours": 35,
        "prerequisites": ["Git", "Docker"],
        "resources": ["GitHub Actions docs", "GitLab CI quickstart"],
        "roadmap": [
            "Step 1: Learn pipeline anatomy: triggers, jobs, steps, caching, and artefacts.",
            "Step 2: Build a pipeline that lints, tests, and builds a Docker image on every pull request.",
            "Step 3: Add automated deployment with environment secrets, approvals, and rollback."
        ]
    },
    "AWS Cloud": {
        "category": "Cloud & DevOps",
        "difficulty": "Intermediate",
        "learning_hours": 70,
        "prerequisites": ["Linux", "Computer Networking"],
        "resources": ["AWS Skill Builder free tier", "AWS Well-Architected Framework"],
        "roadmap": [
            "Step 1: Learn the core services: EC2, S3, IAM, VPC, and RDS, plus the shared responsibility model.",
            "Step 2: Master IAM policies, security groups, load balancers, auto scaling, and CloudWatch.",
            "Step 3: Learn serverless (Lambda, API Gateway) and cost control (budgets, right-sizing).",
            "Step 4: Deploy a real application on free-tier AWS and document the architecture diagram."
        ]
    },
    "Terraform": {
        "category": "Cloud & DevOps",
        "difficulty": "Advanced",
        "learning_hours": 40,
        "prerequisites": ["AWS Cloud"],
        "resources": ["HashiCorp Learn Terraform", "Terraform Registry docs"],
        "roadmap": [
            "Step 1: Learn HCL syntax, providers, resources, variables, and outputs.",
            "Step 2: Master state management, remote backends, modules, and plan/apply workflow.",
            "Step 3: Recreate an existing cloud setup entirely as code, then destroy and rebuild it."
        ]
    },
    "Monitoring & Observability": {
        "category": "Cloud & DevOps",
        "difficulty": "Intermediate",
        "learning_hours": 35,
        "prerequisites": ["Linux"],
        "resources": ["Prometheus & Grafana docs", "Google SRE Book (free)"],
        "roadmap": [
            "Step 1: Learn the three pillars: metrics, logs, and traces, plus SLI/SLO/SLA concepts.",
            "Step 2: Instrument an app with Prometheus metrics and build a Grafana dashboard.",
            "Step 3: Configure alert rules that page on symptoms, and write one incident postmortem."
        ]
    },

    # ---------- Cybersecurity ----------
    "Network Security": {
        "category": "Cybersecurity",
        "difficulty": "Intermediate",
        "learning_hours": 60,
        "prerequisites": ["Computer Networking"],
        "resources": ["Cisco Network Security basics", "Wireshark University samples"],
        "roadmap": [
            "Step 1: Understand TCP/IP networking models, DNS, HTTP/HTTPS, subnetting, and ports.",
            "Step 2: Learn firewall configurations, VPNs, IDS/IPS, and packet inspection using Wireshark.",
            "Step 3: Practise network security auditing and vulnerability scanning with Nmap.",
            "Step 4: Segment a lab network and document the defence-in-depth controls you applied."
        ]
    },
    "Ethical Hacking": {
        "category": "Cybersecurity",
        "difficulty": "Advanced",
        "learning_hours": 80,
        "prerequisites": ["Network Security", "Linux"],
        "resources": ["TryHackMe learning paths", "PortSwigger Web Security Academy (free)", "OWASP Top 10"],
        "roadmap": [
            "Step 1: Understand the phases of ethical hacking (reconnaissance, scanning, gaining access, maintaining access).",
            "Step 2: Learn OWASP Top 10 web vulnerabilities (SQL Injection, XSS, CSRF, Broken Auth).",
            "Step 3: Practise hands-on labs on TryHackMe or PortSwigger Web Security Academy.",
            "Step 4: Write a professional penetration-test report with severity ratings and remediation advice."
        ]
    },
    "Cryptography": {
        "category": "Cybersecurity",
        "difficulty": "Advanced",
        "learning_hours": 50,
        "prerequisites": ["Mathematics"],
        "resources": ["Cryptography I (Dan Boneh, free)", "CryptoHack challenges"],
        "roadmap": [
            "Step 1: Understand symmetric vs asymmetric encryption algorithms (AES, RSA).",
            "Step 2: Learn hashing algorithms (SHA-256), digital signatures, and PKI/SSL/TLS certificates.",
            "Step 3: Implement basic encryption/decryption workflows in Python using vetted crypto libraries."
        ]
    },
    "SIEM": {
        "category": "Cybersecurity",
        "difficulty": "Intermediate",
        "learning_hours": 40,
        "prerequisites": ["Computer Networking"],
        "resources": ["Splunk Free training", "Wazuh documentation", "Elastic Security docs"],
        "roadmap": [
            "Step 1: Understand the purpose of Security Information and Event Management systems and log analysis.",
            "Step 2: Learn log ingestion, normalisation, correlation rules, and threat detection fundamentals.",
            "Step 3: Practise alert triage and incident investigation on an open SIEM platform (Splunk Free or Wazuh)."
        ]
    },
    "Incident Response": {
        "category": "Cybersecurity",
        "difficulty": "Intermediate",
        "learning_hours": 45,
        "prerequisites": ["Network Security"],
        "resources": ["NIST SP 800-61 (free)", "SANS incident handling posters"],
        "roadmap": [
            "Step 1: Learn the IR lifecycle: preparation, detection, containment, eradication, recovery, lessons learned.",
            "Step 2: Practise triage: timeline building, log correlation, IOC collection, and basic forensics.",
            "Step 3: Run a tabletop exercise for a ransomware scenario and produce the incident report."
        ]
    },
    "Cloud Security": {
        "category": "Cybersecurity",
        "difficulty": "Advanced",
        "learning_hours": 50,
        "prerequisites": ["AWS Cloud", "Network Security"],
        "resources": ["AWS Security Best Practices", "CIS Benchmarks", "flaws.cloud free lab"],
        "roadmap": [
            "Step 1: Learn identity-first security: least-privilege IAM, roles, key rotation, and MFA.",
            "Step 2: Master network isolation (VPC, security groups), encryption at rest/in transit, and logging.",
            "Step 3: Audit a cloud account against CIS benchmarks and remediate the top findings."
        ]
    },
    "Security Compliance & Risk": {
        "category": "Cybersecurity",
        "difficulty": "Intermediate",
        "learning_hours": 35,
        "prerequisites": [],
        "resources": ["NIST Cybersecurity Framework", "ISO 27001 overview", "India DPDP Act summary"],
        "roadmap": [
            "Step 1: Learn risk concepts: assets, threats, likelihood/impact scoring, and risk registers.",
            "Step 2: Understand ISO 27001, NIST CSF, and data protection obligations (GDPR, DPDP).",
            "Step 3: Produce a gap assessment and a prioritised control roadmap for a sample organisation."
        ]
    },

    # ---------- Design & UX ----------
    "Figma": {
        "category": "Design & UX",
        "difficulty": "Beginner",
        "learning_hours": 30,
        "prerequisites": [],
        "resources": ["Figma Learn Design", "Figma Community files"],
        "roadmap": [
            "Step 1: Learn frames, auto layout, constraints, components, and variants.",
            "Step 2: Master styles, variables, prototyping links, and developer handoff inspection.",
            "Step 3: Redesign one real app screen and share a clickable prototype for feedback."
        ]
    },
    "Wireframing & Prototyping": {
        "category": "Design & UX",
        "difficulty": "Beginner",
        "learning_hours": 30,
        "prerequisites": ["Figma"],
        "resources": ["Nielsen Norman Group articles", "Laws of UX"],
        "roadmap": [
            "Step 1: Learn information architecture, user flows, and low-fidelity sketching.",
            "Step 2: Move from wireframe to interactive prototype with realistic content and states.",
            "Step 3: Run a 5-user usability test on your prototype and iterate on the findings."
        ]
    },
    "User Research": {
        "category": "Design & UX",
        "difficulty": "Intermediate",
        "learning_hours": 35,
        "prerequisites": [],
        "resources": ["Just Enough Research", "NN/g research methods guide"],
        "roadmap": [
            "Step 1: Learn qualitative vs quantitative methods, interview scripting, and survey design.",
            "Step 2: Practise affinity mapping, personas, journey maps, and problem statements.",
            "Step 3: Run a small study (5-8 participants) and present insights with supporting quotes."
        ]
    },
    "Design Systems": {
        "category": "Design & UX",
        "difficulty": "Advanced",
        "learning_hours": 40,
        "prerequisites": ["Figma"],
        "resources": ["Material Design guidelines", "Atomic Design (Brad Frost, free)"],
        "roadmap": [
            "Step 1: Learn design tokens (colour, type, spacing) and atomic component hierarchy.",
            "Step 2: Build a component library with variants, states, documentation, and usage rules.",
            "Step 3: Keep the design library in sync with the coded components and version the changes."
        ]
    },

    # ---------- Quality & Testing ----------
    "Manual Testing": {
        "category": "Quality & Testing",
        "difficulty": "Beginner",
        "learning_hours": 30,
        "prerequisites": [],
        "resources": ["ISTQB Foundation syllabus (free)", "Ministry of Testing community"],
        "roadmap": [
            "Step 1: Learn the SDLC/STLC, test levels, and defect lifecycle terminology.",
            "Step 2: Write test cases from requirements using equivalence partitioning and boundary analysis.",
            "Step 3: Execute a full test cycle on a live app and log reproducible, well-written bug reports."
        ]
    },
    "Test Automation (Selenium)": {
        "category": "Quality & Testing",
        "difficulty": "Intermediate",
        "learning_hours": 50,
        "prerequisites": ["Manual Testing"],
        "resources": ["Selenium Docs", "Test Automation University (free)"],
        "roadmap": [
            "Step 1: Learn WebDriver setup, locators, waits, and basic browser interactions.",
            "Step 2: Structure a suite with the Page Object Model, TestNG/PyTest, and data-driven tests.",
            "Step 3: Run the suite headless in CI with HTML reports and screenshots on failure."
        ]
    },
    "Cypress": {
        "category": "Quality & Testing",
        "difficulty": "Intermediate",
        "learning_hours": 35,
        "prerequisites": ["JavaScript"],
        "resources": ["Cypress Docs", "Cypress Real World App example"],
        "roadmap": [
            "Step 1: Learn the Cypress runner, selectors, assertions, and automatic waiting.",
            "Step 2: Master fixtures, network stubbing (cy.intercept), custom commands, and test isolation.",
            "Step 3: Cover one real user journey end to end and wire it into a CI pipeline."
        ]
    },
    "API Testing": {
        "category": "Quality & Testing",
        "difficulty": "Intermediate",
        "learning_hours": 30,
        "prerequisites": ["REST APIs"],
        "resources": ["Postman Learning Center", "REST Assured docs"],
        "roadmap": [
            "Step 1: Learn request building, environments, variables, and response assertions in Postman.",
            "Step 2: Cover status codes, schema validation, auth flows, and negative/edge cases.",
            "Step 3: Automate a collection with Newman in CI, or rewrite it in REST Assured/PyTest."
        ]
    },
    "Performance Testing": {
        "category": "Quality & Testing",
        "difficulty": "Advanced",
        "learning_hours": 35,
        "prerequisites": ["Manual Testing"],
        "resources": ["Apache JMeter docs", "k6 open-source docs"],
        "roadmap": [
            "Step 1: Learn load, stress, soak, and spike test types plus key metrics (p95 latency, throughput, error rate).",
            "Step 2: Script a realistic load scenario in JMeter or k6 with think time and ramp-up.",
            "Step 3: Find one bottleneck, fix it, and prove the improvement with a before/after report."
        ]
    },

    # ---------- Hardware & Embedded ----------
    "Microcontrollers (Arduino/ESP32)": {
        "category": "Hardware & Embedded",
        "difficulty": "Beginner",
        "learning_hours": 50,
        "prerequisites": ["Embedded C"],
        "resources": ["Arduino official tutorials", "ESP-IDF programming guide", "Random Nerd Tutorials"],
        "roadmap": [
            "Step 1: Learn GPIO, ADC, PWM, and serial communication with sensors and actuators.",
            "Step 2: Master I2C/SPI peripherals, interrupts, timers, and low-power sleep modes.",
            "Step 3: Build a battery-powered sensor node that publishes readings over Wi-Fi."
        ]
    },
    "IoT Protocols (MQTT)": {
        "category": "Hardware & Embedded",
        "difficulty": "Intermediate",
        "learning_hours": 30,
        "prerequisites": ["Computer Networking"],
        "resources": ["HiveMQ MQTT Essentials", "Eclipse Mosquitto docs"],
        "roadmap": [
            "Step 1: Learn the publish/subscribe model, topics, QoS levels, and retained messages.",
            "Step 2: Understand TLS security, last-will messages, and gateway/edge architecture.",
            "Step 3: Connect devices to a broker and stream telemetry into a live dashboard."
        ]
    },
    "RTOS": {
        "category": "Hardware & Embedded",
        "difficulty": "Advanced",
        "learning_hours": 50,
        "prerequisites": ["Embedded C"],
        "resources": ["FreeRTOS official book (free)", "Zephyr Project docs"],
        "roadmap": [
            "Step 1: Learn tasks, priorities, the scheduler, and stack sizing.",
            "Step 2: Master queues, semaphores, mutexes, and avoiding priority inversion.",
            "Step 3: Port a polling-based firmware project to FreeRTOS with measured timing guarantees."
        ]
    },
    "Digital Electronics": {
        "category": "Hardware & Embedded",
        "difficulty": "Beginner",
        "learning_hours": 40,
        "prerequisites": [],
        "resources": ["All About Circuits (free textbook)", "NPTEL Digital Electronics"],
        "roadmap": [
            "Step 1: Learn number systems, logic gates, Boolean algebra, and K-map simplification.",
            "Step 2: Understand combinational blocks (mux, adder) and sequential blocks (flip-flops, counters).",
            "Step 3: Simulate a small circuit (Logisim/Tinkercad) and then build it on a breadboard."
        ]
    },

    # ---------- Game Development ----------
    "Unity": {
        "category": "Game Development",
        "difficulty": "Intermediate",
        "learning_hours": 70,
        "prerequisites": ["C#"],
        "resources": ["Unity Learn Pathways (free)", "Brackeys archive (YouTube)"],
        "roadmap": [
            "Step 1: Learn the editor, GameObjects, components, prefabs, and the MonoBehaviour lifecycle.",
            "Step 2: Master physics, collisions, animation, UI canvas, input handling, and scene management.",
            "Step 3: Learn profiling, object pooling, and build pipelines for PC/Android.",
            "Step 4: Ship a small complete game with a menu, scoring, save state, and sound."
        ]
    },
    "Game Design": {
        "category": "Game Development",
        "difficulty": "Beginner",
        "learning_hours": 35,
        "prerequisites": [],
        "resources": ["The Art of Game Design (Schell)", "GDC Vault free talks"],
        "roadmap": [
            "Step 1: Learn core loops, player motivation, difficulty curves, and feedback/reward systems.",
            "Step 2: Practise writing a one-page game design document and paper-prototyping mechanics.",
            "Step 3: Playtest a prototype with 5 players and iterate the balance from their data."
        ]
    },
    "3D Modelling (Blender)": {
        "category": "Game Development",
        "difficulty": "Intermediate",
        "learning_hours": 40,
        "prerequisites": [],
        "resources": ["Blender Guru Donut series", "Blender Manual"],
        "roadmap": [
            "Step 1: Learn navigation, mesh modelling, modifiers, and basic materials.",
            "Step 2: Master UV unwrapping, texture baking, and low-poly game-ready topology.",
            "Step 3: Export rigged, optimised assets into Unity and verify scale, pivot, and draw calls."
        ]
    },

    # ---------- Blockchain & Web3 ----------
    "Blockchain Fundamentals": {
        "category": "Blockchain & Web3",
        "difficulty": "Intermediate",
        "learning_hours": 40,
        "prerequisites": [],
        "resources": ["Mastering Bitcoin (free on GitHub)", "ethereum.org learn hub"],
        "roadmap": [
            "Step 1: Learn hashing, Merkle trees, blocks, public-key wallets, and transaction signing.",
            "Step 2: Understand consensus (PoW vs PoS), gas, forks, and layer-2 scaling.",
            "Step 3: Read real on-chain transactions in a block explorer and explain each field."
        ]
    },
    "Smart Contract Security": {
        "category": "Blockchain & Web3",
        "difficulty": "Advanced",
        "learning_hours": 45,
        "prerequisites": ["Solidity"],
        "resources": ["Ethernaut wargame", "Damn Vulnerable DeFi", "Slither static analyser"],
        "roadmap": [
            "Step 1: Learn the classic vulnerability classes: reentrancy, overflow, access control, oracle abuse.",
            "Step 2: Master defensive patterns, invariant testing, fuzzing, and static analysis tooling.",
            "Step 3: Audit a small open-source contract and publish a written findings report."
        ]
    },
    "Web3.js": {
        "category": "Blockchain & Web3",
        "difficulty": "Intermediate",
        "learning_hours": 30,
        "prerequisites": ["JavaScript", "Blockchain Fundamentals"],
        "resources": ["ethers.js docs", "wagmi + viem docs"],
        "roadmap": [
            "Step 1: Learn providers, signers, wallet connection, and reading contract state.",
            "Step 2: Master sending transactions, listening to events, and handling chain/network switches.",
            "Step 3: Build a dApp front end that reads and writes to your own testnet contract."
        ]
    },
}


# ==========================================
# 3. Skill Aliases
# ==========================================
# Students type skills in many forms. The recommender canonicalises every
# entered skill through this map before matching, so "js", "node" and
# "react.js" all score correctly instead of counting as gaps.
SKILL_ALIASES = {
    "py": "Python", "python3": "Python",
    "js": "JavaScript", "ecmascript": "JavaScript", "vanilla js": "JavaScript",
    "ts": "TypeScript",
    "reactjs": "React", "react.js": "React", "react js": "React",
    "node": "Node.js", "nodejs": "Node.js", "node js": "Node.js", "express": "Node.js", "express.js": "Node.js",
    "html5": "HTML", "css3": "CSS", "tailwind": "Tailwind CSS", "tailwindcss": "Tailwind CSS",
    "a11y": "Accessibility (a11y)", "web accessibility": "Accessibility (a11y)",
    "dsa": "Data Structures & Algorithms", "data structures": "Data Structures & Algorithms",
    "algorithms": "Data Structures & Algorithms", "ds & algo": "Data Structures & Algorithms",
    "oops": "Java", "core java": "Java", "j2ee": "Java",
    "cpp": "C++", "c plus plus": "C++", "c sharp": "C#", "csharp": "C#", "dotnet": "C#", ".net": "C#",
    "mysql": "SQL", "postgres": "SQL", "postgresql": "SQL", "sqlite": "SQL", "oracle sql": "SQL",
    "plsql": "SQL", "rdbms": "SQL", "dbms": "SQL",
    "mongo": "MongoDB", "nosql": "MongoDB",
    "dba": "Database Administration",
    "er diagram": "Database Design", "normalization": "Database Design",
    "ms excel": "Excel", "microsoft excel": "Excel", "spreadsheets": "Excel", "google sheets": "Excel",
    "powerbi": "Power BI", "power-bi": "Power BI", "dax": "Power BI",
    "matplotlib": "Data Visualization", "seaborn": "Data Visualization", "charts": "Data Visualization",
    "stats": "Statistics", "probability": "Statistics", "statistical analysis": "Statistics",
    "maths": "Mathematics", "math": "Mathematics", "linear algebra": "Mathematics", "calculus": "Mathematics",
    "ml": "Machine Learning", "machine-learning": "Machine Learning", "supervised learning": "Machine Learning",
    "sklearn": "Scikit-learn", "scikit learn": "Scikit-learn",
    "dl": "Deep Learning", "neural networks": "Deep Learning", "ann": "Deep Learning",
    "cnn": "Deep Learning", "tensorflow": "Deep Learning", "keras": "Deep Learning",
    "torch": "PyTorch",
    "nlp": "Natural Language Processing", "text mining": "Natural Language Processing",
    "cv": "Computer Vision", "opencv": "Computer Vision", "image processing": "Computer Vision",
    "llm": "Large Language Models (LLM)", "llms": "Large Language Models (LLM)",
    "generative ai": "Large Language Models (LLM)", "gen ai": "Large Language Models (LLM)",
    "prompt engineering": "Large Language Models (LLM)", "rag": "Large Language Models (LLM)",
    "etl": "ETL & Data Pipelines", "data pipelines": "ETL & Data Pipelines", "dbt": "ETL & Data Pipelines",
    "spark": "Apache Spark", "pyspark": "Apache Spark", "big data": "Apache Spark", "hadoop": "Apache Spark",
    "airflow": "Apache Airflow", "kafka": "Apache Kafka",
    "data warehouse": "Data Warehousing", "snowflake": "Data Warehousing", "bigquery": "Data Warehousing",
    "github": "Git", "gitlab": "Git", "version control": "Git",
    "unix": "Linux", "ubuntu": "Linux", "linux admin": "Linux",
    "bash": "Shell Scripting", "shell": "Shell Scripting", "powershell": "Shell Scripting",
    "containers": "Docker", "docker compose": "Docker",
    "k8s": "Kubernetes", "kubernets": "Kubernetes",
    "cicd": "CI/CD", "ci-cd": "CI/CD", "jenkins": "CI/CD", "github actions": "CI/CD", "devops pipeline": "CI/CD",
    "aws": "AWS Cloud", "amazon web services": "AWS Cloud", "cloud computing": "AWS Cloud",
    "azure": "AWS Cloud", "gcp": "AWS Cloud", "ec2": "AWS Cloud",
    "iac": "Terraform", "infrastructure as code": "Terraform",
    "prometheus": "Monitoring & Observability", "grafana": "Monitoring & Observability",
    "logging": "Monitoring & Observability", "observability": "Monitoring & Observability",
    "networking": "Computer Networking", "tcp/ip": "Computer Networking", "ccna": "Computer Networking",
    "network": "Computer Networking", "routing and switching": "Computer Networking",
    "netsec": "Network Security", "firewalls": "Network Security", "vapt": "Network Security",
    "pentesting": "Ethical Hacking", "penetration testing": "Ethical Hacking", "kali linux": "Ethical Hacking",
    "burp suite": "Ethical Hacking", "owasp": "Ethical Hacking",
    "crypto": "Cryptography", "encryption": "Cryptography", "pki": "Cryptography",
    "splunk": "SIEM", "wazuh": "SIEM", "log analysis": "SIEM", "soc": "SIEM",
    "ir": "Incident Response", "dfir": "Incident Response", "forensics": "Incident Response",
    "iso 27001": "Security Compliance & Risk", "grc": "Security Compliance & Risk",
    "compliance": "Security Compliance & Risk",
    "ui design": "Figma", "figma design": "Figma", "adobe xd": "Figma", "sketch": "Figma",
    "wireframing": "Wireframing & Prototyping", "prototyping": "Wireframing & Prototyping",
    "ux research": "User Research", "usability testing": "User Research",
    "design system": "Design Systems",
    "manual qa": "Manual Testing", "software testing": "Manual Testing", "test cases": "Manual Testing",
    "istqb": "Manual Testing",
    "selenium": "Test Automation (Selenium)", "automation testing": "Test Automation (Selenium)",
    "playwright": "Cypress", "e2e testing": "Cypress",
    "postman": "API Testing", "rest assured": "API Testing",
    "jmeter": "Performance Testing", "load testing": "Performance Testing", "k6": "Performance Testing",
    "rest": "REST APIs", "rest api": "REST APIs", "api": "REST APIs", "apis": "REST APIs",
    "graphql": "REST APIs", "fastapi": "REST APIs", "flask": "REST APIs", "django": "REST APIs",
    "spring": "Spring Boot", "springboot": "Spring Boot",
    "jwt": "Authentication & Authorization", "oauth": "Authentication & Authorization",
    "auth": "Authentication & Authorization",
    "hld": "System Design", "lld": "System Design", "software architecture": "System Design",
    "os": "Operating Systems", "operating system": "Operating Systems",
    "scrum": "Agile & Scrum", "agile": "Agile & Scrum", "kanban": "Agile & Scrum",
    "atlassian jira": "Jira", "confluence": "Jira",
    "brd": "Business Requirement Analysis", "srs": "Business Requirement Analysis",
    "requirement gathering": "Business Requirement Analysis",
    "bpmn": "Process Modeling (BPMN)", "process mapping": "Process Modeling (BPMN)",
    "roadmap": "Product Roadmapping", "prd": "Product Roadmapping", "product management": "Product Roadmapping",
    "ab testing": "A/B Testing", "a-b testing": "A/B Testing", "experimentation": "A/B Testing",
    "rn": "React Native", "react-native": "React Native", "dart": "Flutter",
    "android": "Kotlin", "android development": "Kotlin", "jetpack compose": "Kotlin",
    "arduino": "Microcontrollers (Arduino/ESP32)", "esp32": "Microcontrollers (Arduino/ESP32)",
    "raspberry pi": "Microcontrollers (Arduino/ESP32)", "iot": "IoT Protocols (MQTT)", "mqtt": "IoT Protocols (MQTT)",
    "freertos": "RTOS", "embedded": "Embedded C", "embedded systems": "Embedded C",
    "microcontroller": "Microcontrollers (Arduino/ESP32)", "vlsi": "Digital Electronics",
    "electronics": "Digital Electronics", "logic gates": "Digital Electronics",
    "unity3d": "Unity", "unity engine": "Unity", "game dev": "Game Design",
    "blender": "3D Modelling (Blender)", "3d modelling": "3D Modelling (Blender)",
    "blockchain": "Blockchain Fundamentals", "web3": "Web3.js", "ethers.js": "Web3.js",
    "smart contracts": "Solidity", "ethereum": "Blockchain Fundamentals",
    "pandas dataframe": "Pandas", "numpy array": "NumPy",
    "data analysis": "Pandas", "eda": "Pandas",
}


# ==========================================
# 4. Career Database
# ==========================================
# Each career carries:
#   required_skills   - full benchmark skill set used for gap analysis
#   core_skills       - must-have subset, weighted CORE_SKILL_WEIGHT in scoring
#   career_path       - 5-stage role progression ladder used to generate the
#                       long-term career path (not just the learning plan)
CAREER_DATABASE = [
    {
        "id": "software_developer",
        "title": "Software Developer",
        "category": "Software Engineering",
        "description": "Designs, develops, tests, and maintains scalable software applications and system tools.",
        "required_skills": [
            "Python", "Java", "Data Structures & Algorithms", "Git", "SQL",
            "REST APIs", "Operating Systems", "System Design"
        ],
        "core_skills": ["Data Structures & Algorithms", "Git", "SQL", "REST APIs"],
        "relevant_interests": [
            "Problem Solving", "Software Architecture", "Coding", "Open Source"
        ],
        "recommended_education": "Bachelor's Degree in Computer Science, Information Technology, or related STEM field",
        "education_keywords": [
            "computer science", "information technology", "b.tech", "b.e", "bca", "mca", "b.sc cs", "software engineering"
        ],
        "demand": "Very High",
        "remote_friendly": True,
        "entry_salary_inr": "4.5 - 9 LPA",
        "growth_outlook": "Largest hiring pool in Indian IT; steady demand across product companies, services and startups.",
        "industries": ["IT Services", "Product Startups", "Fintech", "E-commerce", "Enterprise Software"],
        "tools": ["VS Code / IntelliJ", "Git & GitHub", "Postman", "Docker", "Jira"],
        "soft_skills": ["Debugging patience", "Code review communication", "Estimation", "Teamwork"],
        "certifications": ["Oracle Certified Java Programmer", "AWS Certified Developer - Associate", "Meta Back-End Developer (Coursera)"],
        "portfolio_projects": [
            "Library or inventory management system with authentication and role-based access",
            "REST API backend with 15+ endpoints, tests, and Swagger documentation",
            "CLI productivity tool published as an installable package"
        ],
        "related_careers": ["backend_developer", "web_developer", "devops_engineer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Junior Software Developer / SDE-1", "experience": "0 - 2 years",
             "salary_inr": "4.5 - 9 LPA", "focus": "Ship small well-tested features inside an existing codebase.",
             "skills_to_add": ["Git", "Data Structures & Algorithms", "REST APIs"],
             "milestone": "Close 20+ real tickets and get your code reviewed and merged consistently."},
            {"stage": 2, "level": "Mid", "role": "Software Developer / SDE-2", "experience": "2 - 4 years",
             "salary_inr": "9 - 18 LPA", "focus": "Own a module end to end, including design, tests and on-call fixes.",
             "skills_to_add": ["System Design", "Docker", "CI/CD"],
             "milestone": "Lead one feature from requirement document to production release."},
            {"stage": 3, "level": "Senior", "role": "Senior Software Engineer", "experience": "4 - 7 years",
             "salary_inr": "18 - 35 LPA", "focus": "Design services, mentor juniors, and guard code quality.",
             "skills_to_add": ["Microservices", "Monitoring & Observability", "Kubernetes"],
             "milestone": "Deliver a service used by other teams and document its architecture."},
            {"stage": 4, "level": "Lead", "role": "Tech Lead / Engineering Manager", "experience": "7 - 10 years",
             "salary_inr": "35 - 60 LPA", "focus": "Own delivery for a team: planning, quality, and technical direction.",
             "skills_to_add": ["Stakeholder Management", "Agile & Scrum", "Product Roadmapping"],
             "milestone": "Run a 5-8 person team through two successful quarterly releases."},
            {"stage": 5, "level": "Principal", "role": "Software Architect / Principal Engineer", "experience": "10+ years",
             "salary_inr": "60 LPA - 1 Cr+", "focus": "Set architecture standards across multiple teams and products.",
             "skills_to_add": ["System Design", "Cloud Security", "Terraform"],
             "milestone": "Define a platform standard adopted org-wide."}
        ]
    },
    {
        "id": "frontend_developer",
        "title": "Frontend Developer",
        "category": "Software Engineering",
        "description": "Builds the interfaces users actually touch: accessible, fast, responsive screens in the browser.",
        "required_skills": [
            "HTML", "CSS", "JavaScript", "React", "Git",
            "TypeScript", "Tailwind CSS", "Accessibility (a11y)"
        ],
        "core_skills": ["HTML", "CSS", "JavaScript", "React", "Git"],
        "relevant_interests": [
            "Frontend Development", "UI/UX Design", "Web Applications", "Creative Design"
        ],
        "recommended_education": "Any Bachelor's Degree with strong portfolio; CS/IT background preferred (bootcamp or self-taught accepted)",
        "education_keywords": [
            "computer science", "information technology", "web development", "bca", "diploma", "b.tech", "b.e", "design"
        ],
        "demand": "Very High",
        "remote_friendly": True,
        "entry_salary_inr": "3.5 - 8 LPA",
        "growth_outlook": "Portfolio-driven field where demonstrated work can outweigh degree; strong freelance market.",
        "industries": ["Product Startups", "Digital Agencies", "SaaS", "E-commerce", "Media"],
        "tools": ["VS Code", "Chrome DevTools", "Vite", "Figma", "Lighthouse"],
        "soft_skills": ["Attention to visual detail", "Empathy for users", "Design collaboration"],
        "certifications": ["Meta Front-End Developer (Coursera)", "freeCodeCamp Responsive Web Design", "Google Mobile Web Specialist"],
        "portfolio_projects": [
            "Pixel-accurate rebuild of a real product page, responsive and keyboard accessible",
            "Dashboard SPA consuming a public API with loading, empty and error states",
            "Reusable component library documented in Storybook"
        ],
        "related_careers": ["web_developer", "ui_ux_designer", "mobile_app_developer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Junior Frontend Developer", "experience": "0 - 2 years",
             "salary_inr": "3.5 - 8 LPA", "focus": "Convert designs into working, responsive components.",
             "skills_to_add": ["React", "Tailwind CSS", "Git"],
             "milestone": "Ship 3 production screens that pass a Lighthouse score of 90+."},
            {"stage": 2, "level": "Mid", "role": "Frontend Developer", "experience": "2 - 4 years",
             "salary_inr": "8 - 16 LPA", "focus": "Own state management, performance budgets and shared components.",
             "skills_to_add": ["TypeScript", "Accessibility (a11y)", "Cypress"],
             "milestone": "Cut a real page's load time measurably and write the test suite for it."},
            {"stage": 3, "level": "Senior", "role": "Senior Frontend Engineer", "experience": "4 - 7 years",
             "salary_inr": "16 - 32 LPA", "focus": "Set frontend architecture, tooling and design-system contracts.",
             "skills_to_add": ["Design Systems", "System Design", "Monitoring & Observability"],
             "milestone": "Roll out a design system used by every frontend team."},
            {"stage": 4, "level": "Lead", "role": "Frontend Lead / UI Architect", "experience": "7 - 10 years",
             "salary_inr": "32 - 55 LPA", "focus": "Own the web platform: build pipeline, standards, hiring bar.",
             "skills_to_add": ["Stakeholder Management", "CI/CD", "Agile & Scrum"],
             "milestone": "Migrate a legacy frontend to the modern stack without feature regressions."},
            {"stage": 5, "level": "Principal", "role": "Principal Engineer (Web Platform)", "experience": "10+ years",
             "salary_inr": "55 LPA+", "focus": "Define multi-product web strategy and developer experience.",
             "skills_to_add": ["Microservices", "Product Roadmapping"],
             "milestone": "Own the web architecture decision record for the whole organisation."}
        ]
    },
    {
        "id": "backend_developer",
        "title": "Backend Developer",
        "category": "Software Engineering",
        "description": "Builds the APIs, business logic, databases and integrations that power applications behind the scenes.",
        "required_skills": [
            "Python", "SQL", "REST APIs", "Git", "Database Design",
            "Authentication & Authorization", "Docker", "System Design"
        ],
        "core_skills": ["SQL", "REST APIs", "Git", "Database Design"],
        "relevant_interests": [
            "Problem Solving", "Software Architecture", "Coding", "Scalable Systems"
        ],
        "recommended_education": "Bachelor's Degree in Computer Science, IT, or related engineering discipline",
        "education_keywords": [
            "computer science", "information technology", "b.tech", "b.e", "bca", "mca", "software engineering"
        ],
        "demand": "Very High",
        "remote_friendly": True,
        "entry_salary_inr": "4 - 9 LPA",
        "growth_outlook": "Consistently the hardest role to fill; backend depth transfers well into cloud and data roles.",
        "industries": ["Fintech", "SaaS", "E-commerce", "Healthtech", "IT Services"],
        "tools": ["Postman", "Docker", "PostgreSQL", "Redis", "Swagger/OpenAPI"],
        "soft_skills": ["Clear API documentation", "Incident calm", "Trade-off reasoning"],
        "certifications": ["AWS Certified Developer - Associate", "Oracle Database SQL Certified Associate", "MongoDB Associate Developer"],
        "portfolio_projects": [
            "Multi-tenant REST API with JWT auth, rate limiting and OpenAPI docs",
            "Payment or booking service with transactional integrity and audit logs",
            "Background job system with a queue, retries and a monitoring dashboard"
        ],
        "related_careers": ["software_developer", "devops_engineer", "data_engineer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Junior Backend Developer", "experience": "0 - 2 years",
             "salary_inr": "4 - 9 LPA", "focus": "Write CRUD endpoints, queries and unit tests against a clear spec.",
             "skills_to_add": ["REST APIs", "SQL", "Git"],
             "milestone": "Deliver an authenticated CRUD module with tests and documentation."},
            {"stage": 2, "level": "Mid", "role": "Backend Developer", "experience": "2 - 4 years",
             "salary_inr": "9 - 18 LPA", "focus": "Design schemas, handle caching and keep latency within budget.",
             "skills_to_add": ["Database Design", "Docker", "Monitoring & Observability"],
             "milestone": "Reduce a slow endpoint's p95 latency by 50% and prove it with metrics."},
            {"stage": 3, "level": "Senior", "role": "Senior Backend Engineer", "experience": "4 - 7 years",
             "salary_inr": "18 - 36 LPA", "focus": "Own service boundaries, data consistency and scaling decisions.",
             "skills_to_add": ["System Design", "Microservices", "Apache Kafka"],
             "milestone": "Split a monolith module into an independently deployed service."},
            {"stage": 4, "level": "Lead", "role": "Backend Lead / Platform Lead", "experience": "7 - 10 years",
             "salary_inr": "36 - 60 LPA", "focus": "Set platform standards, review designs and own reliability targets.",
             "skills_to_add": ["Kubernetes", "Stakeholder Management", "Cloud Security"],
             "milestone": "Define and hit an SLO for a business-critical service."},
            {"stage": 5, "level": "Principal", "role": "Principal Engineer / Architect", "experience": "10+ years",
             "salary_inr": "60 LPA - 1 Cr+", "focus": "Shape multi-system architecture and technology selection.",
             "skills_to_add": ["Terraform", "Data Warehousing"],
             "milestone": "Lead a company-wide architecture migration with measured outcomes."}
        ]
    },
    {
        "id": "web_developer",
        "title": "Web Developer",
        "category": "Software Engineering",
        "description": "Builds and maintains responsive client-facing websites and full-stack web applications.",
        "required_skills": [
            "HTML", "CSS", "JavaScript", "React", "Node.js", "Git",
            "MongoDB", "REST APIs"
        ],
        "core_skills": ["HTML", "CSS", "JavaScript", "Git"],
        "relevant_interests": [
            "Web Applications", "UI/UX Design", "Frontend Development", "Creative Design"
        ],
        "recommended_education": "Diploma, Associate, or Bachelor's Degree in Computer Science or Web Development (or self-taught/bootcamp)",
        "education_keywords": [
            "computer science", "information technology", "web development", "bca", "diploma", "b.tech", "b.e"
        ],
        "demand": "Very High",
        "remote_friendly": True,
        "entry_salary_inr": "3 - 7.5 LPA",
        "growth_outlook": "Easiest entry point into tech with a portfolio; also the strongest freelance market.",
        "industries": ["Digital Agencies", "Startups", "E-commerce", "Education", "Freelance"],
        "tools": ["VS Code", "Git & GitHub", "Vite", "Netlify / Vercel", "Chrome DevTools"],
        "soft_skills": ["Client communication", "Scoping small projects", "Self-learning"],
        "certifications": ["Meta Full-Stack Developer (Coursera)", "freeCodeCamp Full Stack Certification", "MongoDB Associate Developer"],
        "portfolio_projects": [
            "Full-stack MERN app with authentication, image upload and deployment",
            "Client-style business website with a CMS and contact form backend",
            "Personal portfolio that scores 95+ on Lighthouse and loads under 1 second"
        ],
        "related_careers": ["frontend_developer", "backend_developer", "ui_ux_designer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Junior Web Developer", "experience": "0 - 2 years",
             "salary_inr": "3 - 7.5 LPA", "focus": "Build and deploy complete small sites and features.",
             "skills_to_add": ["React", "Node.js", "Git"],
             "milestone": "Deploy 3 live full-stack projects with public URLs."},
            {"stage": 2, "level": "Mid", "role": "Full-Stack Web Developer", "experience": "2 - 4 years",
             "salary_inr": "7.5 - 15 LPA", "focus": "Own both ends of a feature: UI, API, database and deploy.",
             "skills_to_add": ["REST APIs", "MongoDB", "Docker"],
             "milestone": "Run a production app with real users and uptime monitoring."},
            {"stage": 3, "level": "Senior", "role": "Senior Full-Stack Developer", "experience": "4 - 7 years",
             "salary_inr": "15 - 30 LPA", "focus": "Make architecture calls and keep a growing codebase healthy.",
             "skills_to_add": ["System Design", "TypeScript", "CI/CD"],
             "milestone": "Refactor a legacy app into a documented, tested architecture."},
            {"stage": 4, "level": "Lead", "role": "Web Tech Lead / Freelance Studio Owner", "experience": "7 - 10 years",
             "salary_inr": "30 - 50 LPA (or project-based)", "focus": "Lead teams or run client delivery end to end.",
             "skills_to_add": ["Stakeholder Management", "Agile & Scrum", "AWS Cloud"],
             "milestone": "Deliver a multi-developer client project on time and on budget."},
            {"stage": 5, "level": "Principal", "role": "Engineering Manager / Technical Director", "experience": "10+ years",
             "salary_inr": "50 LPA+", "focus": "Own product engineering strategy and team growth.",
             "skills_to_add": ["Product Roadmapping", "Microservices"],
             "milestone": "Build and retain a high-performing web engineering team."}
        ]
    },
    {
        "id": "mobile_app_developer",
        "title": "Mobile App Developer",
        "category": "Software Engineering",
        "description": "Builds Android, iOS and cross-platform apps, from UI and offline storage to store release.",
        "required_skills": [
            "Flutter", "Kotlin", "REST APIs", "Git", "SQL",
            "React Native", "Authentication & Authorization"
        ],
        "core_skills": ["REST APIs", "Git", "Flutter"],
        "relevant_interests": [
            "Mobile Development", "Web Applications", "UI/UX Design", "Coding"
        ],
        "recommended_education": "Bachelor's Degree in Computer Science, IT, BCA/MCA, or equivalent portfolio experience",
        "education_keywords": [
            "computer science", "information technology", "b.tech", "b.e", "bca", "mca", "diploma"
        ],
        "demand": "High",
        "remote_friendly": True,
        "entry_salary_inr": "3.5 - 8 LPA",
        "growth_outlook": "India-first mobile products keep demand high, especially for cross-platform Flutter skills.",
        "industries": ["Consumer Apps", "Fintech", "Edtech", "Logistics", "Health & Fitness"],
        "tools": ["Android Studio", "Xcode", "Firebase", "Flutter DevTools", "Play Console"],
        "soft_skills": ["UX judgement on small screens", "Patience with device fragmentation", "Release discipline"],
        "certifications": ["Google Associate Android Developer", "Flutter Certified Application Developer", "Firebase fundamentals"],
        "portfolio_projects": [
            "Offline-first app that syncs to a backend when connectivity returns",
            "App published on the Play Store with crash reporting and analytics",
            "Cross-platform app sharing one codebase across Android and iOS"
        ],
        "related_careers": ["frontend_developer", "web_developer", "ui_ux_designer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Junior Mobile Developer", "experience": "0 - 2 years",
             "salary_inr": "3.5 - 8 LPA", "focus": "Build screens, wire APIs and fix device-specific bugs.",
             "skills_to_add": ["Flutter", "REST APIs", "Git"],
             "milestone": "Publish one app to the Play Store with at least 100 real installs."},
            {"stage": 2, "level": "Mid", "role": "Mobile Application Developer", "experience": "2 - 4 years",
             "salary_inr": "8 - 16 LPA", "focus": "Own app architecture, state management, offline mode and releases.",
             "skills_to_add": ["Kotlin", "Authentication & Authorization", "CI/CD"],
             "milestone": "Set up automated builds and staged rollouts for a production app."},
            {"stage": 3, "level": "Senior", "role": "Senior Mobile Engineer", "experience": "4 - 7 years",
             "salary_inr": "16 - 32 LPA", "focus": "Drive performance, app size, crash-free rate and platform upgrades.",
             "skills_to_add": ["System Design", "Monitoring & Observability", "Performance Testing"],
             "milestone": "Raise crash-free sessions above 99.5% on a live app."},
            {"stage": 4, "level": "Lead", "role": "Mobile Lead", "experience": "7 - 10 years",
             "salary_inr": "32 - 52 LPA", "focus": "Own the mobile roadmap, release process and team standards.",
             "skills_to_add": ["Stakeholder Management", "Product Roadmapping", "Agile & Scrum"],
             "milestone": "Run a quarterly mobile release train with predictable quality."},
            {"stage": 5, "level": "Principal", "role": "Head of Mobile Engineering", "experience": "10+ years",
             "salary_inr": "52 LPA+", "focus": "Set multi-app platform strategy and hiring.",
             "skills_to_add": ["Microservices", "Design Systems"],
             "milestone": "Unify multiple apps onto one shared platform and design system."}
        ]
    },
    {
        "id": "data_analyst",
        "title": "Data Analyst",
        "category": "Data & Analytics",
        "description": "Inspects, cleans, transforms, and models data to discover useful insights and support business decisions.",
        "required_skills": [
            "Python", "SQL", "Excel", "Data Visualization", "Power BI", "Statistics",
            "Pandas", "A/B Testing"
        ],
        "core_skills": ["SQL", "Excel", "Data Visualization", "Statistics"],
        "relevant_interests": [
            "Data Analysis", "Business Intelligence", "Problem Solving", "Statistics"
        ],
        "recommended_education": "Bachelor's Degree in Statistics, Mathematics, Economics, Computer Science, or Business",
        "education_keywords": [
            "statistics", "mathematics", "economics", "computer science", "data science", "business", "bca", "b.tech", "commerce", "b.com", "bba", "mba"
        ],
        "demand": "Very High",
        "remote_friendly": True,
        "entry_salary_inr": "3.5 - 8 LPA",
        "growth_outlook": "Most accessible data role, open to non-CS degrees; natural stepping stone to data science.",
        "industries": ["Consulting", "Banking & Insurance", "E-commerce", "Healthcare", "Marketing"],
        "tools": ["Excel", "Power BI / Tableau", "SQL clients", "Jupyter Notebook", "Google Analytics"],
        "soft_skills": ["Business curiosity", "Storytelling with data", "Stakeholder questioning"],
        "certifications": ["Microsoft Power BI Data Analyst (PL-300)", "Google Data Analytics Certificate", "Tableau Desktop Specialist"],
        "portfolio_projects": [
            "End-to-end analysis of a public dataset with a written recommendation memo",
            "Interactive sales or operations dashboard with drill-downs and filters",
            "SQL case study answering 10 real business questions on a relational dataset"
        ],
        "related_careers": ["data_scientist", "business_analyst", "data_engineer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Junior Data Analyst / Analytics Trainee", "experience": "0 - 2 years",
             "salary_inr": "3.5 - 8 LPA", "focus": "Pull clean data, build recurring reports and answer defined questions.",
             "skills_to_add": ["SQL", "Excel", "Power BI"],
             "milestone": "Own a weekly business report that a real team actually uses."},
            {"stage": 2, "level": "Mid", "role": "Data Analyst", "experience": "2 - 4 years",
             "salary_inr": "8 - 15 LPA", "focus": "Frame the question yourself, run the analysis and present findings.",
             "skills_to_add": ["Python", "Pandas", "A/B Testing"],
             "milestone": "Deliver an analysis that visibly changed a business decision."},
            {"stage": 3, "level": "Senior", "role": "Senior Data Analyst", "experience": "4 - 7 years",
             "salary_inr": "15 - 28 LPA", "focus": "Define metrics, build self-serve models and mentor analysts.",
             "skills_to_add": ["Data Warehousing", "ETL & Data Pipelines", "Machine Learning"],
             "milestone": "Publish the company's single source of truth for one metric domain."},
            {"stage": 4, "level": "Lead", "role": "Analytics Lead / BI Manager", "experience": "7 - 10 years",
             "salary_inr": "28 - 48 LPA", "focus": "Own the analytics roadmap, data quality and team output.",
             "skills_to_add": ["Stakeholder Management", "Product Roadmapping", "Tableau"],
             "milestone": "Stand up a BI function that leadership relies on monthly."},
            {"stage": 5, "level": "Principal", "role": "Head of Analytics / Data Science Manager", "experience": "10+ years",
             "salary_inr": "48 LPA+", "focus": "Set the organisation's data strategy and governance.",
             "skills_to_add": ["Security Compliance & Risk", "MLOps"],
             "milestone": "Make data-informed decision making the default across departments."}
        ]
    },
    {
        "id": "data_scientist",
        "title": "Data Scientist",
        "category": "Data & Analytics",
        "description": "Combines statistics, programming and domain knowledge to model data and predict business outcomes.",
        "required_skills": [
            "Python", "SQL", "Statistics", "Mathematics", "Pandas",
            "Machine Learning", "Scikit-learn", "Data Visualization", "A/B Testing"
        ],
        "core_skills": ["Python", "SQL", "Statistics", "Machine Learning"],
        "relevant_interests": [
            "Data Science", "Machine Learning", "Statistics", "Research", "Data Analysis"
        ],
        "recommended_education": "Bachelor's or Master's in Statistics, Mathematics, Computer Science, Data Science, or Economics",
        "education_keywords": [
            "statistics", "mathematics", "computer science", "data science", "economics", "m.tech", "m.sc", "mca", "b.tech", "phd"
        ],
        "demand": "High",
        "remote_friendly": True,
        "entry_salary_inr": "6 - 14 LPA",
        "growth_outlook": "Strong pay band, but expects proven statistical rigour and real modelling projects, not just courses.",
        "industries": ["Fintech", "E-commerce", "Consulting", "Pharma & Healthcare", "Telecom"],
        "tools": ["Jupyter", "scikit-learn", "SQL", "MLflow", "Matplotlib/Seaborn"],
        "soft_skills": ["Scientific scepticism", "Explaining models to non-experts", "Experiment design"],
        "certifications": ["IBM Data Science Professional Certificate", "Microsoft Azure Data Scientist Associate (DP-100)", "Google Advanced Data Analytics"],
        "portfolio_projects": [
            "Churn or default prediction model with business-impact framing and error analysis",
            "Forecasting model evaluated against a naive baseline with honest metrics",
            "Kaggle competition writeup explaining feature engineering decisions"
        ],
        "related_careers": ["ai_ml_engineer", "data_analyst", "data_engineer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Junior Data Scientist / Data Science Intern", "experience": "0 - 2 years",
             "salary_inr": "6 - 14 LPA", "focus": "Clean data, build baseline models and validate assumptions.",
             "skills_to_add": ["Pandas", "Scikit-learn", "Statistics"],
             "milestone": "Ship one model that beats the existing heuristic in production."},
            {"stage": 2, "level": "Mid", "role": "Data Scientist", "experience": "2 - 4 years",
             "salary_inr": "14 - 26 LPA", "focus": "Own problem framing, feature engineering and experiment design.",
             "skills_to_add": ["A/B Testing", "Machine Learning", "ETL & Data Pipelines"],
             "milestone": "Run a controlled experiment whose result changed a product decision."},
            {"stage": 3, "level": "Senior", "role": "Senior Data Scientist", "experience": "4 - 7 years",
             "salary_inr": "26 - 45 LPA", "focus": "Lead modelling strategy, review rigour and mentor the team.",
             "skills_to_add": ["Deep Learning", "MLOps", "Apache Spark"],
             "milestone": "Take a model from notebook to monitored production service."},
            {"stage": 4, "level": "Lead", "role": "Lead Data Scientist / DS Manager", "experience": "7 - 10 years",
             "salary_inr": "45 - 70 LPA", "focus": "Align the DS roadmap with business value and run the team.",
             "skills_to_add": ["Stakeholder Management", "Product Roadmapping"],
             "milestone": "Build a DS portfolio of projects with measured revenue or cost impact."},
            {"stage": 5, "level": "Principal", "role": "Principal Data Scientist / Head of Data Science", "experience": "10+ years",
             "salary_inr": "70 LPA - 1.2 Cr", "focus": "Set the company's modelling and experimentation standards.",
             "skills_to_add": ["Large Language Models (LLM)", "Security Compliance & Risk"],
             "milestone": "Define org-wide standards for model validation and responsible use."}
        ]
    },
    {
        "id": "data_engineer",
        "title": "Data Engineer",
        "category": "Data & Analytics",
        "description": "Builds the pipelines and warehouses that move raw data into reliable, query-ready tables.",
        "required_skills": [
            "Python", "SQL", "ETL & Data Pipelines", "Data Warehousing", "Apache Spark",
            "Apache Airflow", "Linux", "Docker", "Apache Kafka"
        ],
        "core_skills": ["Python", "SQL", "ETL & Data Pipelines", "Data Warehousing"],
        "relevant_interests": [
            "Data Engineering", "Scalable Systems", "Data Analysis", "Problem Solving", "Cloud Computing"
        ],
        "recommended_education": "Bachelor's Degree in Computer Science, IT, or Engineering with strong SQL and programming",
        "education_keywords": [
            "computer science", "information technology", "b.tech", "b.e", "mca", "data science", "data engineering"
        ],
        "demand": "Very High",
        "remote_friendly": True,
        "entry_salary_inr": "5 - 11 LPA",
        "growth_outlook": "Demand outstrips supply; often better paid than analytics for the same experience.",
        "industries": ["Fintech", "E-commerce", "Telecom", "Media Streaming", "Consulting"],
        "tools": ["Airflow", "Spark / Databricks", "dbt", "Snowflake / BigQuery", "Kafka"],
        "soft_skills": ["Ownership of data quality", "Documentation habit", "Debugging under pressure"],
        "certifications": ["Google Professional Data Engineer", "Databricks Certified Data Engineer Associate", "AWS Certified Data Engineer - Associate"],
        "portfolio_projects": [
            "Daily batch pipeline with Airflow, incremental loads and data quality tests",
            "Streaming pipeline that ingests events into a warehouse in near real time",
            "Dimensional warehouse layer with dbt models and documented lineage"
        ],
        "related_careers": ["data_analyst", "backend_developer", "devops_engineer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Junior Data Engineer", "experience": "0 - 2 years",
             "salary_inr": "5 - 11 LPA", "focus": "Write SQL transformations and maintain existing pipelines.",
             "skills_to_add": ["SQL", "Python", "ETL & Data Pipelines"],
             "milestone": "Own a scheduled pipeline and handle its failures yourself."},
            {"stage": 2, "level": "Mid", "role": "Data Engineer", "experience": "2 - 4 years",
             "salary_inr": "11 - 22 LPA", "focus": "Design pipelines, model warehouse layers and enforce data contracts.",
             "skills_to_add": ["Apache Airflow", "Data Warehousing", "Docker"],
             "milestone": "Deliver a warehouse layer that analysts query without your help."},
            {"stage": 3, "level": "Senior", "role": "Senior Data Engineer", "experience": "4 - 7 years",
             "salary_inr": "22 - 40 LPA", "focus": "Own platform scalability, cost and streaming architecture.",
             "skills_to_add": ["Apache Spark", "Apache Kafka", "Terraform"],
             "milestone": "Cut pipeline cost or runtime by half while improving reliability."},
            {"stage": 4, "level": "Lead", "role": "Lead Data Engineer / Data Platform Lead", "experience": "7 - 10 years",
             "salary_inr": "40 - 65 LPA", "focus": "Run the data platform team, governance and tooling choices.",
             "skills_to_add": ["Stakeholder Management", "Security Compliance & Risk", "Kubernetes"],
             "milestone": "Establish platform SLAs that downstream teams depend on."},
            {"stage": 5, "level": "Principal", "role": "Data Architect / Head of Data Platform", "experience": "10+ years",
             "salary_inr": "65 LPA - 1 Cr", "focus": "Define the enterprise data architecture and strategy.",
             "skills_to_add": ["System Design", "Cloud Security"],
             "milestone": "Deliver an organisation-wide data architecture migration."}
        ]
    },
    {
        "id": "ai_ml_engineer",
        "title": "AI/ML Engineer",
        "category": "AI & Machine Learning",
        "description": "Researches, builds, and ships self-running artificial intelligence systems and machine learning models.",
        "required_skills": [
            "Python", "Machine Learning", "Deep Learning", "Mathematics", "Statistics", "SQL",
            "PyTorch", "MLOps", "Large Language Models (LLM)"
        ],
        "core_skills": ["Python", "Machine Learning", "Deep Learning", "Mathematics"],
        "relevant_interests": [
            "Artificial Intelligence", "Machine Learning", "Data Science", "Research", "Problem Solving"
        ],
        "recommended_education": "Bachelor's or Master's Degree in Computer Science, Data Science, AI, or Mathematics",
        "education_keywords": [
            "computer science", "data science", "artificial intelligence", "mathematics", "m.tech", "b.tech", "mca", "m.sc", "phd", "statistics"
        ],
        "demand": "Very High",
        "remote_friendly": True,
        "entry_salary_inr": "6 - 15 LPA",
        "growth_outlook": "Fastest-growing pay band in Indian tech, with heavy current demand for LLM and MLOps skills.",
        "industries": ["AI Product Startups", "Big Tech R&D", "Fintech", "Healthtech", "Manufacturing (vision)"],
        "tools": ["PyTorch / TensorFlow", "Hugging Face", "MLflow", "Docker", "Weights & Biases"],
        "soft_skills": ["Reading research papers", "Honest error analysis", "Communicating uncertainty"],
        "certifications": ["DeepLearning.AI Deep Learning Specialisation", "TensorFlow Developer Certificate", "AWS Certified Machine Learning - Specialty"],
        "portfolio_projects": [
            "Deep learning model trained and deployed behind a REST endpoint with monitoring",
            "RAG question-answering system over a document set with evaluation metrics",
            "Computer vision or NLP application with a documented accuracy/latency trade-off"
        ],
        "related_careers": ["data_scientist", "data_engineer", "backend_developer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "ML Engineer Trainee / Junior AI Engineer", "experience": "0 - 2 years",
             "salary_inr": "6 - 15 LPA", "focus": "Train, evaluate and document models on prepared datasets.",
             "skills_to_add": ["Machine Learning", "Python", "Scikit-learn"],
             "milestone": "Reproduce a published result and explain every metric you report."},
            {"stage": 2, "level": "Mid", "role": "Machine Learning Engineer", "experience": "2 - 4 years",
             "salary_inr": "15 - 30 LPA", "focus": "Own the full pipeline: data, training, serving and monitoring.",
             "skills_to_add": ["Deep Learning", "PyTorch", "Docker"],
             "milestone": "Serve a model in production with versioning and rollback."},
            {"stage": 3, "level": "Senior", "role": "Senior ML Engineer", "experience": "4 - 7 years",
             "salary_inr": "30 - 50 LPA", "focus": "Design ML systems, control cost/latency and lead evaluation rigour.",
             "skills_to_add": ["MLOps", "Large Language Models (LLM)", "Kubernetes"],
             "milestone": "Build an ML platform component reused by several models."},
            {"stage": 4, "level": "Lead", "role": "ML Lead / Applied Research Lead", "experience": "7 - 10 years",
             "salary_inr": "50 - 80 LPA", "focus": "Set the AI roadmap and balance research with delivery.",
             "skills_to_add": ["System Design", "Stakeholder Management"],
             "milestone": "Deliver an AI capability that became a core product feature."},
            {"stage": 5, "level": "Principal", "role": "Principal AI Scientist / Head of AI", "experience": "10+ years",
             "salary_inr": "80 LPA - 1.5 Cr", "focus": "Own AI strategy, responsible-use policy and external credibility.",
             "skills_to_add": ["Security Compliance & Risk", "Product Roadmapping"],
             "milestone": "Publish or patent work and set the organisation's AI standards."}
        ]
    },
    {
        "id": "cybersecurity_analyst",
        "title": "Cybersecurity Analyst",
        "category": "Cybersecurity",
        "description": "Monitors, detects, investigates, and prevents cyber threats and unauthorized access to digital systems.",
        "required_skills": [
            "Network Security", "Linux", "Ethical Hacking", "Cryptography", "Python", "SIEM",
            "Computer Networking", "Incident Response"
        ],
        "core_skills": ["Network Security", "Linux", "Computer Networking", "SIEM"],
        "relevant_interests": [
            "Cybersecurity", "Information Security", "Ethical Hacking", "Network Defense", "Problem Solving"
        ],
        "recommended_education": "Bachelor's Degree in Cybersecurity, Computer Science, Information Technology, or related discipline",
        "education_keywords": [
            "cybersecurity", "information security", "computer science", "information technology", "b.tech", "bca", "mca", "forensics"
        ],
        "demand": "Very High",
        "remote_friendly": True,
        "entry_salary_inr": "4 - 9 LPA",
        "growth_outlook": "Regulation and breach pressure keep demand high; certifications carry real weight here.",
        "industries": ["Banking & Finance", "IT Services", "Government & Defence", "Healthcare", "Consulting"],
        "tools": ["Wireshark", "Nmap", "Burp Suite", "Splunk / Wazuh", "Kali Linux"],
        "soft_skills": ["Methodical investigation", "Report writing", "Calm escalation"],
        "certifications": ["CompTIA Security+", "CEH (Certified Ethical Hacker)", "Microsoft SC-200 Security Operations Analyst"],
        "portfolio_projects": [
            "Home SOC lab with Wazuh/Splunk ingesting logs and custom detection rules",
            "Full penetration test of a deliberately vulnerable app with a written report",
            "Network hardening writeup: before/after scan results with remediation evidence"
        ],
        "related_careers": ["network_engineer", "cloud_engineer", "devops_engineer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "SOC Analyst (L1) / Security Trainee", "experience": "0 - 2 years",
             "salary_inr": "4 - 9 LPA", "focus": "Triage alerts, escalate true positives and document findings.",
             "skills_to_add": ["SIEM", "Computer Networking", "Linux"],
             "milestone": "Handle a full shift of alert triage with clean, reproducible notes."},
            {"stage": 2, "level": "Mid", "role": "Cybersecurity Analyst (L2)", "experience": "2 - 4 years",
             "salary_inr": "9 - 18 LPA", "focus": "Investigate incidents, tune detections and run vulnerability scans.",
             "skills_to_add": ["Incident Response", "Network Security", "Python"],
             "milestone": "Lead one incident investigation from detection to postmortem."},
            {"stage": 3, "level": "Senior", "role": "Senior Security Analyst / Penetration Tester", "experience": "4 - 7 years",
             "salary_inr": "18 - 34 LPA", "focus": "Threat hunting, red-team exercises and control design.",
             "skills_to_add": ["Ethical Hacking", "Cloud Security", "Cryptography"],
             "milestone": "Deliver a pentest or threat-hunt that closed a critical risk."},
            {"stage": 4, "level": "Lead", "role": "Security Lead / SOC Manager", "experience": "7 - 10 years",
             "salary_inr": "34 - 55 LPA", "focus": "Run the security programme, team and audit readiness.",
             "skills_to_add": ["Security Compliance & Risk", "Stakeholder Management"],
             "milestone": "Pass an external security audit with no critical findings."},
            {"stage": 5, "level": "Principal", "role": "CISO / Head of Information Security", "experience": "10+ years",
             "salary_inr": "55 LPA - 1.2 Cr", "focus": "Own enterprise risk posture, policy and board reporting.",
             "skills_to_add": ["Security Compliance & Risk", "Product Roadmapping"],
             "milestone": "Define and fund a multi-year security strategy."}
        ]
    },
    {
        "id": "devops_engineer",
        "title": "DevOps Engineer",
        "category": "Cloud & Infrastructure",
        "description": "Automates build, release and infrastructure so teams can ship safely many times a day.",
        "required_skills": [
            "Linux", "Git", "Docker", "CI/CD", "Shell Scripting",
            "Kubernetes", "AWS Cloud", "Terraform", "Monitoring & Observability"
        ],
        "core_skills": ["Linux", "Git", "Docker", "CI/CD"],
        "relevant_interests": [
            "DevOps & Automation", "Cloud Computing", "Scalable Systems", "Problem Solving", "System Administration"
        ],
        "recommended_education": "Bachelor's Degree in Computer Science, IT, or Engineering; strong Linux experience can substitute",
        "education_keywords": [
            "computer science", "information technology", "b.tech", "b.e", "bca", "mca", "diploma", "electronics"
        ],
        "demand": "Very High",
        "remote_friendly": True,
        "entry_salary_inr": "4.5 - 10 LPA",
        "growth_outlook": "Few freshers have real pipeline experience, so a strong home lab stands out immediately.",
        "industries": ["SaaS", "Fintech", "IT Services", "E-commerce", "Cloud Consulting"],
        "tools": ["Docker", "Kubernetes", "GitHub Actions / Jenkins", "Terraform", "Prometheus & Grafana"],
        "soft_skills": ["Automation mindset", "Blameless postmortems", "Cross-team empathy"],
        "certifications": ["AWS Certified Solutions Architect - Associate", "Certified Kubernetes Administrator (CKA)", "HashiCorp Terraform Associate"],
        "portfolio_projects": [
            "Full CI/CD pipeline that tests, builds and deploys an app on every merge",
            "Entire cloud environment provisioned from Terraform code, destroyed and rebuilt",
            "Kubernetes deployment with autoscaling, health probes and Grafana dashboards"
        ],
        "related_careers": ["cloud_engineer", "backend_developer", "cybersecurity_analyst"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Junior DevOps / Build Engineer", "experience": "0 - 2 years",
             "salary_inr": "4.5 - 10 LPA", "focus": "Maintain pipelines, fix builds and script repetitive work away.",
             "skills_to_add": ["Linux", "Docker", "CI/CD"],
             "milestone": "Automate one manual release process end to end."},
            {"stage": 2, "level": "Mid", "role": "DevOps Engineer", "experience": "2 - 4 years",
             "salary_inr": "10 - 20 LPA", "focus": "Own infrastructure as code, environments and deployment safety.",
             "skills_to_add": ["Terraform", "AWS Cloud", "Monitoring & Observability"],
             "milestone": "Move an environment fully into version-controlled infrastructure code."},
            {"stage": 3, "level": "Senior", "role": "Senior DevOps / SRE", "experience": "4 - 7 years",
             "salary_inr": "20 - 38 LPA", "focus": "Reliability engineering: SLOs, capacity, incident response, cost.",
             "skills_to_add": ["Kubernetes", "Cloud Security", "Shell Scripting"],
             "milestone": "Define SLOs and cut incident recovery time measurably."},
            {"stage": 4, "level": "Lead", "role": "DevOps Lead / Platform Engineering Manager", "experience": "7 - 10 years",
             "salary_inr": "38 - 60 LPA", "focus": "Build the internal platform other engineers build on.",
             "skills_to_add": ["Stakeholder Management", "Microservices"],
             "milestone": "Ship a self-service platform that cuts time-to-deploy for every team."},
            {"stage": 5, "level": "Principal", "role": "Head of Infrastructure / Cloud Architect", "experience": "10+ years",
             "salary_inr": "60 LPA - 1 Cr", "focus": "Own multi-cloud strategy, resilience and spend.",
             "skills_to_add": ["System Design", "Security Compliance & Risk"],
             "milestone": "Lead a cloud strategy that improves both uptime and cost."}
        ]
    },
    {
        "id": "cloud_engineer",
        "title": "Cloud Engineer",
        "category": "Cloud & Infrastructure",
        "description": "Designs, deploys and secures applications and networks on cloud platforms like AWS, Azure or GCP.",
        "required_skills": [
            "AWS Cloud", "Linux", "Computer Networking", "Docker", "Terraform",
            "Shell Scripting", "Monitoring & Observability", "Cloud Security"
        ],
        "core_skills": ["AWS Cloud", "Linux", "Computer Networking"],
        "relevant_interests": [
            "Cloud Computing", "DevOps & Automation", "System Administration", "Scalable Systems", "Networking"
        ],
        "recommended_education": "Bachelor's Degree in Computer Science, IT, or Electronics; cloud certifications are highly valued",
        "education_keywords": [
            "computer science", "information technology", "b.tech", "b.e", "bca", "mca", "electronics", "diploma"
        ],
        "demand": "Very High",
        "remote_friendly": True,
        "entry_salary_inr": "4.5 - 10 LPA",
        "growth_outlook": "Every migration project needs cloud skills; certification plus a real deployed project opens doors fast.",
        "industries": ["Cloud Consulting", "Banking", "IT Services", "SaaS", "Government Digital"],
        "tools": ["AWS Console & CLI", "Terraform", "CloudWatch", "Docker", "VPN / networking tools"],
        "soft_skills": ["Cost awareness", "Documentation", "Risk thinking"],
        "certifications": ["AWS Certified Solutions Architect - Associate", "Microsoft Azure Administrator (AZ-104)", "Google Associate Cloud Engineer"],
        "portfolio_projects": [
            "Three-tier application deployed on free-tier cloud with an architecture diagram",
            "Cost-optimised setup documenting before/after monthly spend",
            "Automated backup and disaster-recovery plan you actually tested"
        ],
        "related_careers": ["devops_engineer", "network_engineer", "cybersecurity_analyst"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Cloud Support / Junior Cloud Engineer", "experience": "0 - 2 years",
             "salary_inr": "4.5 - 10 LPA", "focus": "Provision resources, handle tickets and follow runbooks.",
             "skills_to_add": ["AWS Cloud", "Linux", "Computer Networking"],
             "milestone": "Pass an associate-level cloud certification and deploy a live app."},
            {"stage": 2, "level": "Mid", "role": "Cloud Engineer", "experience": "2 - 4 years",
             "salary_inr": "10 - 20 LPA", "focus": "Design VPCs, automate provisioning and manage IAM properly.",
             "skills_to_add": ["Terraform", "Docker", "Monitoring & Observability"],
             "milestone": "Migrate one on-prem workload to the cloud with no data loss."},
            {"stage": 3, "level": "Senior", "role": "Senior Cloud Engineer", "experience": "4 - 7 years",
             "salary_inr": "20 - 38 LPA", "focus": "Own architecture reviews, security posture and resilience.",
             "skills_to_add": ["Cloud Security", "Kubernetes", "System Design"],
             "milestone": "Design a multi-AZ architecture that survives a zone failure."},
            {"stage": 4, "level": "Lead", "role": "Cloud Architect", "experience": "7 - 10 years",
             "salary_inr": "38 - 65 LPA", "focus": "Lead migrations, standards and vendor decisions.",
             "skills_to_add": ["Stakeholder Management", "Security Compliance & Risk"],
             "milestone": "Deliver an enterprise migration programme on schedule."},
            {"stage": 5, "level": "Principal", "role": "Principal Cloud Architect / Head of Cloud", "experience": "10+ years",
             "salary_inr": "65 LPA - 1 Cr", "focus": "Set cloud strategy, governance and FinOps for the organisation.",
             "skills_to_add": ["Terraform", "Microservices"],
             "milestone": "Own a cloud landing-zone standard adopted company-wide."}
        ]
    },
    {
        "id": "ui_ux_designer",
        "title": "UI/UX Designer",
        "category": "Design & Product",
        "description": "Researches user needs and designs interfaces that are clear, usable and pleasant to work with.",
        "required_skills": [
            "Figma", "Wireframing & Prototyping", "User Research", "Design Systems",
            "HTML", "CSS", "Accessibility (a11y)"
        ],
        "core_skills": ["Figma", "Wireframing & Prototyping", "User Research"],
        "relevant_interests": [
            "UI/UX Design", "Creative Design", "Design Thinking", "User Psychology", "Frontend Development"
        ],
        "recommended_education": "Degree or diploma in Design, HCI, Fine Arts, or any field with a strong design portfolio",
        "education_keywords": [
            "design", "fine arts", "architecture", "human computer interaction", "b.des", "m.des", "computer science", "diploma", "mass communication"
        ],
        "demand": "High",
        "remote_friendly": True,
        "entry_salary_inr": "3 - 7 LPA",
        "growth_outlook": "Hiring is portfolio-first; case studies that show reasoning matter more than the degree.",
        "industries": ["Product Startups", "Design Studios", "E-commerce", "Fintech", "Edtech"],
        "tools": ["Figma", "FigJam", "Maze / usability tools", "Notion", "Webflow"],
        "soft_skills": ["Listening to users", "Defending decisions with evidence", "Receiving critique"],
        "certifications": ["Google UX Design Certificate", "NN/g UX Certification", "Interaction Design Foundation courses"],
        "portfolio_projects": [
            "End-to-end case study: research, wireframes, prototype, usability test, final UI",
            "Redesign of a frustrating real app with before/after usability evidence",
            "Component library with documented tokens, states and accessibility notes"
        ],
        "related_careers": ["frontend_developer", "product_manager", "web_developer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Junior UI/UX Designer", "experience": "0 - 2 years",
             "salary_inr": "3 - 7 LPA", "focus": "Produce screens and prototypes from existing patterns and briefs.",
             "skills_to_add": ["Figma", "Wireframing & Prototyping", "Accessibility (a11y)"],
             "milestone": "Publish 3 complete case studies in a portfolio site."},
            {"stage": 2, "level": "Mid", "role": "UI/UX Designer", "experience": "2 - 4 years",
             "salary_inr": "7 - 14 LPA", "focus": "Own a product area: research, flows, UI and developer handoff.",
             "skills_to_add": ["User Research", "Design Systems", "HTML"],
             "milestone": "Ship a redesign that improved a measured usability or conversion metric."},
            {"stage": 3, "level": "Senior", "role": "Senior Product Designer", "experience": "4 - 7 years",
             "salary_inr": "14 - 28 LPA", "focus": "Shape product strategy with design and mentor juniors.",
             "skills_to_add": ["Product Roadmapping", "A/B Testing", "Stakeholder Management"],
             "milestone": "Lead design for a full product launch."},
            {"stage": 4, "level": "Lead", "role": "Design Lead / Design Manager", "experience": "7 - 10 years",
             "salary_inr": "28 - 48 LPA", "focus": "Run the design team, the system and the research practice.",
             "skills_to_add": ["Design Systems", "Agile & Scrum"],
             "milestone": "Build a design system and process the whole org follows."},
            {"stage": 5, "level": "Principal", "role": "Head of Design / Design Director", "experience": "10+ years",
             "salary_inr": "48 LPA+", "focus": "Own design vision, hiring and brand consistency across products.",
             "skills_to_add": ["Product Roadmapping", "Stakeholder Management"],
             "milestone": "Establish design as a decision-making partner at leadership level."}
        ]
    },
    {
        "id": "qa_automation_engineer",
        "title": "QA / Test Automation Engineer",
        "category": "Quality Engineering",
        "description": "Protects release quality through test design, automation suites and performance verification.",
        "required_skills": [
            "Manual Testing", "Test Automation (Selenium)", "API Testing", "Git", "SQL",
            "Cypress", "CI/CD", "Performance Testing"
        ],
        "core_skills": ["Manual Testing", "Test Automation (Selenium)", "API Testing"],
        "relevant_interests": [
            "Quality Assurance", "Problem Solving", "DevOps & Automation", "Coding"
        ],
        "recommended_education": "Bachelor's Degree in Computer Science, IT, BCA/MCA, or any engineering degree",
        "education_keywords": [
            "computer science", "information technology", "b.tech", "b.e", "bca", "mca", "diploma", "engineering"
        ],
        "demand": "High",
        "remote_friendly": True,
        "entry_salary_inr": "3 - 7 LPA",
        "growth_outlook": "Reliable entry route into IT; automation skills roughly double the pay band versus manual-only QA.",
        "industries": ["IT Services", "Product Companies", "Banking", "Healthcare IT", "Gaming"],
        "tools": ["Selenium", "Postman", "Cypress", "JMeter", "Jira & TestRail"],
        "soft_skills": ["Scepticism", "Precise bug writing", "Negotiating quality vs deadline"],
        "certifications": ["ISTQB Certified Tester Foundation Level", "Test Automation University certificates", "Certified Selenium Professional"],
        "portfolio_projects": [
            "Automation framework with Page Object Model running in CI with reports",
            "API test collection covering happy paths, negatives and schema validation",
            "Load test report finding and proving a real bottleneck fix"
        ],
        "related_careers": ["software_developer", "devops_engineer", "backend_developer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "QA Trainee / Manual Test Engineer", "experience": "0 - 2 years",
             "salary_inr": "3 - 7 LPA", "focus": "Write and execute test cases, log clean reproducible defects.",
             "skills_to_add": ["Manual Testing", "SQL", "API Testing"],
             "milestone": "Own the test cycle for one module across a full release."},
            {"stage": 2, "level": "Mid", "role": "Automation Test Engineer", "experience": "2 - 4 years",
             "salary_inr": "7 - 14 LPA", "focus": "Build and maintain automation suites that teams trust.",
             "skills_to_add": ["Test Automation (Selenium)", "Cypress", "CI/CD"],
             "milestone": "Automate a regression suite and cut manual cycle time in half."},
            {"stage": 3, "level": "Senior", "role": "Senior SDET", "experience": "4 - 7 years",
             "salary_inr": "14 - 28 LPA", "focus": "Design test architecture, performance strategy and quality gates.",
             "skills_to_add": ["Performance Testing", "Docker", "System Design"],
             "milestone": "Define quality gates that block bad releases automatically."},
            {"stage": 4, "level": "Lead", "role": "QA Lead / Quality Manager", "experience": "7 - 10 years",
             "salary_inr": "28 - 45 LPA", "focus": "Own the quality strategy, metrics and team across products.",
             "skills_to_add": ["Stakeholder Management", "Agile & Scrum"],
             "milestone": "Reduce production defect escape rate with a measurable programme."},
            {"stage": 5, "level": "Principal", "role": "Head of Quality Engineering", "experience": "10+ years",
             "salary_inr": "45 LPA+", "focus": "Set org-wide quality engineering and release standards.",
             "skills_to_add": ["Monitoring & Observability", "Security Compliance & Risk"],
             "milestone": "Embed quality ownership inside every delivery team."}
        ]
    },
    {
        "id": "business_analyst",
        "title": "Business Analyst (IT)",
        "category": "Business & Product",
        "description": "Bridges business and engineering: gathers requirements, models processes and validates delivered value.",
        "required_skills": [
            "Business Requirement Analysis", "SQL", "Excel", "Process Modeling (BPMN)",
            "Stakeholder Management", "Data Visualization", "Agile & Scrum", "Jira"
        ],
        "core_skills": ["Business Requirement Analysis", "Excel", "Stakeholder Management"],
        "relevant_interests": [
            "Business Strategy", "Business Intelligence", "Problem Solving", "Data Analysis", "Product Management"
        ],
        "recommended_education": "Bachelor's or Master's in Business, Commerce, Economics, Engineering, or MBA",
        "education_keywords": [
            "business", "commerce", "b.com", "bba", "mba", "economics", "management", "computer science", "information technology", "b.tech"
        ],
        "demand": "High",
        "remote_friendly": True,
        "entry_salary_inr": "4 - 9 LPA",
        "growth_outlook": "Strong path for commerce and management students into tech without heavy coding.",
        "industries": ["Consulting", "Banking & Insurance", "ERP Implementation", "Healthcare", "Retail"],
        "tools": ["Excel", "Jira & Confluence", "Power BI", "Lucidchart / bpmn.io", "SQL clients"],
        "soft_skills": ["Active listening", "Written clarity", "Negotiation", "Facilitation"],
        "certifications": ["IIBA ECBA / CCBA", "PMI Professional in Business Analysis (PBA)", "Microsoft Power BI (PL-300)"],
        "portfolio_projects": [
            "Complete BRD/SRS for a real process with as-is and to-be BPMN diagrams",
            "Requirement traceability matrix linking user stories to test cases",
            "Dashboard plus written recommendation for a business problem you scoped yourself"
        ],
        "related_careers": ["data_analyst", "product_manager", "qa_automation_engineer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Junior Business Analyst", "experience": "0 - 2 years",
             "salary_inr": "4 - 9 LPA", "focus": "Document requirements, maintain backlogs and support UAT.",
             "skills_to_add": ["Business Requirement Analysis", "Jira", "Excel"],
             "milestone": "Write the requirement document for one shipped feature."},
            {"stage": 2, "level": "Mid", "role": "Business Analyst", "experience": "2 - 4 years",
             "salary_inr": "9 - 17 LPA", "focus": "Own a domain: elicitation, process design, data checks and sign-off.",
             "skills_to_add": ["SQL", "Process Modeling (BPMN)", "Data Visualization"],
             "milestone": "Lead requirements for a project from kickoff to go-live."},
            {"stage": 3, "level": "Senior", "role": "Senior Business Analyst", "experience": "4 - 7 years",
             "salary_inr": "17 - 30 LPA", "focus": "Shape solution options, business cases and change management.",
             "skills_to_add": ["Stakeholder Management", "Product Roadmapping", "A/B Testing"],
             "milestone": "Present a business case that secured budget approval."},
            {"stage": 4, "level": "Lead", "role": "Lead BA / Product Owner", "experience": "7 - 10 years",
             "salary_inr": "30 - 48 LPA", "focus": "Own product backlog priority and cross-team delivery outcomes.",
             "skills_to_add": ["Agile & Scrum", "Product Roadmapping"],
             "milestone": "Own a product line's backlog and its delivered business metrics."},
            {"stage": 5, "level": "Principal", "role": "Business Architect / Consulting Manager", "experience": "10+ years",
             "salary_inr": "48 LPA+", "focus": "Design business capability models and lead transformation programmes.",
             "skills_to_add": ["Security Compliance & Risk", "Stakeholder Management"],
             "milestone": "Lead an enterprise transformation with measured ROI."}
        ]
    },
    {
        "id": "database_administrator",
        "title": "Database Administrator (DBA)",
        "category": "Data & Analytics",
        "description": "Keeps databases fast, available, backed up and secure, and tunes the queries that run on them.",
        "required_skills": [
            "SQL", "Database Design", "Database Administration", "Linux", "Shell Scripting",
            "Monitoring & Observability", "Security Compliance & Risk"
        ],
        "core_skills": ["SQL", "Database Administration", "Linux"],
        "relevant_interests": [
            "Data Analysis", "System Administration", "Scalable Systems", "Problem Solving", "Information Security"
        ],
        "recommended_education": "Bachelor's Degree in Computer Science, IT, or BCA/MCA with strong database coursework",
        "education_keywords": [
            "computer science", "information technology", "b.tech", "b.e", "bca", "mca", "diploma"
        ],
        "demand": "Moderate",
        "remote_friendly": True,
        "entry_salary_inr": "4 - 8.5 LPA",
        "growth_outlook": "Smaller but stable niche with low competition; cloud database skills keep it relevant.",
        "industries": ["Banking", "Government", "ERP & Enterprise IT", "Telecom", "Healthcare"],
        "tools": ["PostgreSQL / Oracle / MySQL", "pgAdmin", "Backup tooling", "Grafana", "Bash"],
        "soft_skills": ["Caution with production", "Change discipline", "Clear runbooks"],
        "certifications": ["Oracle Database Administration Certified Professional", "Microsoft Azure Database Administrator (DP-300)", "AWS Database Specialty"],
        "portfolio_projects": [
            "Backup and point-in-time recovery drill documented with timings",
            "Replication setup with failover tested and measured",
            "Query tuning case study showing EXPLAIN plans before and after"
        ],
        "related_careers": ["data_engineer", "backend_developer", "cloud_engineer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Junior DBA / Database Support", "experience": "0 - 2 years",
             "salary_inr": "4 - 8.5 LPA", "focus": "Run backups, monitor jobs and handle access requests.",
             "skills_to_add": ["SQL", "Linux", "Database Administration"],
             "milestone": "Complete a restore drill without any data loss."},
            {"stage": 2, "level": "Mid", "role": "Database Administrator", "experience": "2 - 4 years",
             "salary_inr": "8.5 - 16 LPA", "focus": "Own tuning, indexing, replication and upgrade planning.",
             "skills_to_add": ["Database Design", "Shell Scripting", "Monitoring & Observability"],
             "milestone": "Tune the top 10 slow queries and document the gains."},
            {"stage": 3, "level": "Senior", "role": "Senior DBA", "experience": "4 - 7 years",
             "salary_inr": "16 - 30 LPA", "focus": "High availability, capacity planning and database security.",
             "skills_to_add": ["Security Compliance & Risk", "AWS Cloud", "Data Warehousing"],
             "milestone": "Deliver a zero-downtime major version upgrade."},
            {"stage": 4, "level": "Lead", "role": "Database Lead / Data Platform Engineer", "experience": "7 - 10 years",
             "salary_inr": "30 - 48 LPA", "focus": "Standardise database platforms and automate operations.",
             "skills_to_add": ["Terraform", "Stakeholder Management"],
             "milestone": "Automate provisioning and patching across all database fleets."},
            {"stage": 5, "level": "Principal", "role": "Data Architect", "experience": "10+ years",
             "salary_inr": "48 LPA+", "focus": "Own enterprise data storage architecture and governance.",
             "skills_to_add": ["System Design", "Data Warehousing"],
             "milestone": "Define the data storage standard for the organisation."}
        ]
    },
    {
        "id": "game_developer",
        "title": "Game Developer",
        "category": "Software Engineering",
        "description": "Builds interactive games: gameplay systems, physics, UI, performance tuning and release builds.",
        "required_skills": [
            "C#", "Unity", "Game Design", "Mathematics", "Git",
            "C++", "3D Modelling (Blender)", "Performance Testing"
        ],
        "core_skills": ["C#", "Unity", "Game Design"],
        "relevant_interests": [
            "Game Development", "Creative Design", "Coding", "Storytelling", "Problem Solving"
        ],
        "recommended_education": "Bachelor's in Computer Science, Game Design, Animation, or a strong shipped-game portfolio",
        "education_keywords": [
            "computer science", "game", "animation", "multimedia", "information technology", "b.tech", "bca", "design", "diploma"
        ],
        "demand": "Moderate",
        "remote_friendly": True,
        "entry_salary_inr": "3 - 7 LPA",
        "growth_outlook": "Competitive but growing with India's mobile gaming market; shipped games beat degrees.",
        "industries": ["Mobile Gaming", "Game Studios", "AR/VR", "Edtech Gamification", "Simulation & Training"],
        "tools": ["Unity", "Blender", "Git LFS", "Unity Profiler", "Play Console / Steam"],
        "soft_skills": ["Playtest humility", "Scope discipline", "Collaboration with artists"],
        "certifications": ["Unity Certified Associate: Game Developer", "Unreal Engine Fellowship courses"],
        "portfolio_projects": [
            "A complete small game shipped on itch.io or the Play Store",
            "Game jam entry built in 48 hours with a written postmortem",
            "Gameplay systems demo (inventory, AI, procedural level) with clean code"
        ],
        "related_careers": ["mobile_app_developer", "software_developer", "ui_ux_designer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Junior Game Programmer", "experience": "0 - 2 years",
             "salary_inr": "3 - 7 LPA", "focus": "Implement mechanics, UI and bug fixes inside an existing project.",
             "skills_to_add": ["Unity", "C#", "Game Design"],
             "milestone": "Ship one complete playable game with a menu, save state and sound."},
            {"stage": 2, "level": "Mid", "role": "Game Developer", "experience": "2 - 4 years",
             "salary_inr": "7 - 14 LPA", "focus": "Own gameplay systems, performance and build pipeline.",
             "skills_to_add": ["Performance Testing", "Mathematics", "Git"],
             "milestone": "Hold a stable 60 FPS on mid-range devices for a real title."},
            {"stage": 3, "level": "Senior", "role": "Senior Gameplay Engineer", "experience": "4 - 7 years",
             "salary_inr": "14 - 28 LPA", "focus": "Architect game systems, tools and multiplayer networking.",
             "skills_to_add": ["C++", "System Design", "Monitoring & Observability"],
             "milestone": "Build an engine tool or framework the whole studio uses."},
            {"stage": 4, "level": "Lead", "role": "Lead Game Developer / Technical Director", "experience": "7 - 10 years",
             "salary_inr": "28 - 45 LPA", "focus": "Own technical direction and production quality for a title.",
             "skills_to_add": ["Stakeholder Management", "Agile & Scrum"],
             "milestone": "Lead a title from prototype to launch."},
            {"stage": 5, "level": "Principal", "role": "Studio Technical Director / Indie Studio Founder", "experience": "10+ years",
             "salary_inr": "45 LPA+ (or revenue-based)", "focus": "Set studio technology strategy or run your own studio.",
             "skills_to_add": ["Product Roadmapping", "Design Systems"],
             "milestone": "Ship a commercially successful title with a team you built."}
        ]
    },
    {
        "id": "blockchain_developer",
        "title": "Blockchain Developer",
        "category": "Emerging Technology",
        "description": "Writes and audits smart contracts and builds decentralised applications on blockchain networks.",
        "required_skills": [
            "Blockchain Fundamentals", "Solidity", "JavaScript", "Web3.js", "Git",
            "Smart Contract Security", "Cryptography", "REST APIs"
        ],
        "core_skills": ["Blockchain Fundamentals", "Solidity", "JavaScript"],
        "relevant_interests": [
            "Blockchain & Web3", "Coding", "Information Security", "Problem Solving", "Research"
        ],
        "recommended_education": "Bachelor's Degree in Computer Science or IT; verifiable on-chain work matters most",
        "education_keywords": [
            "computer science", "information technology", "b.tech", "b.e", "mca", "bca", "mathematics"
        ],
        "demand": "Moderate",
        "remote_friendly": True,
        "entry_salary_inr": "5 - 12 LPA",
        "growth_outlook": "Volatile but high-paying niche; audit and security skills hold value through market cycles.",
        "industries": ["Web3 Startups", "Fintech", "Supply Chain", "Gaming (NFT)", "Security Audit Firms"],
        "tools": ["Hardhat / Foundry", "MetaMask", "Remix IDE", "ethers.js", "Etherscan"],
        "soft_skills": ["Security paranoia", "Public code scrutiny", "Clear technical writing"],
        "certifications": ["Certified Blockchain Developer (Blockchain Council)", "ConsenSys Blockchain Developer course"],
        "portfolio_projects": [
            "Token or escrow contract deployed to a testnet with a full test suite",
            "Full dApp with wallet connection, contract reads/writes and error handling",
            "Public audit writeup of an open-source contract with findings and fixes"
        ],
        "related_careers": ["backend_developer", "cybersecurity_analyst", "frontend_developer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Junior Blockchain Developer", "experience": "0 - 2 years",
             "salary_inr": "5 - 12 LPA", "focus": "Write and test simple contracts and dApp integrations.",
             "skills_to_add": ["Solidity", "Blockchain Fundamentals", "Web3.js"],
             "milestone": "Deploy a tested contract to a public testnet with a working front end."},
            {"stage": 2, "level": "Mid", "role": "Blockchain Developer", "experience": "2 - 4 years",
             "salary_inr": "12 - 24 LPA", "focus": "Own contract architecture, gas optimisation and upgrade patterns.",
             "skills_to_add": ["Smart Contract Security", "Cryptography", "REST APIs"],
             "milestone": "Ship a mainnet contract that has handled real value safely."},
            {"stage": 3, "level": "Senior", "role": "Senior Smart Contract Engineer", "experience": "4 - 7 years",
             "salary_inr": "24 - 45 LPA", "focus": "Lead protocol design, invariant testing and audit response.",
             "skills_to_add": ["System Design", "Smart Contract Security"],
             "milestone": "Pass an external audit on a protocol you designed."},
            {"stage": 4, "level": "Lead", "role": "Protocol Lead / Security Auditor", "experience": "7 - 10 years",
             "salary_inr": "45 - 70 LPA", "focus": "Own protocol economics, security review and team direction.",
             "skills_to_add": ["Stakeholder Management", "Security Compliance & Risk"],
             "milestone": "Publish audits or protocol research the ecosystem cites."},
            {"stage": 5, "level": "Principal", "role": "Protocol Architect / Web3 CTO", "experience": "10+ years",
             "salary_inr": "70 LPA+", "focus": "Set protocol and security strategy for the organisation.",
             "skills_to_add": ["Microservices", "Product Roadmapping"],
             "milestone": "Launch and sustain a protocol with real adoption."}
        ]
    },
    {
        "id": "embedded_iot_engineer",
        "title": "Embedded / IoT Engineer",
        "category": "Hardware & Embedded",
        "description": "Programs microcontrollers and connected devices, from sensor drivers to cloud telemetry.",
        "required_skills": [
            "Embedded C", "Microcontrollers (Arduino/ESP32)", "Digital Electronics", "Computer Networking",
            "IoT Protocols (MQTT)", "RTOS", "Python", "Git"
        ],
        "core_skills": ["Embedded C", "Microcontrollers (Arduino/ESP32)", "Digital Electronics"],
        "relevant_interests": [
            "Internet of Things", "Hardware & Electronics", "Robotics", "Problem Solving", "Coding"
        ],
        "recommended_education": "Bachelor's Degree in Electronics, ECE, EEE, Instrumentation, or Computer Engineering",
        "education_keywords": [
            "electronics", "ece", "eee", "instrumentation", "electrical", "b.tech", "b.e", "diploma", "computer science", "mechatronics"
        ],
        "demand": "High",
        "remote_friendly": False,
        "entry_salary_inr": "3.5 - 8 LPA",
        "growth_outlook": "Strong fit for ECE/EEE students; India's electronics manufacturing push is expanding roles.",
        "industries": ["Consumer Electronics", "Automotive", "Industrial Automation", "Medical Devices", "Smart Energy"],
        "tools": ["STM32CubeIDE / PlatformIO", "Oscilloscope & logic analyser", "Arduino IDE", "MQTT brokers", "Git"],
        "soft_skills": ["Hardware debugging patience", "Datasheet reading", "Safety discipline"],
        "certifications": ["ARM Accredited Engineer", "AWS IoT Core training", "Certified LabVIEW Associate Developer"],
        "portfolio_projects": [
            "Battery-powered sensor node publishing telemetry to a cloud dashboard",
            "Bare-metal driver suite (UART, I2C, SPI) written without vendor libraries",
            "Home automation system with an app, local control and failure handling"
        ],
        "related_careers": ["network_engineer", "software_developer", "devops_engineer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Graduate Embedded Engineer", "experience": "0 - 2 years",
             "salary_inr": "3.5 - 8 LPA", "focus": "Write peripheral code, test on hardware and fix timing bugs.",
             "skills_to_add": ["Embedded C", "Microcontrollers (Arduino/ESP32)", "Digital Electronics"],
             "milestone": "Deliver a working prototype board plus firmware you wrote yourself."},
            {"stage": 2, "level": "Mid", "role": "Embedded / IoT Engineer", "experience": "2 - 4 years",
             "salary_inr": "8 - 16 LPA", "focus": "Own firmware modules, connectivity, OTA updates and power budget.",
             "skills_to_add": ["IoT Protocols (MQTT)", "RTOS", "Computer Networking"],
             "milestone": "Ship a connected device with reliable over-the-air updates."},
            {"stage": 3, "level": "Senior", "role": "Senior Firmware Engineer", "experience": "4 - 7 years",
             "salary_inr": "16 - 30 LPA", "focus": "Architect firmware, certification readiness and production testing.",
             "skills_to_add": ["System Design", "Security Compliance & Risk", "Python"],
             "milestone": "Take a device through certification and mass production."},
            {"stage": 4, "level": "Lead", "role": "Embedded Lead / Hardware-Software Lead", "experience": "7 - 10 years",
             "salary_inr": "30 - 48 LPA", "focus": "Own platform architecture across product lines.",
             "skills_to_add": ["Stakeholder Management", "Monitoring & Observability"],
             "milestone": "Define a reusable firmware platform for multiple products."},
            {"stage": 5, "level": "Principal", "role": "Embedded Systems Architect", "experience": "10+ years",
             "salary_inr": "48 LPA+", "focus": "Set hardware-software strategy, safety and supplier standards.",
             "skills_to_add": ["Cloud Security", "System Design"],
             "milestone": "Own the architecture of a flagship product family."}
        ]
    },
    {
        "id": "network_engineer",
        "title": "Network Engineer",
        "category": "Cloud & Infrastructure",
        "description": "Designs, configures and troubleshoots the routers, switches, firewalls and links that keep traffic flowing.",
        "required_skills": [
            "Computer Networking", "Linux", "Network Security", "Shell Scripting",
            "Monitoring & Observability", "AWS Cloud", "Python"
        ],
        "core_skills": ["Computer Networking", "Network Security", "Linux"],
        "relevant_interests": [
            "Networking", "System Administration", "Network Defense", "Cloud Computing", "Problem Solving"
        ],
        "recommended_education": "Bachelor's Degree in Computer Science, IT, ECE, or diploma with CCNA-level certification",
        "education_keywords": [
            "computer science", "information technology", "electronics", "ece", "b.tech", "b.e", "diploma", "bca", "networking"
        ],
        "demand": "High",
        "remote_friendly": False,
        "entry_salary_inr": "3 - 7 LPA",
        "growth_outlook": "Certification-driven field where CCNA plus a home lab reliably lands the first role.",
        "industries": ["Telecom & ISP", "Data Centres", "Banking", "Government", "Managed Service Providers"],
        "tools": ["Cisco IOS / Packet Tracer", "Wireshark", "GNS3 / EVE-NG", "Zabbix / Nagios", "Ansible"],
        "soft_skills": ["Systematic troubleshooting", "On-call reliability", "Precise change records"],
        "certifications": ["Cisco CCNA", "Cisco CCNP Enterprise", "AWS Advanced Networking Specialty"],
        "portfolio_projects": [
            "Multi-site network built in GNS3/Packet Tracer with routing, VLANs and failover",
            "Firewall and VPN setup documented with test evidence",
            "Monitoring stack alerting on link failures in a lab network"
        ],
        "related_careers": ["cloud_engineer", "cybersecurity_analyst", "devops_engineer"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Network Support Engineer (L1)", "experience": "0 - 2 years",
             "salary_inr": "3 - 7 LPA", "focus": "Handle connectivity tickets, basic configs and escalation.",
             "skills_to_add": ["Computer Networking", "Linux", "Monitoring & Observability"],
             "milestone": "Clear CCNA and troubleshoot a routing issue end to end."},
            {"stage": 2, "level": "Mid", "role": "Network Engineer", "experience": "2 - 4 years",
             "salary_inr": "7 - 14 LPA", "focus": "Configure routing, VLANs, firewalls and document changes.",
             "skills_to_add": ["Network Security", "Shell Scripting", "Python"],
             "milestone": "Deliver a site rollout with zero unplanned downtime."},
            {"stage": 3, "level": "Senior", "role": "Senior Network Engineer", "experience": "4 - 7 years",
             "salary_inr": "14 - 28 LPA", "focus": "Design topologies, capacity and network automation.",
             "skills_to_add": ["AWS Cloud", "Cloud Security", "Terraform"],
             "milestone": "Automate network configuration with version-controlled templates."},
            {"stage": 4, "level": "Lead", "role": "Network Lead / Infrastructure Manager", "experience": "7 - 10 years",
             "salary_inr": "28 - 45 LPA", "focus": "Own network strategy, vendors and reliability targets.",
             "skills_to_add": ["Stakeholder Management", "Security Compliance & Risk"],
             "milestone": "Hit 99.99% network availability across sites for a year."},
            {"stage": 5, "level": "Principal", "role": "Network Architect", "experience": "10+ years",
             "salary_inr": "45 LPA+", "focus": "Design enterprise and hybrid-cloud network architecture.",
             "skills_to_add": ["System Design", "Kubernetes"],
             "milestone": "Deliver an enterprise network redesign with measured gains."}
        ]
    },
    {
        "id": "product_manager",
        "title": "Technical Product Manager",
        "category": "Business & Product",
        "description": "Decides what to build and why: discovers problems, prioritises the roadmap and ships outcomes with the team.",
        "required_skills": [
            "Product Roadmapping", "Business Requirement Analysis", "Agile & Scrum", "SQL",
            "A/B Testing", "Stakeholder Management", "Data Visualization", "Jira"
        ],
        "core_skills": ["Product Roadmapping", "Agile & Scrum", "Stakeholder Management"],
        "relevant_interests": [
            "Product Management", "Business Strategy", "Problem Solving", "UI/UX Design", "Data Analysis"
        ],
        "recommended_education": "Bachelor's in Engineering, Business, or Design; MBA or strong technical background helps",
        "education_keywords": [
            "business", "mba", "bba", "b.com", "management", "computer science", "information technology", "b.tech", "b.e", "design", "economics"
        ],
        "demand": "High",
        "remote_friendly": True,
        "entry_salary_inr": "6 - 14 LPA",
        "growth_outlook": "Rarely a fresher role; most enter via engineering, analytics, BA or support after 1-2 years.",
        "industries": ["SaaS", "Fintech", "E-commerce", "Edtech", "Consumer Apps"],
        "tools": ["Jira & Confluence", "Figma", "Mixpanel / GA4", "SQL clients", "Notion"],
        "soft_skills": ["Saying no with reasons", "Written clarity", "Influence without authority", "User empathy"],
        "certifications": ["Certified Scrum Product Owner (CSPO)", "Google Project Management Certificate", "Pragmatic Institute PMC"],
        "portfolio_projects": [
            "PRD for a real product gap with success metrics and scope boundaries",
            "Teardown of a popular app with prioritised, justified improvements",
            "Experiment plan plus analysis for one growth hypothesis"
        ],
        "related_careers": ["business_analyst", "ui_ux_designer", "data_analyst"],
        "career_path": [
            {"stage": 1, "level": "Entry", "role": "Associate Product Manager (APM)", "experience": "0 - 2 years",
             "salary_inr": "6 - 14 LPA", "focus": "Own small features: specs, grooming, launch checklists.",
             "skills_to_add": ["Agile & Scrum", "Jira", "Business Requirement Analysis"],
             "milestone": "Ship one feature you specified end to end."},
            {"stage": 2, "level": "Mid", "role": "Product Manager", "experience": "2 - 5 years",
             "salary_inr": "14 - 30 LPA", "focus": "Own a product area, its roadmap and its metrics.",
             "skills_to_add": ["Product Roadmapping", "SQL", "A/B Testing"],
             "milestone": "Move a north-star metric with a shipped bet you championed."},
            {"stage": 3, "level": "Senior", "role": "Senior Product Manager", "experience": "5 - 8 years",
             "salary_inr": "30 - 50 LPA", "focus": "Own strategy for a product line and mentor PMs.",
             "skills_to_add": ["Stakeholder Management", "Data Visualization", "System Design"],
             "milestone": "Launch a new product line from discovery to GA."},
            {"stage": 4, "level": "Lead", "role": "Group Product Manager / Director of Product", "experience": "8 - 12 years",
             "salary_inr": "50 - 80 LPA", "focus": "Run a PM team and align portfolio bets with company goals.",
             "skills_to_add": ["Product Roadmapping", "Security Compliance & Risk"],
             "milestone": "Own a portfolio's P&L or primary growth target."},
            {"stage": 5, "level": "Principal", "role": "VP Product / Chief Product Officer", "experience": "12+ years",
             "salary_inr": "80 LPA - 1.5 Cr", "focus": "Set product vision, pricing and market strategy.",
             "skills_to_add": ["Stakeholder Management"],
             "milestone": "Define a company-level product strategy that scales revenue."}
        ]
    }
]


# ==========================================
# 5. Interest & Education Catalogs
# ==========================================
# Grouped interests shown in the profile form. Every interest used by a career
# in CAREER_DATABASE appears here, so the form can always produce a match.
INTEREST_LIBRARY = {
    "Engineering & Building": [
        "Coding", "Problem Solving", "Software Architecture", "Scalable Systems", "Open Source"
    ],
    "Web, Mobile & Design": [
        "Web Applications", "Frontend Development", "Mobile Development",
        "UI/UX Design", "Creative Design", "Design Thinking", "User Psychology"
    ],
    "Data & AI": [
        "Data Analysis", "Data Science", "Data Engineering", "Business Intelligence",
        "Statistics", "Machine Learning", "Artificial Intelligence", "Research"
    ],
    "Infrastructure & Security": [
        "Cloud Computing", "DevOps & Automation", "System Administration", "Networking",
        "Cybersecurity", "Information Security", "Ethical Hacking", "Network Defense"
    ],
    "Business & Product": [
        "Business Strategy", "Product Management", "Quality Assurance"
    ],
    "Emerging & Specialised": [
        "Game Development", "Storytelling", "Blockchain & Web3",
        "Internet of Things", "Hardware & Electronics", "Robotics"
    ]
}

# Education choices offered in the profile form (kept server-side so the
# frontend and the scoring keywords never drift apart).
EDUCATION_OPTIONS = [
    "Bachelor of Technology (B.Tech / B.E.) in Computer Science / IT",
    "Bachelor of Technology (B.Tech / B.E.) in Electronics / ECE / EEE",
    "Bachelor of Technology (B.Tech / B.E.) in Mechanical / Civil / Other Branch",
    "Bachelor of Science (B.Sc) in Computer Science / IT",
    "Bachelor of Science (B.Sc) in Statistics / Mathematics / Physics",
    "Bachelor of Computer Applications (BCA)",
    "Bachelor of Commerce (B.Com) / BBA / Management",
    "Bachelor of Design (B.Des) / Fine Arts / Animation",
    "Bachelor's Degree in Statistics / Mathematics / Economics",
    "Master of Computer Applications (MCA)",
    "Master of Technology (M.Tech) / M.S. in CS / AI / Data Science",
    "Master of Business Administration (MBA)",
    "Master of Science (M.Sc) in Statistics / Mathematics / Data Science",
    "Diploma in Computer Engineering / Information Technology",
    "Diploma in Electronics / Electrical Engineering",
    "High School / Pre-University",
    "Other Graduate / Postgraduate Degree"
]


# Students rarely type a career goal exactly as the catalog spells it. These
# aliases map common job-title phrasings onto a career id so the stated goal is
# recognised ("ML Engineer" -> ai_ml_engineer, "MERN developer" -> web_developer).
CAREER_GOAL_ALIASES = {
    "software engineer": "software_developer", "sde": "software_developer",
    "programmer": "software_developer", "application developer": "software_developer",
    "ui developer": "frontend_developer", "react developer": "frontend_developer",
    "frontend engineer": "frontend_developer", "front end developer": "frontend_developer",
    "backend engineer": "backend_developer", "back end developer": "backend_developer",
    "api developer": "backend_developer", "server side developer": "backend_developer",
    "full stack developer": "web_developer", "fullstack developer": "web_developer",
    "mern developer": "web_developer", "website developer": "web_developer",
    "android developer": "mobile_app_developer", "ios developer": "mobile_app_developer",
    "flutter developer": "mobile_app_developer", "app developer": "mobile_app_developer",
    "mobile developer": "mobile_app_developer",
    "data analytics": "data_analyst", "bi analyst": "data_analyst",
    "business intelligence analyst": "data_analyst", "reporting analyst": "data_analyst",
    "research scientist": "data_scientist", "ml scientist": "data_scientist",
    "machine learning engineer": "ai_ml_engineer", "ml engineer": "ai_ml_engineer",
    "ai engineer": "ai_ml_engineer", "deep learning engineer": "ai_ml_engineer",
    "ai developer": "ai_ml_engineer", "nlp engineer": "ai_ml_engineer",
    "analytics engineer": "data_engineer", "big data engineer": "data_engineer",
    "etl developer": "data_engineer", "data pipeline engineer": "data_engineer",
    "soc analyst": "cybersecurity_analyst", "security analyst": "cybersecurity_analyst",
    "penetration tester": "cybersecurity_analyst", "ethical hacker": "cybersecurity_analyst",
    "information security analyst": "cybersecurity_analyst", "cyber security": "cybersecurity_analyst",
    "sre": "devops_engineer", "site reliability engineer": "devops_engineer",
    "platform engineer": "devops_engineer", "build engineer": "devops_engineer",
    "aws engineer": "cloud_engineer", "solutions architect": "cloud_engineer",
    "cloud architect": "cloud_engineer", "azure engineer": "cloud_engineer",
    "ux designer": "ui_ux_designer", "ui designer": "ui_ux_designer",
    "product designer": "ui_ux_designer", "interaction designer": "ui_ux_designer",
    "qa engineer": "qa_automation_engineer", "sdet": "qa_automation_engineer",
    "test engineer": "qa_automation_engineer", "automation engineer": "qa_automation_engineer",
    "software tester": "qa_automation_engineer", "quality analyst": "qa_automation_engineer",
    "ba": "business_analyst", "systems analyst": "business_analyst",
    "functional consultant": "business_analyst", "process analyst": "business_analyst",
    "dba": "database_administrator", "database engineer": "database_administrator",
    "game programmer": "game_developer", "unity developer": "game_developer",
    "gameplay engineer": "game_developer",
    "smart contract developer": "blockchain_developer", "web3 developer": "blockchain_developer",
    "solidity developer": "blockchain_developer", "dapp developer": "blockchain_developer",
    "firmware engineer": "embedded_iot_engineer", "iot engineer": "embedded_iot_engineer",
    "embedded engineer": "embedded_iot_engineer", "embedded developer": "embedded_iot_engineer",
    "network administrator": "network_engineer", "network admin": "network_engineer",
    "network architect": "network_engineer", "noc engineer": "network_engineer",
    "product owner": "product_manager", "apm": "product_manager",
    "associate product manager": "product_manager", "technical program manager": "product_manager",
}


# ==========================================
# 6. Derived Lookups (computed once at import)
# ==========================================
# Backwards-compatible roadmap map: {skill_name: [step, step, ...]}
SKILL_ROADMAPS = {
    name: info["roadmap"] for name, info in SKILL_LIBRARY.items()
}

# {category_name: [skill, skill, ...]} used by the profile form and /api/skills
SKILL_CATEGORIES = {}
for _name, _info in SKILL_LIBRARY.items():
    SKILL_CATEGORIES.setdefault(_info["category"], []).append(_name)

# Fast career lookup by id
CAREER_INDEX = {career["id"]: career for career in CAREER_DATABASE}

# Flat catalogs
ALL_SKILLS = sorted(SKILL_LIBRARY.keys())
ALL_INTERESTS = sorted({
    interest
    for group in INTEREST_LIBRARY.values()
    for interest in group
})

# Lowercase lookup so matching stays case-insensitive without rebuilding maps
SKILL_LOOKUP_LOWER = {name.lower(): name for name in SKILL_LIBRARY}


# ==========================================
# 7. Knowledge Base Helpers
# ==========================================
def canonical_skill(raw_skill):
    """
    Maps a user-entered skill to its canonical library name.
    Handles case, surrounding whitespace and the SKILL_ALIASES synonyms, e.g.
    "  reactJS " -> "React", "ml" -> "Machine Learning".
    Returns the cleaned original string when the skill is unknown, so custom
    skills typed by a student are never silently dropped.
    """
    if not isinstance(raw_skill, str):
        return ""

    cleaned = raw_skill.strip()
    if not cleaned:
        return ""

    lowered = cleaned.lower()

    # 1. Exact library match (case-insensitive)
    if lowered in SKILL_LOOKUP_LOWER:
        return SKILL_LOOKUP_LOWER[lowered]

    # 2. Known alias / short form
    if lowered in SKILL_ALIASES:
        return SKILL_ALIASES[lowered]

    # 3. Unknown skill: keep what the student typed
    return cleaned


def get_skill_meta(skill_name):
    """
    Returns the library entry for a skill, or a safe default for skills that
    are not in the knowledge base (student-typed or newly added career skills).
    """
    info = SKILL_LIBRARY.get(skill_name)
    if info:
        return {
            "skill": skill_name,
            "category": info["category"],
            "difficulty": info["difficulty"],
            "learning_hours": info["learning_hours"],
            "prerequisites": list(info["prerequisites"]),
            "resources": list(info["resources"]),
            "roadmap": list(info["roadmap"]),
            "in_knowledge_base": True
        }

    return {
        "skill": skill_name,
        "category": "Other",
        "difficulty": "Intermediate",
        "learning_hours": 40,
        "prerequisites": [],
        "resources": ["Official documentation", "A free YouTube crash course", "One hands-on tutorial project"],
        "roadmap": [
            "Step 1: Learn the fundamental concepts and syntax of {0}.".format(skill_name),
            "Step 2: Practise hands-on exercises and mini challenges with {0}.".format(skill_name),
            "Step 3: Build a small portfolio project applying {0} to solve a real problem.".format(skill_name)
        ],
        "in_knowledge_base": False
    }


def get_career_by_id(career_id):
    """Returns a career dict by id, or None when the id is unknown."""
    if not isinstance(career_id, str):
        return None
    return CAREER_INDEX.get(career_id.strip().lower())


def resolve_goal_to_career_id(goal_text):
    """
    Resolves a free-text career goal to a career id using, in order:
    1. an exact career title match ("data analyst")
    2. the career id typed with spaces ("ai ml engineer")
    3. the CAREER_GOAL_ALIASES job-title synonyms ("ml engineer")
    Returns None when the goal does not clearly point at one career.
    """
    if not isinstance(goal_text, str):
        return None

    goal = goal_text.strip().lower()
    if not goal:
        return None

    for career in CAREER_DATABASE:
        if goal == career["title"].lower():
            return career["id"]
        if goal == career["id"].replace("_", " "):
            return career["id"]

    return CAREER_GOAL_ALIASES.get(goal)


def knowledge_base_stats():
    """Summary counts, used by the /api/stats endpoint and the verify script."""
    total_stages = sum(len(c.get("career_path", [])) for c in CAREER_DATABASE)
    return {
        "total_careers": len(CAREER_DATABASE),
        "total_skills": len(SKILL_LIBRARY),
        "total_skill_aliases": len(SKILL_ALIASES),
        "total_skill_categories": len(SKILL_CATEGORIES),
        "total_interests": len(ALL_INTERESTS),
        "total_career_stages": total_stages,
        "total_roadmap_steps": sum(len(steps) for steps in SKILL_ROADMAPS.values()),
        "career_categories": sorted({c["category"] for c in CAREER_DATABASE}),
        "weights": dict(MATCH_WEIGHTS)
    }


def validate_knowledge_base():
    """
    Consistency checks for the static data. Returns a list of human-readable
    problems (empty list means the knowledge base is internally consistent).
    Used by the test suite and verify_backend.py so a typo in this file is
    caught immediately instead of producing a silently wrong roadmap.
    """
    problems = []
    seen_ids = set()

    for career in CAREER_DATABASE:
        cid = career.get("id", "<missing id>")

        if cid in seen_ids:
            problems.append("Duplicate career id: {0}".format(cid))
        seen_ids.add(cid)

        for field in ("title", "description", "required_skills", "core_skills",
                      "relevant_interests", "recommended_education",
                      "education_keywords", "career_path"):
            if not career.get(field):
                problems.append("Career '{0}' is missing field '{1}'".format(cid, field))

        # Core skills must be part of the required skill set
        for core in career.get("core_skills", []):
            if core not in career.get("required_skills", []):
                problems.append(
                    "Career '{0}' lists core skill '{1}' that is not in required_skills".format(cid, core)
                )

        # Every required skill should exist in the skill library
        for skill in career.get("required_skills", []):
            if skill not in SKILL_LIBRARY:
                problems.append("Career '{0}' requires unknown skill '{1}'".format(cid, skill))

        # Interests must be offered somewhere in the form catalog
        for interest in career.get("relevant_interests", []):
            if interest not in ALL_INTERESTS:
                problems.append("Career '{0}' uses interest '{1}' missing from INTEREST_LIBRARY".format(cid, interest))

        # Related careers must resolve
        for related in career.get("related_careers", []):
            if related not in CAREER_INDEX:
                problems.append("Career '{0}' points to unknown related career '{1}'".format(cid, related))

        # Progression ladder sanity
        for index, stage in enumerate(career.get("career_path", []), start=1):
            for field in ("level", "role", "experience", "salary_inr", "focus", "milestone"):
                if not stage.get(field):
                    problems.append(
                        "Career '{0}' stage {1} is missing '{2}'".format(cid, index, field)
                    )
            for skill in stage.get("skills_to_add", []):
                if skill not in SKILL_LIBRARY:
                    problems.append(
                        "Career '{0}' stage {1} references unknown skill '{2}'".format(cid, index, skill)
                    )

    # Skill library internal checks
    for name, info in SKILL_LIBRARY.items():
        if info.get("difficulty") not in DIFFICULTY_ORDER:
            problems.append("Skill '{0}' has invalid difficulty '{1}'".format(name, info.get("difficulty")))
        if not isinstance(info.get("learning_hours"), int) or info["learning_hours"] <= 0:
            problems.append("Skill '{0}' has invalid learning_hours".format(name))
        if not info.get("roadmap"):
            problems.append("Skill '{0}' has no roadmap steps".format(name))
        for prereq in info.get("prerequisites", []):
            if prereq not in SKILL_LIBRARY:
                problems.append("Skill '{0}' depends on unknown prerequisite '{1}'".format(name, prereq))
            if prereq == name:
                problems.append("Skill '{0}' lists itself as a prerequisite".format(name))

    # Aliases must resolve to real skills
    for alias, target in SKILL_ALIASES.items():
        if target not in SKILL_LIBRARY:
            problems.append("Alias '{0}' points to unknown skill '{1}'".format(alias, target))
        if alias != alias.lower():
            problems.append("Alias '{0}' must be lowercase to be matched".format(alias))
        if alias in SKILL_LOOKUP_LOWER:
            problems.append("Alias '{0}' shadows a real skill name".format(alias))

    # Career goal aliases must resolve to real careers
    for alias, career_id in CAREER_GOAL_ALIASES.items():
        if career_id not in CAREER_INDEX:
            problems.append("Goal alias '{0}' points to unknown career '{1}'".format(alias, career_id))
        if alias != alias.lower():
            problems.append("Goal alias '{0}' must be lowercase to be matched".format(alias))

    return problems
