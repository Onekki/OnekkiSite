# 获取蓝图
from app.site import site
# 获取数据库模型对象和SQLAlchemy对象db，注意不可使用app模块中的db
# from app.site.models import *

# 设置路由
@site.route('/')
def index():
    return 'site首页'