import os
from flask import Flask
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed
from sqlalchemy import event

from config import configs
# from app.database.models import BlogReminder
from app.plugins import *
from app.plugins.circle_plugins import admin, api
from app.tasks import *
from app.controller.admin import *
from app.controller.api import *


# 创建app
def create_app(config_name):
    """创建app的方法"""
    # 生成Flask对象
    app = Flask(__name__)

# 导入配置
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)

# 各个模块注册
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    principal.init_app(app)
    celery.init_app(app)
    cache.init_app(app)
    admin.init_app(app)
    api.init_app(app)

    # event.listen(BlogReminder, 'after_insert', on_reminder_save)
    
# 权限验证
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

# 注册蓝图
    from app.controller.site import site
    # from app.admin import admin
    from app.controller.blog import blog

    # app.register_blueprint(admin, url_prefix = '/admin')
    app.register_blueprint(site, url_prefix = '/')
    app.register_blueprint(blog, url_prefix = '/blog')

# 放回Flask对象app
    return app
