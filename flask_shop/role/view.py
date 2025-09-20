from flask import request
from flask_shop.role import role,role_api    # 导入蓝图,Api实例
from flask_shop import models,db
from flask_restful import Resource
from flask_shop.utils.message import to_dict_msg



class Role(Resource):
    def get(self):
        try:
            role_list = []
            roles = models.Role.query.all()
            role_list = [r.to_dict() for r in roles ]
            return to_dict_msg(200,data=role_list,msg='获取角色列表成功!!!')
        except Exception:
            return to_dict_msg(20004)


role_api.add_resource(Role,'/role')
