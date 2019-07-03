# coding: utf-8
from app import db


class BlogUser(db.Model):
    __tablename__ = 'blog_user'
    __table_args__ = {'schema': 'onekki_site'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))


    # 自定义
    def __init__(self, name, password):
        self.name = name
        self.password = self.set_password(password)
    
    def set_password(self, password):
        return bcrypt.generate_password_hash(password)
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)