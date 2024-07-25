import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config  # Import the configuration class

# Initialize Flask application
app = Flask(__name__)

# Apply configuration from Config class
app.config.from_object(Config)

# Print the absolute path of the database file
db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
print(f"Database file will be created at: {db_path}")

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Import the User model and login_manager user_loader callback
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import views after initializing the app
from app import views

# Check if the database file exists after initialization
if os.path.exists(db_path):
    print(f"Database file exists at: {db_path}")
else:
    print(f"Database file was not created at: {db_path}")
