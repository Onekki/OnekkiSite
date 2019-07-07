import os
from app.plugins import db
from app.database.models import *
from app.controller.api import *
from app.controller.admin import *


# 后台管理
from flask_admin import Admin
admin = Admin()
# admin 添加view
admin.add_view(CustomView(name='Custom'))
model_list = [BlogComment, BlogReminder, BlogRole, BlogTag, BlogUser]
for model in model_list:
    admin.add_view(
        CustomModelView(model, db.session, category='Models')
    )
admin.add_view(ArticleView(BlogArticle, db.session, name='EditArticle'))

T_DIR = os.path.dirname(os.path.realpath(__file__))#获取项目根目录
T_DIR = os.path.dirname(T_DIR)
T_DIR = os.path.dirname(T_DIR)
path = os.path.join(T_DIR, "app/static")

admin.add_view(
    CustomFileView(path,
    '/static', 
    name='Static Files')
)


# restful api
from flask_restful import Api

api = Api()
api.add_resource(
    BlogArticleApi,
    '/api/article',
    '/api/article/<int:id>',
    endpoint='restful_api_blog_article'
)
api.add_resource(
    BlogAuthApi,
    '/api/auth',
    endpoint='restful_api_auth'
)