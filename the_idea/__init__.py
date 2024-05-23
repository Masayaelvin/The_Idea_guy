from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['CKEDITOR_PKG_TYPE'] = 'full'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///the_idea_guy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
bcrypt =  Bcrypt(app)

ckeditor = CKEditor(app)
db = SQLAlchemy(app)

from the_idea import routes