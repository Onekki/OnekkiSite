import os

# 项目绝对路径
BASE_DIR = os.getcwd()
# 模版文件路径
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
# 静态文件路径
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# 数据库URI
MYSQL_DATABASE_URI = 'mysql+pymysql://root:zwq123456@39.107.230.35:3306/onekki_site'

class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = MYSQL_DATABASE_URI
    # 查询跟踪，不太需要，False，不占用额外的内存
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    SECRET_KEY = 'CCCD756A-954C-4390-A38F-C018340769BD'
    RECAPTCHA_PUBLIC_KEY = '6LcqjqsUAAAAAItx4Fhs-bhG9L4rcXT4hbXooZTL'
    RECAPTCHA_PRIVATE_KEY = '6LcqjqsUAAAAAJlGpkoXjT1HY-nQ1lQLklwqUWug'
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    CELERY_RESULT_BACKEND = 'redis://39.107.230.35:6379/0'
    CELERY_BROKER_URL = 'redis://39.107.230.35:6379/0'
    pass


class TestingConfig(BaseConfig):
    TESTING = True
    pass

class ProductionConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

