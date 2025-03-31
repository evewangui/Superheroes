import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///heroes.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True  # Enables debug mode (disable in production)
