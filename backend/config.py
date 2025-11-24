import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:chuntian2025@10.40.20.131:3306/blog_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
