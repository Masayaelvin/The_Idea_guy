from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware
from the_idea.models import Users, Projects, Categories  
import random

SQLALCHEMY_DATABASE_URL = "sqlite:///./instance/the_idea_guy.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI()

# Allow CORS for the frontend (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''this is the code for the random_project endpoint it returns a random project from the database'''
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
    
'''this is the code for the users endpoint it returns all the users in the database'''
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
    
    
'''this is the code for the projects endpoint it returns all the projects in the database'''
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


'''this is the code for the user_projects endpoint it returns all the users and the projects they have created'''
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

'''this is the code for the categories endpoint it returns all the categories and the projects in each category'''
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


'''this is the code for the difficulty endpoint  it
gets the difficulty level and returns the projects in that difficulty level'''
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
    
'''this is the code for the category endpoint  it 
gets the category name and returns the projects in that category'''
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



# Check if this resolves the issue:
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "Hello": "Welcome to 'The Idea Guy'",
        "endpoints": {
            "/random_project": {
                "method": "GET",
                "description": "Returns a random project from the database. If no projects are found, it raises a 404 error."
            },
            "/users": {
                "method": "GET",
                "description": "Retrieves and returns a list of all users in the database, including their ID, username, email, and timestamps for creation and updates."
            },
            "/projects": {
                "method": "GET",
                "description": "Retrieves and returns a list of all projects in the database, including project details such as ID, title, difficulty level, description, category ID, user ID, and timestamps for creation and updates."
            },
            "/user_projects": {
                "method": "GET",
                "description": "Returns a list of all users along with the projects they have created. Each user's information includes their ID, username, email, and a list of their projects with project details."
            },
            "/categories": {
                "method": "GET",
                "description": "Retrieves and returns a list of all categories along with the projects within each category. Each category's information includes its ID, name, and a list of projects with project details."
            },
            "/filter/{difficulty}": {
                "method": "GET",
                "description": "Filters and returns projects based on the specified difficulty level. If no projects are found for the given difficulty, it raises a 404 error."
            },
            "/category/{category}": {
                "method": "GET",
                "description": "Retrieves and returns projects within a specified category. If the category is not found, it raises a 404 error. Each category's information includes its ID, name, and a list of projects with project details."
            },
            "/": {
                "method": "GET",
                "description": "A root endpoint that returns a welcome message along with explanations of all other endpoints."
            }
        }
    }


