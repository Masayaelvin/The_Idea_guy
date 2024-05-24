from the_idea import app, db
from the_idea.models import Users, Projects, Categories
from the_idea.forms import RegistrationForm, LoginForm, ProjectForm, CategoryForm
from flask import jsonify, render_template, redirect, url_for, flash
from the_idea import bcrypt
import uuid


@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash(f'Welcome {user.username}', 'success')
            return redirect(url_for('account'))
        else:
            flash('Login failed, please check your email and password', 'danger')
    return render_template('login.html', form = form)


@app.route('/register', methods = ['GET','POST'])
def register():
    id = str(uuid.uuid4())
    form = RegistrationForm()
    if form.validate_on_submit():
        encrpted_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(id = id, username = form.username.data, email = form.email.data, password = encrpted_pwd)
        db.session.add(user)
        db.session.commit()
        flash (f'Account for {form.username.data} has been created successfully', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form = form)

@app.route('/account', methods = ['GET'])
def account():
    return render_template('account.html')

@app.route('/create_project', methods = ['GET', 'POST'])
def create_idea():
    form = ProjectForm()
    if form.validate_on_submit():
        project_id = str(uuid.uuid4())
        project = Projects(project_id = project_id, title = form.title.data, difficulty_level = form.difficulty_level.data, description = form.description.data, category_id = form.category.data, user_id = '1')
        db.session.add(project)
        db.session.commit()
        flash(f'your Project_idea {form.title.data} has been created successfully', 'success')
        return redirect(url_for('account'))
    return render_template('projects.html', form = form)

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
    ideas = all_Projects()
    pass

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
        user_projects.append(users_data)
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
