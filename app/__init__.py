from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Main application instance.
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("app.cfg")

# Extension objects.
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Expose some parts of the application to be easily imported.
from .models import db
from . import views
