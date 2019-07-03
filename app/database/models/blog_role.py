# coding: utf-8
from app import db


class BlogRole(db.Model):
    __tablename__ = 'blog_role'
    __table_args__ = {'schema': 'onekki_site'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))

    # users = db.relationship('BlogUser', secondary='onekki_site.blog_user_role', backref='blog_roles')
