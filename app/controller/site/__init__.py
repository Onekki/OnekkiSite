from flask import Blueprint

from config import TEMPLATES_DIR, STATIC_DIR

# 创建一个蓝图对象，设置别名，模板文件地址，静态文件地址
site = Blueprint('site', __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR)

# 这里导入是为了在解释时，蓝图能加载到views文件中的路由数据
from app.controller.site import views