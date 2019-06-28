import os
from flask_script import Manager

from app import create_app
from app.site import site

# 创建app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# 注册site的蓝图
app.register_blueprint(site, url_prefix = '/site')

# 通过app创建manager对象
manager = Manager(app)

if __name__ == '__main__':
    # 运行服务器
    manager.run()