# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class BlogArticle(db.Model):
    __tablename__ = 'blog_article'
    __table_args__ = {'schema': 'onekki_site'}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45))
    content = db.Column(db.Text)
    publish_time = db.Column(db.DateTime)
    user_id = db.Column(db.ForeignKey('onekki_site.blog_user.id'), index=True)

    user = db.relationship('BlogUser', primaryjoin='BlogArticle.user_id == BlogUser.id', backref='blog_articles')
    tags = db.relationship('BlogTag', secondary='onekki_site.blog_article_tag', backref='blog_articles')


t_blog_article_tag = db.Table(
    'blog_article_tag',
    db.Column('article_id', db.ForeignKey('onekki_site.blog_article.id'), primary_key=True, nullable=False),
    db.Column('tag_id', db.ForeignKey('onekki_site.blog_tag.id'), primary_key=True, nullable=False, index=True),
    schema='onekki_site'
)


class BlogComment(db.Model):
    __tablename__ = 'blog_comment'
    __table_args__ = {'schema': 'onekki_site'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    content = db.Column(db.Text)
    time = db.Column(db.DateTime)
    article_id = db.Column(db.ForeignKey('onekki_site.blog_article.id'), index=True)

    article = db.relationship('BlogArticle', primaryjoin='BlogComment.article_id == BlogArticle.id', backref='blog_comments')


class BlogRole(db.Model):
    __tablename__ = 'blog_role'
    __table_args__ = {'schema': 'onekki_site'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))

    users = db.relationship('BlogUser', secondary='onekki_site.blog_user_role', backref='blog_roles')


class BlogTag(db.Model):
    __tablename__ = 'blog_tag'
    __table_args__ = {'schema': 'onekki_site'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class BlogUser(db.Model):
    __tablename__ = 'blog_user'
    __table_args__ = {'schema': 'onekki_site'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))


t_blog_user_role = db.Table(
    'blog_user_role',
    db.Column('user_id', db.ForeignKey('onekki_site.blog_user.id'), primary_key=True, nullable=False),
    db.Column('role_id', db.ForeignKey('onekki_site.blog_role.id'), primary_key=True, nullable=False, index=True),
    schema='onekki_site'
)
