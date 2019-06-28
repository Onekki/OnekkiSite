# coding: utf-8
from app import db
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


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


class BlogComment(db.Model):
    __tablename__ = 'blog_comment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    content = db.Column(db.Text)
    time = db.Column(db.DateTime)
    article_id = db.Column(db.ForeignKey('blog_article.id'), index=True)

    article = db.relationship('BlogArticle', primaryjoin='BlogComment.article_id == BlogArticle.id', backref='blog_comments')


class BlogTag(db.Model):
    __tablename__ = 'blog_tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    article_id = db.Column(db.ForeignKey('blog_tag.id'), index=True)

    article = db.relationship('BlogTag', remote_side=[id], primaryjoin='BlogTag.article_id == BlogTag.id', backref='blog_tags')


class BlogUser(db.Model):
    __tablename__ = 'blog_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
