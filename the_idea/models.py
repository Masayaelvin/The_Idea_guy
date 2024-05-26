from the_idea import db
from the_idea import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

# This is the table for the users in the database
class Users(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship to projects
    projects = db.relationship('Projects', backref='author', lazy=True)

    def __repr__(self):
        return f'<Users id={self.id} username={self.username} email={self.email}>'

# This is the table for the projects in the database
class Projects(db.Model):
    project_id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    difficulty_level = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    user_id = db.Column(db.String(20), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Projects project_id={self.project_id} title={self.title}>'

# This is the table for the categories of projects
class Categories(db.Model):
    category_id = db.Column(db.String(20), primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Categories category_id={self.category_id} category_name={self.category_name}>'

# This line creates the tables in the database
# db.drop_all()
# db.create_all()
