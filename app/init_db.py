import json
import os
import logging
from app import db

def init_db():
    """Initialize the database with curriculum data."""
    try:
        from app.models.subject import Subject
        from app.models.topic import Topic, TopicConfidence, SubtopicConfidence
        
        # Check if subjects already exist
        if Subject.query.count() > 0:
            print("Database already initialized. Skipping...")
            return
        
        # Load curriculum JSON file
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        curriculum_path = os.path.join(data_dir, 'curriculum.json')
        
        try:
            with open(curriculum_path, 'r') as f:
                curriculum_data = json.load(f)
        except Exception as e:
            logging.error(f"Error loading curriculum data: {str(e)}")
            raise
        
        # Create subjects
        subjects = {
            'Biology Year 12': Subject(name='Biology Year 12', title=curriculum_data['Biology Year 12']['Title']),
            'Biology Year 13': Subject(name='Biology Year 13', title=curriculum_data['Biology Year 13']['Title']),
            'Chemistry': Subject(name='Chemistry', title=curriculum_data['Chemistry']['Title']),
            'Psychology': Subject(name='Psychology', title=curriculum_data['Psychology']['Title'])
        }
        
        # Add subjects to database
        for subject in subjects.values():
            db.session.add(subject)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error committing subjects: {str(e)}")
            raise
        
        try:
            # Create main topics
            main_topics = {}
            
            # Biology Year 12 topics
            for topic_group in curriculum_data['Biology Year 12']['Topics']:
                module_name = topic_group['Name'].replace(' ', '')  # e.g., "Module1"
                topic_key = f"{module_name}_BY12"
                parent_topic = Topic(
                    title=topic_group['Title'],
                    content=topic_group['Description'],
                    subject_id=subjects['Biology Year 12'].id,
                    module_name=topic_group['Name'] + ': ' + topic_group['Title'],
                    is_subtopic=False
                )
                db.session.add(parent_topic)
                db.session.flush()  # Get ID before committing
                main_topics[topic_key] = parent_topic.id
                
                for subtopic in topic_group['Subtopics']:
                    topic = Topic(
                        title=subtopic['Title'],
                        content=subtopic['Description'],
                        subject_id=subjects['Biology Year 12'].id,
                        module_name=topic_group['Name'] + ': ' + topic_group['Title'],
                        parent_topic_id=parent_topic.id,
                        is_subtopic=True
                    )
                    db.session.add(topic)
            
            # Biology Year 13 topics
            for topic_group in curriculum_data['Biology Year 13']['Topics']:
                module_name = topic_group['Name'].replace(' ', '')  # e.g., "Module5" 
                topic_key = f"{module_name}_BY13"
                parent_topic = Topic(
                    title=topic_group['Title'],
                    content=topic_group['Description'],
                    subject_id=subjects['Biology Year 13'].id,
                    module_name=topic_group['Name'] + ': ' + topic_group['Title'],
                    is_subtopic=False
                )
                db.session.add(parent_topic)
                db.session.flush()  # Get ID before committing
                main_topics[topic_key] = parent_topic.id
                
                for subtopic in topic_group['Subtopics']:
                    topic = Topic(
                        title=subtopic['Title'],
                        content=subtopic['Description'],
                        subject_id=subjects['Biology Year 13'].id,
                        module_name=topic_group['Name'] + ': ' + topic_group['Title'],
                        parent_topic_id=parent_topic.id,
                        is_subtopic=True
                    )
                    db.session.add(topic)
            
            # Chemistry topics
            for topic_group in curriculum_data['Chemistry']['Topics']:
                module_name = topic_group['Name'].replace(' ', '')  # e.g., "Module1"
                topic_key = f"{module_name}_CHEM"
                parent_topic = Topic(
                    title=topic_group['Title'],
                    content=topic_group['Description'],
                    subject_id=subjects['Chemistry'].id,
                    module_name=topic_group['Name'] + ': ' + topic_group['Title'],
                    is_subtopic=False
                )
                db.session.add(parent_topic)
                db.session.flush()  # Get ID before committing
                main_topics[topic_key] = parent_topic.id
                
                for subtopic in topic_group['Subtopics']:
                    topic = Topic(
                        title=subtopic['Title'],
                        content=subtopic['Description'],
                        subject_id=subjects['Chemistry'].id,
                        module_name=topic_group['Name'] + ': ' + topic_group['Title'],
                        parent_topic_id=parent_topic.id,
                        is_subtopic=True
                    )
                    db.session.add(topic)
            
            # Psychology topics
            for topic_group in curriculum_data['Psychology']['Topics']:
                paper_name = topic_group['Name'].lower()  # e.g., "paper1"
                topic_key = f"{paper_name}_PSYCH"
                parent_topic = Topic(
                    title=topic_group['Title'],
                    content=topic_group['Description'],
                    subject_id=subjects['Psychology'].id,
                    module_name=topic_group['Name'] + ': ' + topic_group['Title'],
                    is_subtopic=False
                )
                db.session.add(parent_topic)
                db.session.flush()  # Get ID before committing
                main_topics[topic_key] = parent_topic.id
                
                for subtopic in topic_group['Subtopics']:
                    # Handle content field which might be a list or a string
                    content = subtopic.get('Content', [])
                    content_str = '\n'.join(content) if isinstance(content, list) else subtopic['Description']
                    
                    topic = Topic(
                        title=subtopic['Title'],
                        content=content_str,
                        subject_id=subjects['Psychology'].id,
                        module_name=topic_group['Name'] + ': ' + topic_group['Title'],
                        parent_topic_id=parent_topic.id,
                        is_subtopic=True
                    )
                    db.session.add(topic)
            
            db.session.commit()
            print("Database initialized with curriculum data!")
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error initializing topics: {str(e)}")
            raise
            
    except Exception as e:
        logging.error(f"Error in init_db: {str(e)}")
        raise

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        init_db()