from the_idea import app, db
from the_idea.models import Users, Projects, Categories
from flask import jsonify

@app.route('/', methods = ['GET'])
def home():
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
