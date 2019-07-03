from flask import Flask
# 配置文件引入
from config import configs

from app.plugin import login_manager, bcrypt, db

def create_app(config_name):
    """创建app的方法"""
    # 生成Flask对象
    app = Flask(__name__)

    # 导入配置
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)
    # 用SQLAlchemy初始化app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    # 在这还可以配置其他模块，如socketio

    # 放回Flask对象app
    return app
