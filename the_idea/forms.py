from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField, BooleanField, SelectField, TextAreaField, DateField, TimeField)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    confirm_password = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    difficulty_level = SelectField('Difficulty Level', choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Project')