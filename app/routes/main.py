from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.task import Task
from app.models.subject import Subject
from app.models.topic import Topic, TopicConfidence, SubtopicConfidence
from app.forms.settings import SettingsForm, FirstLoginForm
from datetime import datetime, timedelta
import json
import os
import random

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    # If this is the user's first login, redirect to setup
    if current_user.is_first_login:
        return redirect(url_for('main.first_login_setup'))
    
    # Get today's date
    today = datetime.utcnow().date()
    
    # Determine if it's weekend (Friday, Saturday, Sunday)
    is_weekend = today.weekday() >= 4  # 4 is Friday, 5 is Saturday, 6 is Sunday
    
    # Get tasks for today
    today_tasks = Task.query.filter_by(
        user_id=current_user.id,
        date_assigned=today
    ).all()
    
    # If no tasks for today, generate new ones
    if not today_tasks:
        today_tasks = generate_daily_tasks(current_user)
    
    return render_template(
        'main/index.html',
        tasks=today_tasks,
        is_weekend=is_weekend,
        today=today
    )

@main.route('/calendar')
@login_required
def calendar():
    # Get all tasks for the current user
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    # Get exam dates
    exam_dates = {
        'Biology': ['2025-05-15', '2025-05-22', '2025-06-10'],
        'Chemistry': ['2025-05-20', '2025-05-28', '2025-06-12'],
        'Psychology': ['2025-05-14', '2025-05-21', '2025-06-04']
    }
    
    return render_template(
        'main/calendar.html',
        tasks=tasks,
        exam_dates=exam_dates
    )

@main.route('/curriculum')
@login_required
def curriculum():
    # Get all subjects
    subjects = Subject.query.all()
    
    # Load curriculum data 
    curriculum_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'curriculum.json')
    with open(curriculum_path, 'r') as f:
        curriculum_data = json.load(f)
    
    # Get user's topic confidences
    topic_confidences = {}
    topic_confs = TopicConfidence.query.filter_by(user_id=current_user.id).all()
    for tc in topic_confs:
        topic_confidences[tc.topic_key] = tc.confidence_level
    
    # Get user's subtopic confidences
    subtopic_confidences = {}
    subtopic_confs = SubtopicConfidence.query.filter_by(user_id=current_user.id).all()
    for sc in subtopic_confs:
        subtopic_confidences[sc.subtopic_key] = sc.confidence_level
    
    return render_template(
        'main/curriculum.html',
        subjects=subjects,
        curriculum=curriculum_data,
        topic_confidences=topic_confidences,
        subtopic_confidences=subtopic_confidences
    )

@main.route('/progress')
@login_required
def progress():
    # Get all completed tasks
    completed_tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).all()
    
    # Get all skipped tasks
    skipped_tasks = Task.query.filter_by(
        user_id=current_user.id,
        skipped=True
    ).all()
    
    # Get topic confidences
    topic_confidences = current_user.topic_confidences.all()
    
    # Find weakest topics for each subject
    biology_topics = Topic.query.join(Subject).filter(Subject.name == 'Biology').all()
    chemistry_topics = Topic.query.join(Subject).filter(Subject.name == 'Chemistry').all()
    psychology_topics = Topic.query.join(Subject).filter(Subject.name == 'Psychology').all()
    
    # Calculate completion stats
    total_tasks = len(completed_tasks) + len(skipped_tasks)
    completion_rate = (len(completed_tasks) / total_tasks) * 100 if total_tasks > 0 else 0
    
    # Subject distribution stats
    subject_counts = {}
    for task in completed_tasks:
        subject_name = task.subject.name
        if subject_name in subject_counts:
            subject_counts[subject_name] += 1
        else:
            subject_counts[subject_name] = 1
    
    return render_template(
        'main/progress.html',
        completed_tasks=completed_tasks,
        skipped_tasks=skipped_tasks,
        topic_confidences=topic_confidences,
        completion_rate=completion_rate,
        subject_counts=subject_counts
    )

@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    
    if form.validate_on_submit():
        current_user.study_hours_per_day = form.study_hours.data
        current_user.weekend_points_goal = form.weekend_points.data
        current_user.uplearn_biology = form.uplearn_biology.data
        current_user.uplearn_chemistry = form.uplearn_chemistry.data
        current_user.dark_mode = form.dark_mode.data
        
        db.session.commit()
        flash('Settings updated successfully!')
        return redirect(url_for('main.settings'))
    
    # Populate form with current settings
    if request.method == 'GET':
        form.study_hours.data = current_user.study_hours_per_day
        form.weekend_points.data = current_user.weekend_points_goal
        form.uplearn_biology.data = current_user.uplearn_biology
        form.uplearn_chemistry.data = current_user.uplearn_chemistry
        form.dark_mode.data = current_user.dark_mode
    
    return render_template('main/settings.html', form=form)

@main.route('/first-login-setup', methods=['GET', 'POST'])
@login_required
def first_login_setup():
    if not current_user.is_first_login:
        return redirect(url_for('main.index'))
    
    form = FirstLoginForm()
    
    # Get all subjects
    subjects = Subject.query.all()
    
    if form.validate_on_submit():
        # Update user settings
        current_user.study_hours_per_day = form.study_hours.data
        current_user.weekend_points_goal = form.weekend_points.data
        current_user.uplearn_biology = form.uplearn_biology.data
        current_user.uplearn_chemistry = form.uplearn_chemistry.data
        
        # Mark first login as complete
        current_user.is_first_login = False
        
        # Process topic confidences from form data
        for key, value in request.form.items():
            if key.startswith('topic_'):
                try:
                    confidence = int(value)
                    if 1 <= confidence <= 5:
                        # This is a topic confidence
                        tc = TopicConfidence.query.filter_by(
                            user_id=current_user.id,
                            topic_key=key
                        ).first()
                        
                        if tc:
                            tc.confidence_level = confidence
                        else:
                            tc = TopicConfidence(
                                user_id=current_user.id,
                                topic_key=key,
                                confidence_level=confidence
                            )
                            db.session.add(tc)
                except ValueError:
                    # Skip malformed values
                    continue
        
        db.session.commit()
        flash('Thank you for setting up your preferences!')
        return redirect(url_for('main.index'))
    
    # Load curriculum data for displaying topics
    curriculum_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'curriculum.json')
    with open(curriculum_path, 'r') as f:
        curriculum_data = json.load(f)
    
    return render_template(
        'main/first_login_setup.html',
        form=form,
        subjects=subjects,
        curriculum=curriculum_data
    )

@main.route('/api/tasks/complete/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Ensure the task belongs to the current user
    if task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    task.mark_completed()
    
    # Update topic confidence
    if task.topic_id:
        # Get the topic to extract module and subject
        topic = Topic.query.get(task.topic_id)
        if topic and topic.module_name:
            # Extract module from module_name (e.g., "Module 1: Title" -> "Module1")
            parts = topic.module_name.split(':')
            if parts:
                module_name = parts[0].strip().replace(' ', '')
                
                # Determine subject code
                subject_code = ""
                if task.subject.name == "Biology Year 12":
                    subject_code = "BY12"
                elif task.subject.name == "Biology Year 13":
                    subject_code = "BY13"
                elif task.subject.name == "Chemistry":
                    subject_code = "CHEM"
                elif task.subject.name == "Psychology":
                    subject_code = "PSYCH"
                    
                topic_key = f"topic_{module_name}_{subject_code}"
                
                # Update topic confidence
                tc = TopicConfidence.query.filter_by(
                    user_id=current_user.id,
                    topic_key=topic_key
                ).first()
                
                if tc:
                    # Increase confidence (max 5)
                    tc.confidence_level = min(tc.confidence_level + 1, 5)
                else:
                    # Create new topic confidence if it doesn't exist
                    tc = TopicConfidence(
                        user_id=current_user.id,
                        topic_key=topic_key,
                        confidence_level=4  # Start at 4 when completing a task (default is 3)
                    )
                    db.session.add(tc)
    
    db.session.commit()
    return jsonify({'success': True})

@main.route('/api/tasks/skip/<int:task_id>', methods=['POST'])
@login_required
def skip_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Ensure the task belongs to the current user
    if task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    task.mark_skipped()
    
    # Update topic confidence
    if task.topic_id:
        # Get the topic to extract module and subject
        topic = Topic.query.get(task.topic_id)
        if topic and topic.module_name:
            # Extract module from module_name (e.g., "Module 1: Title" -> "Module1")
            parts = topic.module_name.split(':')
            if parts:
                module_name = parts[0].strip().replace(' ', '')
                
                # Determine subject code
                subject_code = ""
                if task.subject.name == "Biology Year 12":
                    subject_code = "BY12"
                elif task.subject.name == "Biology Year 13":
                    subject_code = "BY13"
                elif task.subject.name == "Chemistry":
                    subject_code = "CHEM"
                elif task.subject.name == "Psychology":
                    subject_code = "PSYCH"
                    
                topic_key = f"topic_{module_name}_{subject_code}"
                
                # Update topic confidence
                tc = TopicConfidence.query.filter_by(
                    user_id=current_user.id,
                    topic_key=topic_key
                ).first()
                
                if tc:
                    # Decrease confidence (min 1)
                    tc.confidence_level = max(tc.confidence_level - 1, 1)
                else:
                    # Create new topic confidence if it doesn't exist
                    tc = TopicConfidence(
                        user_id=current_user.id,
                        topic_key=topic_key,
                        confidence_level=2  # Start at 2 when skipping a task (default is 3)
                    )
                    db.session.add(tc)
    
    # Generate a new task to replace the skipped one
    new_task = generate_replacement_task(current_user, task.subject_id)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'new_task': {
            'id': new_task.id,
            'title': new_task.title,
            'description': new_task.description,
            'subject': new_task.subject.name,
            'duration': new_task.duration,
            'task_type': new_task.task_type
        }
    })

@main.route('/api/topic-confidence/<string:topic_id>', methods=['POST'])
@login_required
def update_topic_confidence(topic_id):
    data = request.get_json()
    confidence_level = data.get('confidence_level', 3)
    
    # Validate confidence level
    if not 1 <= confidence_level <= 5:
        return jsonify({'error': 'Invalid confidence level'}), 400
    
    # Get topic confidence or create if not exists
    tc = TopicConfidence.query.filter_by(
        user_id=current_user.id,
        topic_key=topic_id
    ).first()
    
    if tc:
        tc.confidence_level = confidence_level
    else:
        tc = TopicConfidence(
            user_id=current_user.id,
            topic_key=topic_id,
            confidence_level=confidence_level
        )
        db.session.add(tc)
    
    db.session.commit()
    return jsonify({'success': True})


@main.route('/api/subtopic-confidence/<string:subtopic_id>', methods=['POST'])
@login_required
def update_subtopic_confidence(subtopic_id):
    data = request.get_json()
    confidence_level = data.get('confidence_level', 3)
    
    # Validate confidence level
    if not 1 <= confidence_level <= 5:
        return jsonify({'error': 'Invalid confidence level'}), 400
    
    # Get subtopic confidence or create if not exists
    sc = SubtopicConfidence.query.filter_by(
        user_id=current_user.id,
        subtopic_key=subtopic_id
    ).first()
    
    if sc:
        sc.confidence_level = confidence_level
    else:
        sc = SubtopicConfidence(
            user_id=current_user.id,
            subtopic_key=subtopic_id,
            confidence_level=confidence_level
        )
        db.session.add(sc)
    
    # Extract topic_id from subtopic_id (e.g., "Module1_Cell_structure_BY12" -> "Module1_BY12")
    parts = subtopic_id.split('_')
    if len(parts) >= 2:  # At least has a prefix and suffix
        subject_code = parts[-1]  # Last part is subject code (e.g., BY12, CHEM, PSYCH)
        topic_prefix = parts[0]   # First part is topic module/paper (e.g., Module1, paper1)
        topic_id = f"topic_{topic_prefix}_{subject_code}"
        
        # Calculate new topic confidence based on all subtopics
        subtopic_confs = SubtopicConfidence.query.filter(
            SubtopicConfidence.user_id == current_user.id,
            SubtopicConfidence.subtopic_key.like(f"%_{subject_code}")
        ).all()
        
        # Group by topic prefix to calculate averages
        topic_totals = {}
        topic_counts = {}
        
        for sc in subtopic_confs:
            # Extract topic prefix from subtopic key
            key_parts = sc.subtopic_key.split('_')
            if len(key_parts) >= 2:
                t_prefix = key_parts[0]
                t_subject = key_parts[-1]
                t_key = f"{t_prefix}_{t_subject}"
                
                if t_key not in topic_totals:
                    topic_totals[t_key] = 0
                    topic_counts[t_key] = 0
                
                topic_totals[t_key] += sc.confidence_level
                topic_counts[t_key] += 1
        
        # Update topic confidence if we have data for this topic
        if topic_id in topic_totals and topic_counts[topic_id] > 0:
            avg_confidence = round(topic_totals[topic_id] / topic_counts[topic_id])
            
            # Update topic confidence
            tc = TopicConfidence.query.filter_by(
                user_id=current_user.id,
                topic_key=topic_id
            ).first()
            
            if tc:
                tc.confidence_level = avg_confidence
            else:
                tc = TopicConfidence(
                    user_id=current_user.id,
                    topic_key=topic_id,
                    confidence_level=avg_confidence
                )
                db.session.add(tc)
        
    db.session.commit()
    
    # Return success with updated topic confidence for UI update
    return jsonify({
        'success': True,
        'topic_id': topic_id,
        'topic_confidence': tc.confidence_level if 'tc' in locals() and tc else None
    })

@main.route('/api/update-dark-mode', methods=['POST'])
@login_required
def update_dark_mode():
    data = request.get_json()
    dark_mode = data.get('dark_mode', False)
    
    current_user.dark_mode = dark_mode
    db.session.commit()
    
    return jsonify({'success': True})

# Helper functions
def generate_daily_tasks(user):
    """Generate tasks for the day based on user preferences."""
    # Determine number of tasks based on study hours
    num_tasks = int(user.study_hours_per_day / 0.5)  # Assuming average task is 30 minutes
    
    # Ensure minimum of 2 and maximum of 4 tasks
    num_tasks = max(2, min(num_tasks, 4))
    
    # Get all subjects
    subjects = Subject.query.all()
    
    # Ensure tasks are distributed across subjects
    subject_distribution = distribute_subjects(subjects, num_tasks)
    
    tasks = []
    for subject_id, count in subject_distribution.items():
        for _ in range(count):
            new_task = generate_task_for_subject(user, subject_id)
            tasks.append(new_task)
    
    # Save tasks to database
    db.session.add_all(tasks)
    db.session.commit()
    
    return tasks

def generate_task_for_subject(user, subject_id):
    """Generate a single task for a specific subject."""
    subject = Subject.query.get(subject_id)
    
    # Get topics for this subject
    topics = Topic.query.filter_by(subject_id=subject_id).all()
    
    # Determine subject code based on subject name
    subject_code = ""
    if subject.name == "Biology Year 12":
        subject_code = "BY12"
    elif subject.name == "Biology Year 13":
        subject_code = "BY13"
    elif subject.name == "Chemistry":
        subject_code = "CHEM"
    elif subject.name == "Psychology":
        subject_code = "PSYCH"
        
    # Get all topic confidences for this user and this subject
    topic_confidences = TopicConfidence.query.filter(
        TopicConfidence.user_id == user.id,
        TopicConfidence.topic_key.like(f"%_{subject_code}")
    ).all()
    
    # Create weighted list of module/topic names
    weighted_topics = []
    
    # If no confidence data exists yet, use default distribution
    if not topic_confidences:
        for topic in topics:
            # Extract module name from topic.module_name (e.g., "Module 1: Title" -> "Module1")
            if topic.module_name:
                parts = topic.module_name.split(':')
                if parts:
                    module_name = parts[0].strip().replace(' ', '')
                    weighted_topics.extend([module_name] * 3)  # Default weight
    else:
        # Use confidence-based weighting
        for tc in topic_confidences:
            # Extract module/topic prefix from topic_key
            # e.g., "topic_Module1_BY12" -> "Module1"
            parts = tc.topic_key.split('_')
            if len(parts) >= 2:
                module_name = parts[1]
                
                # Lower confidence = higher weight (inverse scaling)
                weight = 6 - tc.confidence_level  # Confidence 1 => weight 5, Confidence 5 => weight 1
                
                # Add to weighted list
                weighted_topics.extend([module_name] * weight)
    
    # If weighted list is empty, add default topics
    if not weighted_topics:
        for topic in topics:
            weighted_topics.append(topic.module_name)
    
    # Randomly select a module/topic from the weighted list
    selected_module = random.choice(weighted_topics) if weighted_topics else None
    
    # Find a topic that matches this module
    if selected_module:
        matching_topics = [t for t in topics if selected_module in t.module_name.replace(' ', '')]
        selected_topic = random.choice(matching_topics) if matching_topics else random.choice(topics)
    else:
        selected_topic = random.choice(topics) if topics else None
    
    # Determine task type
    task_types = ['mind_map', 'past_paper', 'notes_review', 'practice_questions']
    
    # If UpLearn is enabled for this subject, only use UpLearn tasks
    if ((subject.name == "Biology Year 12" or subject.name == "Biology Year 13") and user.uplearn_biology) or \
       (subject.name == "Chemistry" and user.uplearn_chemistry):
        task_type = 'uplearn'
    else:
        task_type = random.choice(task_types)
    
    # Create task
    task = Task(
        user_id=user.id,
        subject_id=subject_id,
        topic_id=selected_topic.id if selected_topic else None,
        title=f"{task_type.replace('_', ' ').title()}: {selected_topic.title if selected_topic else subject.name}",
        description=f"Study {selected_topic.title if selected_topic else 'general topics'} in {subject.name}",
        task_type=task_type,
        duration=30,  # 30 minutes default
        points=1,
        date_assigned=datetime.utcnow().date()
    )
    
    return task

def generate_replacement_task(user, subject_id):
    """Generate a replacement task when a task is skipped."""
    new_task = generate_task_for_subject(user, subject_id)
    db.session.add(new_task)
    return new_task

def distribute_subjects(subjects, num_tasks):
    """Distribute tasks evenly across subjects."""
    # Simple distribution: round-robin
    result = {subject.id: 0 for subject in subjects}
    subject_ids = [subject.id for subject in subjects]
    
    for i in range(num_tasks):
        subject_id = subject_ids[i % len(subject_ids)]
        result[subject_id] += 1
    
    return result