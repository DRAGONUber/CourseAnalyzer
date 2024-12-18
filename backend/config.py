import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/course_analyzer')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
