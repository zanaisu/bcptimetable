#!/usr/bin/env python3
"""
Direct database initialization script for troubleshooting.
This script creates the database tables directly without any batch file intermediary.
"""
import os
import sys
import time
import sqlite3

print("Starting database initialization...")

# Import all necessary models
try:
    from app import create_app, db
    from app.models.user import User
    from app.models.task import Task
    from app.models.subject import Subject
    from app.models.topic import Topic, TopicConfidence, SubtopicConfidence
    
    print("Models imported successfully.")
except Exception as e:
    print(f"Error importing models: {e}")
    sys.exit(1)

# Create app
try:
    app = create_app()
    print(f"App created. Instance path: {app.instance_path}")
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
except Exception as e:
    print(f"Error creating app: {e}")
    sys.exit(1)

# Ensure app instance directory exists
app_dir = os.path.dirname(os.path.abspath(__file__))
app_module_dir = os.path.join(app_dir, 'app')
instance_path = os.path.join(app_module_dir, 'instance')
os.makedirs(instance_path, exist_ok=True)
print(f"App instance directory ensured: {instance_path}")

# Get database path - adjusted for relative SQLite path
db_path = None
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
    relative_path = app.config['SQLALCHEMY_DATABASE_URI'][10:]
    db_path = os.path.join(app_module_dir, relative_path)
    print(f"Identified SQLite database path: {db_path}")
else:
    print(f"Not a SQLite database or path could not be extracted.")

# Create database tables
try:
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")
        
        # Verify tables were created
        if db_path and os.path.exists(db_path):
            try:
                # Connect to the database and check tables
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # List all tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                print(f"Tables in database: {[table[0] for table in tables]}")
                
                # Check if users table exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
                if cursor.fetchone():
                    print("Users table exists.")
                else:
                    print("WARNING: Users table does not exist!")
                
                conn.close()
            except Exception as e:
                print(f"Error inspecting database: {e}")
        else:
            print(f"WARNING: Database file not found at {db_path}")
except Exception as e:
    print(f"Error creating database tables: {e}")
    sys.exit(1)

# Load curriculum data
try:
    from app.init_db import init_db
    
    with app.app_context():
        init_db()
        print("Curriculum data loaded successfully.")
except Exception as e:
    print(f"Error loading curriculum data: {e}")
    sys.exit(1)

print("Database initialization completed successfully.")