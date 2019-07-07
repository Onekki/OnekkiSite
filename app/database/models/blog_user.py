# coding: utf-8
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask_principal import current_app
from flask_login import AnonymousUserMixin
from app.plugins import db, bcrypt


class BlogUser(db.Model):
    __tablename__ = 'blog_user'
    __table_args__ = {'schema': 'onekki_site'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    articles = db.relationship('BlogArticle', backref='blog_user', lazy='dynamic')
    roles = db.relationship('BlogRole', secondary='onekki_site.blog_user_role', backref=db.backref('blog_users', lazy='dynamic'))

    # 自定义
    def __init__(self, name, password):
        self.name = name
        self.password = self.set_password(password)

        defalut = db.session.query('BlogRole').filter_by(name="default").one()
        self.roles.append(defalut)
    
    def __repr__(self):
        return "<BlogUser:`{}`>".format(self.name)
    
    def set_password(self, password):
        return bcrypt.generate_password_hash(password)
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True
    
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False
    
    def get_id(self):
        return self.id

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(
            current_app.config['SECRET_KEY']
        )
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        
        user = BlogUser.query.filter_by(id=data['id']).first()
        return user
