# coding: utf-8
from app.plugins import db

class BlogComment(db.Model):
    __tablename__ = 'blog_comment'
    __table_args__ = {'schema': 'onekki_site'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    content = db.Column(db.Text)
    time = db.Column(db.DateTime)
    article_id = db.Column(db.ForeignKey('onekki_site.blog_article.id'), index=True)

    article = db.relationship('BlogArticle', primaryjoin='BlogComment.article_id == BlogArticle.id', backref='blog_comments')
