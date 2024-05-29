from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./the_idea_guy.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


app = FastAPI()
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from the_idea.models import Users, Projects, Categories  # Import your models here
from database import get_db
import random

app = FastAPI()

@app.get("/random_project")
def random_project(db: Session = Depends(get_db)):
    projects = db.query(Projects).all()
    if not projects:
        raise HTTPException(status_code=404, detail="No projects found")
    random_project = random.choice(projects)
    return {
        'project_id': random_project.project_id,
        'title': random_project.title,
        'difficulty_level': random_project.difficulty_level,
        'description': random_project.description,
        'category_id': random_project.category_id,
        'user_id': random_project.user_id,
        'created_at': random_project.created_at,
        'updated_at': random_project.updated_at
    }

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at,
        'updated_at': user.updated_at
    } for user in users]

@app.get("/projects")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Projects).all()
    return [{
        'project_id': project.project_id,
        'title': project.title,
        'difficulty_level': project.difficulty_level,
        'description': project.description,
        'category_id': project.category_id,
        'user_id': project.user_id,
        'created_at': project.created_at,
        'updated_at': project.updated_at
    } for project in projects]

@app.get("/user_projects")
def user_projects(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    user_projects = []
    for user in users:
        user_data = {
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
        user_projects.append(user_data)
    return user_projects

@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Categories).all()
    category_data = []
    for category in categories:
        category_info = {
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
    return category_data

@app.get("/filter/{difficulty}")
def filter_project(difficulty: str, db: Session = Depends(get_db)):
    projects = db.query(Projects).filter_by(difficulty_level=difficulty).all()
    if not projects:
        raise HTTPException(status_code=404, detail="No projects found for the specified difficulty level")
    return [{
        'project_id': project.project_id,
        'title': project.title,
        'difficulty_level': project.difficulty_level,
        'description': project.description,
        'category_id': project.category_id,
        'user_id': project.user_id,
        'created_at': project.created_at,
        'updated_at': project.updated_at
    } for project in projects]

@app.get("/category/{category}")
def category_project(category: str, db: Session = Depends(get_db)):
    category = db.query(Categories).filter_by(category_name=category).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {
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

