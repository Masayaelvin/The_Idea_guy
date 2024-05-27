from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField, BooleanField, SelectField, TextAreaField, DateField, PasswordField)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError
from flask_ckeditor import CKEditorField
from the_idea.models import Categories
from the_idea.models import Users

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
        
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ProjectForm(FlaskForm):
    choices = [(category.category_name, category.category_name) for category in Categories.query.all()]
    category = SelectField('Category', choices=choices, validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    difficulty_level = SelectField('Difficulty Level', choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], validators=[DataRequired()])
    description = CKEditorField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Idea')

class CategoryForm(FlaskForm):
    category_name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Create Category')
    
class SearchForm(FlaskForm):
    search_bar = StringField('Search')
    category_filter = SelectField('Category', choices=[('All Categories','All Categories')] + [(category.category_id, category.category_name) for category in Categories.query.all()], validators=[DataRequired()])
    difficulty_filter = SelectField('Difficulty Level', choices=[('All Difficulty Levels','All Difficulty Levels'), ('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], validators=[DataRequired()])
    submit = SubmitField('Search')