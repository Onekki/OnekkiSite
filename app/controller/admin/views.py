# 获取蓝图
# from app.admin import admin
# # 获取数据库模型对象和SQLAlchemy对象db，注意不可使用App模块中的db
# # from app.admin.models import *

# # 设置路由
# @admin.route('/')
# def index():
#     return 'admin首页'

from flask_admin import BaseView, expose


class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom.html')
    
    @expose('/second_page')
    def second_page(self):
        return self.render('admin/second_page.html')

from flask_admin.contrib.sqla import ModelView

class CustomModelView(ModelView):
    pass