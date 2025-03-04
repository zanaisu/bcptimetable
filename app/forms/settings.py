from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class SettingsForm(FlaskForm):
    study_hours = FloatField('Study Hours Per Day', validators=[
        DataRequired(), NumberRange(min=0.5, max=12)
    ])
    weekend_points = IntegerField('Weekend Points Goal', validators=[
        DataRequired(), NumberRange(min=5, max=100)
    ])
    uplearn_biology = BooleanField('Use UpLearn for Biology')
    uplearn_chemistry = BooleanField('Use UpLearn for Chemistry')
    dark_mode = BooleanField('Dark Mode')
    submit = SubmitField('Save Settings')

class FirstLoginForm(FlaskForm):
    study_hours = FloatField('Study Hours Per Day', validators=[
        DataRequired(), NumberRange(min=0.5, max=12)
    ], default=4.0)
    weekend_points = IntegerField('Weekend Points Goal', validators=[
        DataRequired(), NumberRange(min=5, max=100)
    ], default=30)
    uplearn_biology = BooleanField('Use UpLearn for Biology')
    uplearn_chemistry = BooleanField('Use UpLearn for Chemistry')
    submit = SubmitField('Save Preferences')
    
    # Note: Topic confidence fields are handled via JavaScript and processed in routes/main.py