from app import create_app, db
from flask_migrate import upgrade
import os
import sys

app = create_app()

@app.cli.command("create-tables")
def create_tables():
    """Create tables."""
    # Import all models to ensure they're registered with SQLAlchemy
    from app.models.user import User
    from app.models.task import Task
    from app.models.subject import Subject
    from app.models.topic import Topic, TopicConfidence, SubtopicConfidence
    
    db.create_all()
    print("Tables created successfully.")

@app.cli.command("init-db")
def init_db():
    """Initialize the database with curriculum data."""
    # First create the tables
    from app.models.user import User
    from app.models.task import Task
    from app.models.subject import Subject
    from app.models.topic import Topic, TopicConfidence, SubtopicConfidence
    
    db.create_all()
    
    # Initialize with curriculum data
    from app.init_db import init_db as load_curriculum
    with app.app_context():
        load_curriculum()
    
    print("Database initialized successfully.")

def reset_db_function():
    """Reset the database by dropping all tables and recreating them."""
    # Check if database file exists and remove it
    db_path = os.path.join(app.instance_path, 'timetable.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database file: {db_path}")
    
    # Import all models to ensure they're registered with SQLAlchemy
    from app.models.user import User
    from app.models.task import Task
    from app.models.subject import Subject
    from app.models.topic import Topic, TopicConfidence, SubtopicConfidence
    
    # Create all tables
    with app.app_context():
        db.create_all()
        print("Tables created successfully.")
        
        # Initialize with curriculum data
        from app.init_db import init_db as load_curriculum
        load_curriculum()
            
    print("Database reset and initialized successfully.")

@app.cli.command("reset-db")
def reset_db():
    reset_db_function()
    
if __name__ == '__main__':
    # Check if command line arguments are provided
    if len(sys.argv) > 1:
        # Process commands
        if sys.argv[1] == 'reset-db':
            reset_db_function()
            sys.exit(0)
    
    # Otherwise, run the Flask app
    app.run(debug=True)