from the_idea import db
''' this is the table for the users in the database'''
class users(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

'''this is the table for the projects in the database'''
class projects(db.Model):
    project_id = db.Column(db.String(20), primary_key=True)
    difficulty_level = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(80))
    description = db.Column(db.String(120))
    category = db.relationship('categories', backref='projects', lazy=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# This is the table for the categories of projects
class categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    projects = db.relationship('projects', backref='categories', lazy=True)

# This is the association table for the many-to-many relationship between users and projects
class userProjects(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    
# This line creates the tables in the database  
create = db.create_all()