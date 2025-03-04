from app import db

class Topic(db.Model):
    __tablename__ = 'topics'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    content = db.Column(db.Text, nullable=True)
    
    # Foreign keys
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    module_name = db.Column(db.String(64), nullable=True)
    parent_topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=True)
    
    # Relationships
    tasks = db.relationship('Task', backref='topic', lazy='dynamic')
    subtopics = db.relationship('Topic', backref=db.backref('parent_topic', remote_side=[id]), lazy='dynamic')
    
    # Topic type (main topic or subtopic)
    is_subtopic = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Topic {self.title}>'


class TopicConfidence(db.Model):
    __tablename__ = 'topic_confidences'
    
    id = db.Column(db.Integer, primary_key=True)
    confidence_level = db.Column(db.Integer, default=3)  # Scale of 1-5
    topic_key = db.Column(db.String(128), nullable=False)  # e.g., "topic_Module1_BY12"
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<TopicConfidence user_id={self.user_id} topic_key={self.topic_key} level={self.confidence_level}>'


class SubtopicConfidence(db.Model):
    __tablename__ = 'subtopic_confidences'
    
    id = db.Column(db.Integer, primary_key=True)
    confidence_level = db.Column(db.Integer, default=3)  # Scale of 1-5
    subtopic_key = db.Column(db.String(128), nullable=False)  # e.g., "Module1_Cell_structure_BY12"
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<SubtopicConfidence user_id={self.user_id} subtopic_key={self.subtopic_key} level={self.confidence_level}>'
    
    @staticmethod
    def calculate_topic_confidence(user_id, topic_key):
        """Calculate topic confidence based on related subtopic confidences"""
        # Extract the module/paper and subject from the topic key
        # e.g., "topic_Module1_BY12" -> ["topic", "Module1", "BY12"]
        parts = topic_key.split('_')
        if len(parts) < 3:
            return 3  # Default
            
        module_name = parts[1]
        subject_code = parts[2]
        
        # Find all subtopics for this module and subject
        subtopics = SubtopicConfidence.query.filter(
            SubtopicConfidence.user_id == user_id,
            SubtopicConfidence.subtopic_key.like(f"{module_name}_%_{subject_code}")
        ).all()
        
        if not subtopics:
            return 3  # Default if no subtopics found
            
        # Calculate average confidence
        total = sum(st.confidence_level for st in subtopics)
        return round(total / len(subtopics))