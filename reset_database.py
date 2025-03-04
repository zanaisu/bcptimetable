#!/usr/bin/env python3
from app import create_app, db
import os
import logging

def reset_database():
    """Reset the database to a clean state with the new schema."""
    app = create_app()
    
    with app.app_context():
        # Import all models to register them with SQLAlchemy
        from app.models.user import User
        from app.models.task import Task 
        from app.models.subject import Subject
        from app.models.topic import Topic, TopicConfidence, SubtopicConfidence
        
        # Check for all possible database locations and remove them
        possible_paths = [
            os.path.join(app.instance_path, 'timetable.db'),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'timetable.db'),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'timetable.db')
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    os.remove(path)
                    print(f"Removed database file: {path}")
                except Exception as e:
                    print(f"Could not remove {path}: {e}")
        
        # Create all tables based on the updated schema
        try:
            db.create_all()
            print("Created new database tables with updated schema.")
            print(f"Database created at: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Initialize with curriculum data
            from app.init_db import init_db as load_curriculum
            load_curriculum()
            print("Initialized database with curriculum data.")
            
            print("Database reset complete!")
        except Exception as e:
            logging.error(f"Error creating database: {str(e)}")
            print(f"Error: {str(e)}")
            raise

if __name__ == "__main__":
    reset_database()