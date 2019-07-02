# coding: utf-8
from app import db
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def dump_datetime(value):
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

class BlogArticle(db.Model):
    __tablename__ = 'blog_article'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45))
    content = db.Column(db.Text)
    publish_time = db.Column(db.DateTime)
    user_id = db.Column(db.ForeignKey('blog_user.id'), index=True)
    tag_id = db.Column(db.ForeignKey('blog_tag.id'), index=True)

    tag = db.relationship('BlogTag', primaryjoin='BlogArticle.tag_id == BlogTag.id', backref='blog_articles')
    user = db.relationship('BlogUser', primaryjoin='BlogArticle.user_id == BlogUser.id', backref='blog_articles')
    
    def __repr__(self):
        return self.title
        
    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "publish_time": dump_datetime(self.publish_time),
            "user_id": self.user_id,
            "tag_id": self.tag_id
        } 

class BlogComment(db.Model):
    __tablename__ = 'blog_comment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    content = db.Column(db.Text)
    time = db.Column(db.DateTime)
    article_id = db.Column(db.ForeignKey('blog_article.id'), index=True)

    article = db.relationship('BlogArticle', primaryjoin='BlogComment.article_id == BlogArticle.id', backref='blog_comments')

    def __repr__(self):
        return self.name

class BlogTag(db.Model):
    __tablename__ = 'blog_tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
   
    def __repr__(self):
        return self.name

class BlogUser(db.Model):
    __tablename__ = 'blog_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, name, password):
        self.name = name
        self.password = self.set_password(password)

    def __repr__(self):
        return self.name
    
    def set_password(self, password):
        return bcrypt.generate_password_hash(password)
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)