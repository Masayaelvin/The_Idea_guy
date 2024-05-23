from the_idea import app, db
from the_idea.models import Users, Projects, Categories
from the_idea.forms import RegistrationForm, LoginForm, ProjectForm, CategoryForm
from flask import jsonify, render_template, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import uuid


@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user and Bcrypt.check_password_hash(user.password, form.password.data):
            flash(f'Welcome {user.username}', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed, please check your email and password', 'danger')
    return render_template('login.html', form = form)


@app.route('/register', methods = ['GET','POST'])
def register():
    id = str(uuid.uuid4())
    form = RegistrationForm()
    if form.validate_on_submit():
        encrpted_pwd = Bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(id = id, username = form.username.data, email = form.email.data, password = encrpted_pwd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    flash (f'Account for {form.username.data} has been created successfully', 'success')
    return render_template('register.html', form = form)



'''the api routes for the project'''
@app.route('/users', methods = ['GET'])
def users():
    users = Users.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at,
        'updated_at': user.updated_at
    } for user in users])

@app.route('/projects', methods = ['GET'])    
def all_Projects():
    projects = Projects.query.all()
    return jsonify([{
        'project_id': project.project_id,
        'title': project.title,
        'difficulty_level': project.difficulty_level,
        'description': project.description,
        'category_id': project.category_id,
        'user_id': project.user_id,
        'created_at': project.created_at,
        'updated_at': project.updated_at
    } for project in projects])

@app.route('/user_projects', methods = ['GET'])
def user_projects():
    users = Users.query.all()
    user_projects = []
    for user in users:
        users_data = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'projects': [{
                    'project_id': project.project_id,
                    'title': project.title,
                    'difficulty_level': project.difficulty_level,
                    'description': project.description,
                    'created_at': project.created_at,
                    'updated_at': project.updated_at
                } for project in user.projects]
            }            
        ]
        user_projects.append(users_data)
    return jsonify(user_projects)
    

@app.route('/categories', methods = ['GET'])
def categories():
    categories = Categories.query.all()
    result = []
    for category in categories:
        category_data = {
            'category_id': category.category_id,
            'category_name': category.category_name,
            'projects': [{
                'project_id': project.project_id,
                'title': project.title,
                'difficulty_level': project.difficulty_level,
                'description': project.description,
                'created_at': project.created_at,
                'updated_at': project.updated_at
            } for project in category.projects]
        }
        result.append(category_data)
    
    return jsonify(result)
