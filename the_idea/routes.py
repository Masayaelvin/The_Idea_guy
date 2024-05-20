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
def Projects():
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
    user_projects = Projects.query.filter_by(user_id = '1').all()
    return jsonify([{
        'project_id': project.project_id,
        'title': project.title,
        'difficulty_level': project.difficulty_level,
        'description': project.description,
        'category_id': project.category_id,
        'user_id': project.user_id,
        'created_at': project.created_at,
        'updated_at': project.updated_at
    } for project in user_projects])
    

@app.route('/categories', methods = ['GET'])
def categories(category):
    categories = Categories.query.all()
    for category in categories:
        return jsonify([{
            category : [{
                category.projects
            }]
        }])
