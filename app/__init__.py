from flask import Flask
# mysql引入
from flask_sqlalchemy import SQLAlchemy
# 配置文件引入
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy()

def create_app():
    """创建app的方法"""
    # 生成Flask对象
    app = Flask(__name__)
    # 配置app的mysql
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    # 用SQLAlchemy初始化app
    db.init_app(app=app)
    
    # 在这还可以配置其他模块，如socketio

    # 放回Flask对象app
    return app
