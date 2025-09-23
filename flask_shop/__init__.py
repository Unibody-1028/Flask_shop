from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_map

# 初始化数据库实例,不绑定数据库
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)

    # 通过参数获取到不同开发环境的配置文件
    config_class = config_map.get(config_name)
    if not config_class:
        raise ValueError(f"配置名称 {config_name} 不存在")

    # 将配置类的参数加载到Flask应用
    app.config.from_object(config_class)

    # 初始化app对象后,再绑定数据库
    db.init_app(app)

    # 注册user蓝图
    from flask_shop.user import user as user_bp
    app.register_blueprint(user_bp)

    # 注册menu蓝图
    from flask_shop.menu import menu as menu_bp
    app.register_blueprint(menu_bp)

    # 注册role蓝图
    from flask_shop.role import role as role_bp
    app.register_blueprint(role_bp)

    # 注册category蓝图
    from flask_shop.category import category as category_bp
    app.register_blueprint(category_bp)

    # 注册attribute蓝图
    from flask_shop.category import attribute as attribute_bp
    app.register_blueprint(attribute_bp)

    # 注册goods蓝图
    from flask_shop.goods import goods as goods_bp
    app.register_blueprint(goods_bp)
    return app



