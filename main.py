import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

database_name='polaris.db'
debug_mode = os.getenv("DEBUG_MODE", "True") == "False"                                             # Get the DEBUG_MODE environment variable. Default is True

persistent_path = os.getenv("PERSISTENT_STORAGE_DIR", os.path.dirname(os.path.realpath(__file__)))  # Get the path to the persistent storage directory
db_path = os.path.join(persistent_path, database_name)                                              # Define the path to the database file

app = Flask(__name__)                                                                               # Create a Flask app object
app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{db_path}'                                      # Set the URI for the database
app.config["SQLALCHEMY_ECHO"] = debug_mode                                                          # Enable SQLAlchemy logging. True for debugging
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False                                                # Disable tracking modifications. Can be left as False Advance use only

from routes.views import app as app_route                                                           # Import the app_routes Blueprint object from views.py after the db object is created
from models import db                                                                               

app.register_blueprint(app_route)                                                                   # Register the app_routes Blueprint object with the Flask app
db.init_app(app)                                                                                    # Initialize the SQLAlchemy object with the Flask app

with app.app_context():
    db.create_all()                                                                                 # Create the tables in the database                                              
    
if __name__ == "__main__":
    app.run(debug=True)                                                                             # Start the Flask app with debugging enabled so updates are automatically applied                      