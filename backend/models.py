from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    
    articles = db.relationship('Article', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(256))
    
    articles = db.relationship('Article', backref='category', lazy='dynamic')

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    summary = db.Column(db.String(500))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.String(20), default='published') # published, draft, private
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    comments = db.relationship('Comment', backref='article', lazy='dynamic')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending') # pending, approved, rejected
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, index=True)
    value = db.Column(db.String(256))
    description = db.Column(db.String(256))
