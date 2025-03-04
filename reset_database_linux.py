#!/usr/bin/env python3
"""
Reset database script that works in a Linux environment.
This creates a new SQLite database file with the correct schema.
"""
import os
import sys
import sqlite3

# Create instance directory if it doesn't exist
os.makedirs('instance', exist_ok=True)

# Create database file
db_path = os.path.join('instance', 'timetable.db')
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Removed existing database file: {db_path}")

# Create tables manually
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(64) UNIQUE,
    email VARCHAR(120) UNIQUE,
    password_hash VARCHAR(128),
    created_at TIMESTAMP,
    study_hours_per_day FLOAT,
    weekend_points_goal INTEGER,
    uplearn_biology BOOLEAN,
    uplearn_chemistry BOOLEAN,
    dark_mode BOOLEAN,
    is_first_login BOOLEAN
)
''')

# Create subjects table
cursor.execute('''
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY,
    name VARCHAR(64),
    title VARCHAR(128)
)
''')

# Create topics table
cursor.execute('''
CREATE TABLE topics (
    id INTEGER PRIMARY KEY,
    title VARCHAR(128),
    content TEXT,
    subject_id INTEGER,
    module_name VARCHAR(64),
    parent_topic_id INTEGER,
    is_subtopic BOOLEAN,
    FOREIGN KEY (subject_id) REFERENCES subjects (id),
    FOREIGN KEY (parent_topic_id) REFERENCES topics (id)
)
''')

# Create topic_confidences table with topic_key
cursor.execute('''
CREATE TABLE topic_confidences (
    id INTEGER PRIMARY KEY,
    confidence_level INTEGER,
    topic_key VARCHAR(128),
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

# Create subtopic_confidences table
cursor.execute('''
CREATE TABLE subtopic_confidences (
    id INTEGER PRIMARY KEY,
    confidence_level INTEGER,
    subtopic_key VARCHAR(128),
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

# Create tasks table
cursor.execute('''
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title VARCHAR(128),
    description TEXT,
    duration INTEGER,
    points INTEGER,
    task_type VARCHAR(64),
    completed BOOLEAN,
    skipped BOOLEAN,
    date_assigned DATE,
    date_completed DATE,
    user_id INTEGER,
    subject_id INTEGER,
    topic_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (subject_id) REFERENCES subjects (id),
    FOREIGN KEY (topic_id) REFERENCES topics (id)
)
''')

# Commit and close
conn.commit()
conn.close()

print("Created new database tables with updated schema.")
print("Database reset complete!")