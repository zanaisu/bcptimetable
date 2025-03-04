from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize SQLAlchemy with less strict settings
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    # Create Flask app with app directory as the instance path
    # This aligns with where the database is already being created
    app_dir = os.path.abspath(os.path.dirname(__file__))
    instance_path = os.path.join(app_dir, 'instance')
    app = Flask(__name__, instance_path=instance_path)
    
    # Configure app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')
    
    # GitHub configuration
    app.config['GITHUB_CLIENT_ID'] = os.environ.get('GITHUB_CLIENT_ID')
    app.config['GITHUB_CLIENT_SECRET'] = os.environ.get('GITHUB_CLIENT_SECRET')
    app.config['GITHUB_CALLBACK_URL'] = os.environ.get('GITHUB_CALLBACK_URL', 'http://localhost:5000/auth/github/callback')
    
    # Get database URL with a fallback to SQLite
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///timetable.db')
    
    # Handle Railway's "postgres://" format (if needed)
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Ensure instance path exists
    os.makedirs(instance_path, exist_ok=True)
    
    # Log where database is expected to be created
    db_dir = os.path.dirname(os.path.abspath(__file__))
    expected_db_path = os.path.join(db_dir, 'timetable.db')
    print(f"Expected database path: {expected_db_path}")
    
    # Initialize extensions with app context
    with app.app_context():
        # Initialize extensions
        db.init_app(app)
        migrate.init_app(app, db)
        login_manager.init_app(app)
        login_manager.login_view = 'auth.login'
    
        try:
            # Import and register blueprints
            from app.routes.auth import auth as auth_blueprint
            app.register_blueprint(auth_blueprint)
            
            from app.routes.main import main as main_blueprint
            app.register_blueprint(main_blueprint)
        except Exception as e:
            app.logger.error(f"Error registering blueprints: {str(e)}")
    
    # Add an error handler
    @app.errorhandler(500)
    def handle_500(error):
        return "Internal Server Error. Please check the logs.", 500
    
    return app