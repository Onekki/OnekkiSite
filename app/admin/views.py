# 获取蓝图
from app.admin import admin
# 获取数据库模型对象和SQLAlchemy对象db，注意不可使用App模块中的db
from app.admin.models import *

# 设置路由
@site.route('/')
def index():
    return 'admin首页'