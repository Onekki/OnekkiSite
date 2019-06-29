import os
from flask_script import Manager, Server

from app import create_app, db
from app.site import site
from app.blog import blog

# 创建app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# 注册蓝图
app.register_blueprint(site, url_prefix = '/site')
app.register_blueprint(blog, url_prefix = '/blog')

# 通过app创建manager对象
manager = Manager(app)

# 从模型创建数据库的指令
manager.add_command("server", Server())
@manager.shell
def make_shell_context():
    return dict(app=app,db=db)

if __name__ == '__main__':
    # 运行服务器
    manager.run()