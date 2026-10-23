"""
career_data.py
--------------
This file stores the static knowledge base for the career recommendation system:
1. Matching weights (Skill: 50%, Interest: 30%, Education: 20%)
2. Career profiles (Software Developer, Web Developer, Data Analyst, AI/ML Engineer, Cybersecurity Analyst)
3. Step-by-step learning roadmaps for technical skills
"""

# ==========================================
# 1. Configurable Matching Weights
# ==========================================
# Skill match = 50%, Interest match = 30%, Education match = 20%
# All weights sum up to 1.0 (100%)
MATCH_WEIGHTS = {
    "skill": 0.50,
    "interest": 0.30,
    "education": 0.20
}

# ==========================================
# 2. Career Dataset
# ==========================================
# Rule-based knowledge base of career paths and requirements
CAREER_DATABASE = [
    {
        "id": "software_developer",
        "title": "Software Developer",
        "description": "Designs, develops, tests, and maintains scalable software applications and system tools.",
        "required_skills": [
            "Python",
            "Java",
            "Data Structures & Algorithms",
            "Git",
            "SQL"
        ],
        "relevant_interests": [
            "Problem Solving",
            "Software Architecture",
            "Coding",
            "Open Source"
        ],
        "recommended_education": "Bachelor's Degree in Computer Science, Information Technology, or related STEM field",
        "education_keywords": [
            "computer science", "information technology", "b.tech", "b.e", "bca", "mca", "b.sc cs", "software engineering"
        ]
    },
    {
        "id": "web_developer",
        "title": "Web Developer",
        "description": "Builds and maintains responsive client-facing websites and full-stack web applications.",
        "required_skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Node.js",
            "Git"
        ],
        "relevant_interests": [
            "Web Applications",
            "UI/UX Design",
            "Frontend Development",
            "Creative Design"
        ],
        "recommended_education": "Diploma, Associate, or Bachelor's Degree in Computer Science or Web Development (or self-taught/bootcamp)",
        "education_keywords": [
            "computer science", "information technology", "web development", "bca", "diploma", "b.tech", "b.e", "any"
        ]
    },
    {
        "id": "data_analyst",
        "title": "Data Analyst",
        "description": "Inspects, cleans, transforms, and models data to discover useful insights and support business decisions.",
        "required_skills": [
            "Python",
            "SQL",
            "Excel",
            "Data Visualization",
            "Power BI",
            "Statistics"
        ],
        "relevant_interests": [
            "Data Analysis",
            "Business Intelligence",
            "Problem Solving",
            "Statistics"
        ],
        "recommended_education": "Bachelor's Degree in Statistics, Mathematics, Economics, Computer Science, or Business",
        "education_keywords": [
            "statistics", "mathematics", "economics", "computer science", "data science", "business", "bca", "b.tech"
        ]
    },
    {
        "id": "ai_ml_engineer",
        "title": "AI/ML Engineer",
        "description": "Researches, builds, and designs self-running artificial intelligence systems and machine learning models.",
        "required_skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "Mathematics",
            "Statistics",
            "SQL"
        ],
        "relevant_interests": [
            "Artificial Intelligence",
            "Machine Learning",
            "Data Science",
            "Research"
        ],
        "recommended_education": "Bachelor's or Master's Degree in Computer Science, Data Science, AI, or Mathematics",
        "education_keywords": [
            "computer science", "data science", "artificial intelligence", "mathematics", "m.tech", "b.tech", "mca", "m.sc"
        ]
    },
    {
        "id": "cybersecurity_analyst",
        "title": "Cybersecurity Analyst",
        "description": "Monitors, detects, investigates, and prevents cyber threats and unauthorized access to digital systems.",
        "required_skills": [
            "Network Security",
            "Linux",
            "Ethical Hacking",
            "Cryptography",
            "Python",
            "SIEM"
        ],
        "relevant_interests": [
            "Cybersecurity",
            "Information Security",
            "Ethical Hacking",
            "Network Defense"
        ],
        "recommended_education": "Bachelor's Degree in Cybersecurity, Computer Science, Information Technology, or related discipline",
        "education_keywords": [
            "cybersecurity", "information security", "computer science", "information technology", "b.tech", "bca"
        ]
    }
]

# ==========================================
# 3. Predefined Skill Learning Roadmaps
# ==========================================
# Concrete, step-by-step learning milestones for each technical skill
SKILL_ROADMAPS = {
    "Python": [
        "Step 1: Master Python fundamentals (variables, loops, conditionals, functions, lists/dictionaries).",
        "Step 2: Learn Object-Oriented Programming (classes, objects, inheritance) and file I/O operations.",
        "Step 3: Build a practical CLI project (e.g., student management system or web scraper)."
    ],
    "Java": [
        "Step 1: Learn Java syntax, primitive types, and control flow.",
        "Step 2: Understand core OOP principles, Java Collections Framework (ArrayList, HashMap), and exception handling.",
        "Step 3: Build a console application and explore build tools like Maven or Gradle."
    ],
    "Data Structures & Algorithms": [
        "Step 1: Study linear data structures (arrays, linked lists, stacks, queues).",
        "Step 2: Learn non-linear structures (trees, binary search trees, graphs) and Big-O notation.",
        "Step 3: Practice sorting, searching, and recursion problems on LeetCode/HackerRank."
    ],
    "Git": [
        "Step 1: Understand version control concepts and configure Git with GitHub/GitLab.",
        "Step 2: Master basic commands: git init, add, commit, push, pull, and status.",
        "Step 3: Learn branch management, merging, pull requests, and resolving merge conflicts."
    ],
    "SQL": [
        "Step 1: Learn relational database basics and basic SQL queries (SELECT, WHERE, ORDER BY, LIMIT).",
        "Step 2: Master aggregate functions, GROUP BY, HAVING, and table JOINs (INNER, LEFT, RIGHT).",
        "Step 3: Practice database schema design, subqueries, and indexing with SQLite or PostgreSQL."
    ],
    "HTML": [
        "Step 1: Learn HTML5 document structure, semantic tags (header, nav, section, footer), and text elements.",
        "Step 2: Master forms, input validation types, tables, and multimedia tags (audio, video).",
        "Step 3: Build a semantic, accessible multi-page personal portfolio skeleton."
    ],
    "CSS": [
        "Step 1: Understand the CSS box model, selectors, typography, and colors.",
        "Step 2: Master Flexbox and CSS Grid layout systems for responsive design.",
        "Step 3: Learn CSS transitions, media queries, and style your portfolio project beautifully."
    ],
    "JavaScript": [
        "Step 1: Learn JavaScript syntax, variables (let/const), functions, arrays, and objects.",
        "Step 2: Master DOM manipulation, event handling, and ES6+ features (arrow functions, destructuring, promises).",
        "Step 3: Learn Fetch API / async-await and build an interactive project like a Weather App."
    ],
    "React": [
        "Step 1: Understand React JSX syntax, components, props, and component state.",
        "Step 2: Master React Hooks (useState, useEffect, useContext) and handling events.",
        "Step 3: Build a full single-page application with component-driven architecture."
    ],
    "Node.js": [
        "Step 1: Understand Node.js runtime environment, npm, and asynchronous programming in Node.",
        "Step 2: Build RESTful APIs using Express.js framework and middleware.",
        "Step 3: Connect Express to a database (MongoDB or SQLite) and implement CRUD operations."
    ],
    "Excel": [
        "Step 1: Master basic Excel formulas (SUM, AVERAGE, COUNTIF) and data formatting.",
        "Step 2: Learn lookup functions (VLOOKUP, XLOOKUP, INDEX/MATCH) and conditional formatting.",
        "Step 3: Build dynamic Pivot Tables and interactive summary dashboards."
    ],
    "Data Visualization": [
        "Step 1: Learn data visualization principles (choosing the right chart for data types).",
        "Step 2: Practice creating bar charts, line plots, heatmaps, and scatter plots in Matplotlib and Seaborn.",
        "Step 3: Build an end-to-end exploratory data visualization report on an open dataset."
    ],
    "Power BI": [
        "Step 1: Learn Power BI Desktop interface and importing data from CSV/Excel/SQL.",
        "Step 2: Perform data cleaning with Power Query and write basic DAX measures.",
        "Step 3: Design interactive business intelligence dashboards with drill-downs and filters."
    ],
    "Statistics": [
        "Step 1: Study descriptive statistics (mean, median, mode, variance, standard deviation).",
        "Step 2: Understand probability distributions (normal distribution, binomial) and central limit theorem.",
        "Step 3: Learn inferential statistics: hypothesis testing (p-value, t-test, chi-square test, A/B testing)."
    ],
    "Mathematics": [
        "Step 1: Review Linear Algebra fundamentals (vectors, matrices, matrix multiplication, dot products).",
        "Step 2: Understand Multivariable Calculus (derivatives, partial derivatives, gradients, gradient descent).",
        "Step 3: Study Probability Theory and basic optimization techniques used in ML."
    ],
    "Machine Learning": [
        "Step 1: Learn supervised learning algorithms (Linear Regression, Logistic Regression, Decision Trees, Random Forests).",
        "Step 2: Learn unsupervised learning (K-Means Clustering, PCA) and model evaluation metrics (accuracy, precision, recall, F1, ROC-AUC).",
        "Step 3: Build an end-to-end ML classification or prediction pipeline with scikit-learn."
    ],
    "Deep Learning": [
        "Step 1: Understand artificial neural networks, activation functions, loss functions, and backpropagation.",
        "Step 2: Learn Convolutional Neural Networks (CNN) for image tasks and Recurrent Neural Networks (RNN) or Transformers for sequence data.",
        "Step 3: Train and evaluate a deep learning model using PyTorch or TensorFlow."
    ],
    "Network Security": [
        "Step 1: Understand TCP/IP networking models, DNS, HTTP/HTTPS, subnetting, and ports.",
        "Step 2: Learn firewall configurations, VPNs, IDS/IPS, and packet inspection using Wireshark.",
        "Step 3: Practice network security auditing and vulnerability scanning with Nmap."
    ],
    "Linux": [
        "Step 1: Master Linux directory navigation, file permissions (chmod, chown), and basic shell commands.",
        "Step 2: Learn process management (ps, top, kill), package managers (apt), and SSH.",
        "Step 3: Write basic Bash automation scripts and configure system security services."
    ],
    "Ethical Hacking": [
        "Step 1: Understand the phases of ethical hacking (reconnaissance, scanning, gaining access, maintaining access).",
        "Step 2: Learn OWASP Top 10 web vulnerabilities (SQL Injection, XSS, CSRF, Broken Auth).",
        "Step 3: Practice hands-on security labs on platforms like TryHackMe or PortSwigger Web Security Academy."
    ],
    "Cryptography": [
        "Step 1: Understand symmetric vs. asymmetric encryption algorithms (AES, RSA).",
        "Step 2: Learn hashing algorithms (SHA-256), digital signatures, and public key infrastructure (PKI/SSL/TLS certificates).",
        "Step 3: Implement basic encryption/decryption workflows in Python using cryptography libraries."
    ],
    "SIEM": [
        "Step 1: Understand the purpose of Security Information and Event Management (SIEM) systems and log analysis.",
        "Step 2: Learn log ingestion, correlation rules, and threat detection fundamentals.",
        "Step 3: Practice alert triage and incident investigation on an open SIEM platform (e.g., Splunk Free or Wazuh)."
    ]
}
