from the_idea import app, db
from the_idea.models import Users, Projects, Categories, UserProjects

@app.route('/home')
def home():
    users = Users.query.all()
    return ', '.join([str(user.username) for user in users]) 