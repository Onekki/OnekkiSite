from app.plugins import db

t_blog_article_tag = db.Table(
    'blog_article_tag',
    db.Column('article_id', db.ForeignKey('onekki_site.blog_article.id'), primary_key=True, nullable=False),
    db.Column('tag_id', db.ForeignKey('onekki_site.blog_tag.id'), primary_key=True, nullable=False, index=True),
    schema='onekki_site'
)

t_blog_user_role = db.Table(
    'blog_user_role',
    db.Column('user_id', db.ForeignKey('onekki_site.blog_user.id'), primary_key=True, nullable=False),
    db.Column('role_id', db.ForeignKey('onekki_site.blog_role.id'), primary_key=True, nullable=False, index=True),
    schema='onekki_site'
)