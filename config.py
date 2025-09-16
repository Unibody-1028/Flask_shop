import os


class Config:
    # 配置MYSQL参数
    MYSQL_DIALECT = 'mysql'
    MYSQL_DRIVER = 'pymysql'
    MYSQL_NAME = 'root'
    MYSQL_PWD = '123456'
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = '3306'
    MYSQL_DB = 'flask_shop'
    MYSQL_CHARSET= 'utf8mb4'
    # 拼接SQLAlchemy数据库连接URI
    SQLALCHEMY_DATABASE_URI = (f'{MYSQL_DIALECT}+{MYSQL_DRIVER}://{MYSQL_NAME}:{MYSQL_PWD}'
                               f'@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset={MYSQL_CHARSET}')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.urandom(16)
    PORT = 8088

class DevelopmentConfig(Config):
    DEBUG = True
class ProductionConfig(Config):
    DEBUG = False

config_map={
    'develop':DevelopmentConfig,
    'product':ProductionConfig
}