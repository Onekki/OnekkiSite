from flask import Flask
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed
from sqlalchemy import event
# 配置文件
from config import configs
# 插件
from app.plugins import login_manager, bcrypt, db, principal, celery, cache, admin
# 模型
from app.database.models import *
# admin
from app.controller.admin.views import CustomView, CustomModelView

from app.tasks import on_reminder_save

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
    principal.init_app(app)
    celery.init_app(app)
    cache.init_app(app)
    admin.init_app(app)
    admin.add_view(CustomView(name='Custom'))

    model_list = [BlogArticle, BlogComment, BlogReminder, BlogRole, BlogTag, BlogUser]
    for model in model_list:
        admin.add_view(
            CustomModelView(model, db.session, category='Models')
        )

    event.listen(BlogReminder, 'after_insert', on_reminder_save)
    
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
    app.register_blueprint(site, url_prefix = '/site')
    app.register_blueprint(blog, url_prefix = '/blog')

    # 放回Flask对象app
    return app
