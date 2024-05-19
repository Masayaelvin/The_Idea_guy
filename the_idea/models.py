from the_idea import db

# This is the table for the users in the database
class Users(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship to user projects
    user_projects = db.relationship('UserProjects', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<Users id={self.id} username={self.username} email={self.email}>'

# This is the table for the projects in the database
class Projects(db.Model):
    project_id = db.Column(db.String(20), primary_key=True)
    difficulty_level = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(80))
    description = db.Column(db.String(120))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship to categories
    category = db.relationship('Categories', backref='projects', lazy=True)
    # Relationship to user projects
    project_users = db.relationship('UserProjects', backref='project', lazy=True)

# This is the table for the categories of projects
class Categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# This is the association table for the many-to-many relationship between users and projects
class UserProjects(db.Model):
    user_id = db.Column(db.String(20), db.ForeignKey('users.id'), primary_key=True)
    project_id = db.Column(db.String(20), db.ForeignKey('projects.project_id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())


# This line creates the tables in the database
# create = db.create_all()

    