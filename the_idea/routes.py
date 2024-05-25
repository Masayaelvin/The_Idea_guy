from the_idea import app, db
from the_idea.models import Users, Projects, Categories
from the_idea.forms import RegistrationForm, LoginForm, ProjectForm, CategoryForm
from flask import jsonify, render_template, redirect, url_for, flash, request
from the_idea import bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import uuid
import random

@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html', title = 'Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome {user.username}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash('Login failed, please check your email and password', 'danger')
    return render_template('login.html', form = form, title = 'Login')


@app.route('/register', methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    id = str(uuid.uuid4())
    form = RegistrationForm()
    if form.validate_on_submit():
        encrpted_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(id = id, username = form.username.data, email = form.email.data, password = encrpted_pwd)
        db.session.add(user)
        db.session.commit()
        flash (f'Account for {form.username.data} has been created successfully you can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form = form, title = 'Register')

@app.route('/account', methods = ['GET'])
@login_required
def account():
    projects = user_projects()
    my_projects = Projects.query.filter_by(user_id = current_user.id)
    length = len(my_projects.all())
    return render_template('account.html', projects = projects, my_projects = my_projects, title = 'Account', length = length)

@app.route('/create_project', methods = ['GET', 'POST'])
@login_required
def create_idea():  
    form = ProjectForm()
    if form.validate_on_submit():
        project_id = str(uuid.uuid4())
        project = Projects(project_id = project_id, title = form.title.data, difficulty_level = form.difficulty_level.data, description = form.description.data, category_id = form.category.data, user_id = current_user.id)
        db.session.add(project)
        db.session.commit()
        flash(f'your Project_idea {form.title.data} has been created successfully', 'success')
        return redirect(url_for('account'))
    return render_template('projects.html', form = form, title = 'Create Project')

@app.route('/create_category', methods = ['GET', 'POST'])
@login_required
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category_id = str(uuid.uuid4())
        category = Categories(category_id = category_id, category_name = form.category_name.data)
        db.session.add(category)
        db.session.commit()
        flash(f'Category {form.category_name.data} has been created successfully', 'success')
        return redirect(url_for('account'))
    return render_template('categories.html', form = form, title = 'Create Category')

@app.route('/logout', methods = ['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))



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
    
@app.route('/random_idea', methods = ['GET'])
def random_idea():
    ideas =  Users.query.all()
    projects = [{
        'project_id': project.project_id,
        'title': project.title,
        'difficulty_level': project.difficulty_level,
        'description': project.description,
        'category_id': project.category_id,
        'user_id': project.user_id,
        'created_at': project.created_at,
        'updated_at': project.updated_at
    } for user in ideas for project in user.projects
    ]

    random_idea = random.choice(projects)
    return render_template('random_idea.html', random_idea = random_idea, title = 'Random Idea')

@app.route('/user_projects', methods = ['GET'])
def user_projects():
    users = Users.query.all()
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
    return jsonify(users_data)
    

@app.route('/categories', methods = ['GET'])
def categories():
    categories = Categories.query.all()
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
           
    return jsonify(category_data)
