from flask import Blueprint
from flask_restful import Api

category = Blueprint('category',__name__)
category_api = Api(category)

from flask_shop.category import view