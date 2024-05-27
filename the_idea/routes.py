from the_idea import app, db
from the_idea.models import Users, Projects, Categories
from the_idea.forms import RegistrationForm, LoginForm, ProjectForm, CategoryForm, SearchForm
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
        category_id  = Categories.query.filter_by(category_name = form.category.data).first().category_id
        project = Projects(project_id = project_id, title = form.title.data, difficulty_level = form.difficulty_level.data, description = form.description.data, category = form.category.data, category_id=category_id, user_id = current_user.id)
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
        'updated_at': project.updated_at,
        'author': user.username
    } for user in ideas for project in user.projects
    ]
    
    try:
        random_idea = random.choice(projects)
        category = Categories.query.filter_by(category_id = random_idea['category_id']).first()
        return render_template('random_idea.html', random_idea = random_idea, category=category.category_name, title = 'Random Idea')
    except IndexError:
        random_idea = [{'project_id':None,
        'title': None,
        'difficulty_level': None,
        'description': 'No ideas available',
        'category_id': None,
        'user_id': None,
        }]
        return render_template('random_idea.html', title = 'Random Idea', random_idea = random_idea)

@app.route('/delete_project/<project_id>', methods = ['GET'])
@login_required
def delete_project(project_id):
    project = Projects.query.filter_by(project_id = project_id).first()
    db.session.delete(project)
    db.session.commit()
    flash('Project has been deleted successfully', 'success')
    return redirect(url_for('account'))

@app.route('/edit_project/<project_id>', methods = ['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Projects.query.filter_by(project_id = project_id).first()
    form = ProjectForm()
    if form.validate_on_submit():
        project.title = form.title.data
        project.difficulty_level = form.difficulty_level.data
        project.description = form.description.data
        db.session.commit()
        flash('Project has been updated successfully', 'success')
        return redirect(url_for('account'))
    form.title.data = project.title
    form.difficulty_level.data = project.difficulty_level
    form.description.data = project.description
    return render_template('projects.html', form = form, title = 'Edit Project')

# @app.route('/all_ideas', methods = ['GET'])
# def all_ideas():
#     projects = Projects.query.all()
#     categories = Categories.query.all()
#     return render_template('all_ideas.html', projects = projects, categories=categories, title = 'All Ideas')


@app.route('/search', methods = ['GET', 'POST'])
def all_ideas():
    projects = Projects.query.all()
    categories = Categories.query.all()
    form = SearchForm()
    if form.validate_on_submit():
        search = form.search_bar.data
        category_filter = form.category_filter.data
        difficulty_filter = form.difficulty_filter.data
        if category_filter == '' and difficulty_filter == '':
            projects = Projects.query.filter(Projects.title.contains(search))
        elif category_filter == '' and difficulty_filter != '':
            projects = Projects.query.filter(Projects.title.contains(search), Projects.difficulty_level == difficulty_filter)
        elif category_filter != '' and difficulty_filter == '':
            projects = Projects.query.filter(Projects.title.contains(search), Projects.category_id == category_filter)
        else:
            projects = Projects.query.filter(Projects.title.contains(search), Projects.category_id == category_filter, Projects.difficulty_level == difficulty_filter)
        return render_template('all_ideas.html', projects = projects, form = form, categories=categories, title = 'All Ideas')
    return render_template('all_ideas.html', projects = projects, form = form, categories=categories, title = 'All Ideas')    


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
    category_data = []
    for category in categories:
        category_info =  {
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
        category_data.append(category_info)
    return jsonify(category_data)
