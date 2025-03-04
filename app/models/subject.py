from app import db

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    title = db.Column(db.String(128))
    
    # Relationships
    topics = db.relationship('Topic', backref='subject', lazy='dynamic')
    tasks = db.relationship('Task', backref='subject', lazy='dynamic')
    
    def __repr__(self):
        return f'<Subject {self.name}>'