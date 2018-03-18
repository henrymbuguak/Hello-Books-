from flask import Flask, render_template
from flask_security import Security, login_required, SQLAlchemySessionUserDatastore
from database import db_session, init_db
from models import User, Role


# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'

# Setup Flask-Security
use_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, use_datastore)

# Create a user for test with
# @app.before_first_request
# def create_user():
#     init_db()
#     use_datastore.create_user(username='henry', email='henrymbuguak@gmail.com', password='password')
#     db_session.commit()
#

# views
@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()