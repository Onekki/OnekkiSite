import os

# 项目绝对路径
BASE_DIR = os.getcwd()
# 模版文件路径
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
# 静态文件路径
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# 数据库URI
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@39.107.230.35:3306/onekki_site'

# 查询跟踪，不太需要，False，不占用额外的内存
SQLALCHEMY_TRACK_MODIFICATIONS = False
