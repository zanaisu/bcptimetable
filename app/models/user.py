from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # User settings
    study_hours_per_day = db.Column(db.Float, default=4.0)
    weekend_points_goal = db.Column(db.Integer, default=30)
    uplearn_biology = db.Column(db.Boolean, default=False)
    uplearn_chemistry = db.Column(db.Boolean, default=False)
    
    # Dark mode preference
    dark_mode = db.Column(db.Boolean, default=False)
    
    # Relationships
    tasks = db.relationship('Task', backref='user', lazy='dynamic')
    topic_confidences = db.relationship('TopicConfidence', backref='user', lazy='dynamic')
    subtopic_confidences = db.relationship('SubtopicConfidence', backref='user', lazy='dynamic')
    
    # First login flag
    is_first_login = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'