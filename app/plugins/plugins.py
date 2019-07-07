# 数据库
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


# 加密
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()


# 登录信息
from flask_login import LoginManager
login_manager = LoginManager()

login_manager.login_view = "blog.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"

@login_manager.user_loader
def user_loader(id):
    from app.database.models import BlogUser
    return BlogUser.query.filter_by(id=id).first()

# 角色权限
from flask_principal import Principal, Permission, RoleNeed
principal = Principal()

permission_admin = Permission(RoleNeed('admin'))
permission_poster = Permission(RoleNeed('poster'))
permission_default = Permission(RoleNeed('default'))


# 消息队列、异步任务
from flask_celery import Celery
celery = Celery()

# 邮件
from flask_mail import Mail
mail = Mail()


# 缓存
from flask_cache import Cache
cache = Cache()

