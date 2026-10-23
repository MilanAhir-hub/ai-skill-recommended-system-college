"""
database.py
-----------
Handles SQLite database connection, table initialization, and user CRUD operations.
Uses Python's built-in sqlite3 library.
"""

import json
import sqlite3
import os

# Default SQLite database filename
DEFAULT_DB_PATH = "career_system.db"


def get_db_path(custom_path=None):
    """
    Returns the database file path.
    Uses custom_path if provided, then checks DB_PATH environment variable,
    and falls back to DEFAULT_DB_PATH.
    """
    if custom_path:
        return custom_path
    return os.environ.get("DB_PATH", DEFAULT_DB_PATH)


def get_db_connection(db_path=None):
    """
    Opens and returns a connection to the SQLite database.
    Sets row_factory to sqlite3.Row so columns can be accessed by name.
    """
    path = get_db_path(db_path)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    """
    Creates required tables automatically if they do not already exist.
    Called when the Flask app starts.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # Create the users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            education TEXT,
            skills TEXT NOT NULL,
            interests TEXT NOT NULL,
            career_goal TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()


def create_user(name, education, skills, interests, career_goal=None, db_path=None):
    """
    Inserts a new user profile into SQLite.
    Skills and interests lists are converted to JSON strings for storage.
    Returns the newly created user as a dictionary.
    """
    # Ensure skills and interests are lists
    skills_list = skills if isinstance(skills, list) else []
    interests_list = interests if isinstance(interests, list) else []

    # Convert Python lists to JSON strings for SQLite storage
    skills_json = json.dumps(skills_list)
    interests_json = json.dumps(interests_list)

    # Clean strings
    clean_name = name.strip() if name else ""
    clean_education = education.strip() if education else ""
    clean_career_goal = career_goal.strip() if career_goal else ""

    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (name, education, skills, interests, career_goal)
        VALUES (?, ?, ?, ?, ?)
    """, (clean_name, clean_education, skills_json, interests_json, clean_career_goal))

    conn.commit()
    user_id = cursor.lastrowid

    # Fetch the newly created record
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    return format_user_row(row)


def get_user_by_id(user_id, db_path=None):
    """
    Retrieves a user profile by ID from the database.
    Returns None if user does not exist.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return format_user_row(row)


def format_user_row(row):
    """
    Helper function to convert an SQLite row into a clean Python dictionary.
    Deserializes skills and interests from JSON strings to Python lists.
    """
    if row is None:
        return None

    # Safely load JSON or fallback to empty list
    try:
        skills = json.loads(row["skills"]) if row["skills"] else []
    except Exception:
        skills = []

    try:
        interests = json.loads(row["interests"]) if row["interests"] else []
    except Exception:
        interests = []

    return {
        "id": row["id"],
        "name": row["name"],
        "education": row["education"] or "",
        "skills": skills,
        "interests": interests,
        "career_goal": row["career_goal"] or "",
        "created_at": str(row["created_at"])
    }
