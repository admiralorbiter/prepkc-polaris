from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


persistent_path = os.getenv("PERSISTENT_STORAGE_DIR", os.path.dirname(os.path.realpath(__file__)))

app = Flask(__name__)
db_path = os.path.join(persistent_path, "polaris.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{db_path}'
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.routes import views
from app import models

# db.init_app(app)
# migrate.init_app(app, db)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)