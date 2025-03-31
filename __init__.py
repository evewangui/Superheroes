from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load settings from config.py

    db.init_app(app)
    Migrate(app, db)

    # Import models here so they are registered
    from .app.models import Hero, Power, HeroPower

    return app

