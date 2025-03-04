from app import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.Text, nullable=True)
    task_type = db.Column(db.String(64))  # 'mind_map', 'past_paper', 'uplearn', etc.
    duration = db.Column(db.Integer, default=60)  # Duration in minutes
    points = db.Column(db.Integer, default=1)
    
    # Date information
    date_assigned = db.Column(db.Date, default=datetime.utcnow().date)
    date_completed = db.Column(db.Date, nullable=True)
    
    # Status
    completed = db.Column(db.Boolean, default=False)
    skipped = db.Column(db.Boolean, default=False)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=True)
    
    def __repr__(self):
        return f'<Task {self.title}>'
    
    def mark_completed(self):
        self.completed = True
        self.date_completed = datetime.utcnow().date
        
    def mark_skipped(self):
        self.skipped = True