import os
from flask_script import Manager, Server
from app import create_app, db

# 创建app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# 通过app创建manager对象
manager = Manager(app)

# 从模型创建数据库的指令
manager.add_command("server", Server(host='0.0.0.0', port=80))

@manager.shell
def make_shell_context():
    return dict(app, db)

if __name__ == '__main__':
    # 运行服务器
    manager.run()