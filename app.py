from flask import Flask, render_template
from flask_security import Security, login_required, SQLAlchemySessionUserDatastore
from database import db_session, init_db
from flask_mail import Mail
from models import User, Role

mail = Mail()
# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'bcrypt'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_POST_LOGIN_VIEW'] = '/dashboard'
app.config['SECURITY_POST_REGISTER_VIEW'] = '/dashboard'
mail.init_app(app)

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


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run()