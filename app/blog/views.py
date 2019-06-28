# 获取蓝图
from app.blog import blog
# 获取数据库模型对象和SQLAlchemy对象db，注意不可使用App模块中的db
from app.blog.models import *

# 设置路由
@blog.route('/')
def index():
    return 'blog首页'