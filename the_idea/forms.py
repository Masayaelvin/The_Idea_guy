from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField, BooleanField, SelectField, TextAreaField, DateField, TimeField)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError
from flask_ckeditor import CKEditorField
from the_idea.models import Categories

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    confirm_password = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ProjectForm(FlaskForm):
    category = SelectField('Category', choices=[(Categories.category_id, Categories.category_name) for category in Categories.query.all()], validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    difficulty_level = SelectField('Difficulty Level', choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], validators=[DataRequired()])
    description = CKEditorField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Project')

class CategoryForm(FlaskForm):
    category_name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Create Category')