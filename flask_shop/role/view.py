from flask import request
from flask_shop.role import role,role_api    # 导入蓝图,Api实例
from flask_shop import models,db
from flask_restful import Resource
from flask_shop.utils.message import to_dict_msg



class Role(Resource):
    # 获取角色列表
    def get(self):
        try:
            role_list = []
            roles = models.Role.query.all()
            role_list = [r.to_dict() for r in roles ]
            return to_dict_msg(200,data=role_list,msg='获取角色列表成功!!!')
        except Exception:
            return to_dict_msg(20004)
    # 创建新角色
    def post(self):
        name = request.form.get('name')
        desc = request.form.get('desc')
        try:
            if name:
                role = models.Role(name=name,desc=desc)
                db.session.add(role)
                db.session.commit()
                return to_dict_msg(status=200,msg='增加角色成功')
            return to_dict_msg(status=10002)
        except Exception as e:
            print(e)
            return to_dict_msg(status=20005)
    # 删除角色
    def delete(self):
        try:
            id = int(request.form.get('id'))
            r = models.Role.query.get(id)
            if r: # 是否找到用户
                db.session.delete(r)
                db.session.commit()
                return to_dict_msg(200,msg='删除角色成功')
            return to_dict_msg(status=10018)
        except Exception as e:
            return to_dict_msg(20000)



role_api.add_resource(Role,'/role')
