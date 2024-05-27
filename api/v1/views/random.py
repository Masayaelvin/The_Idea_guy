from api.v1.app import app
from the_idea.models import Users, Projects, Categories
import random
from flask import jsonify
from the_idea import db
'''the api routes for the project'''

@app.route('/random_project', methods = ['GET'])
def random_project():
    projects = Projects.query.all()
    random_project = random.choice(projects)
    return jsonify({
        'project_id': random_project.project_id,
        'title': random_project.title,
        'difficulty_level': random_project.difficulty_level,
        'description': random_project.description,
        'category_id': random_project.category_id,
        'user_id': random_project.user_id,
        'created_at': random_project.created_at,
        'updated_at': random_project.updated_at
    })

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

    
'''filter project by difficulty level'''
    
@app.route('/filter/<difficulty>', methods = ['GET'])
def filter_project(difficulty):
    projects = Projects.query.filter_by(difficulty_level = difficulty).all()
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

'''filter project by category'''
@app.route('/category/<category>', methods = ['GET'])
def category_project(category):
    category = Categories.query.filter_by(category_name = category).first()
    return jsonify({
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
    })
