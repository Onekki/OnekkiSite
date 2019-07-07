# coding: utf-8
from app.plugins import db

class BlogArticle(db.Model):
    __tablename__ = 'blog_article'
    __table_args__ = {'schema': 'onekki_site'}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45))
    content = db.Column(db.Text)
    publish_time = db.Column(db.DateTime)
    user_id = db.Column(db.ForeignKey('onekki_site.blog_user.id'), index=True)

    user = db.relationship('BlogUser', primaryjoin='BlogArticle.user_id == BlogUser.id', backref='blog_articles')

    comments = db.relationship('BlogComment', backref='blog_article', lazy='dynamic')
    tags = db.relationship('BlogTag', secondary='onekki_site.blog_article_tag', backref='blog_articles')

