# coding: utf-8
from app import db


class BlogTag(db.Model):
    __tablename__ = 'blog_tag'
    __table_args__ = {'schema': 'onekki_site'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))