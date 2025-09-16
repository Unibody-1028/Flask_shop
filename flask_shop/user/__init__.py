from flask import Blueprint
from flask_restful import Api



# 创建用户蓝图
user = Blueprint('user',__name__,url_prefix='/user')

user_api = Api(user)

from flask_shop.user import view