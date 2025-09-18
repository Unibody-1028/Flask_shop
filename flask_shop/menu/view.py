from flask import request
from flask_shop.menu import menu_api,menu     # 导入蓝图,Api实例
from flask_shop import models,db
from flask_restful import Resource
from flask_shop.utils.message import to_dict_msg


class Menu(Resource):
    def get(self):
        '''
        逻辑：
        每个菜单实例调用to_dict()时,会通过get_child_list()获取自己的子菜单。
        get_child_list()先通过self.children拿到子菜单实例。
        对每个子菜单实例递归调用to_dict(),将子菜单也转为包含自身子菜单的字典。
        最终形成嵌套字典列表,形成菜单的层级结构。
        :args   type参数:list,tree
        :return:菜单的嵌套字典列表
        '''
        menu_list = []
        type_ = request.args.get('type')
        if type_ == 'list':
            # 获取数据,并将数据填充到menu_list
            mu = models.Menu.query.filter(models.Menu.level!=0).all()
            for m in mu:
                menu_list.append(m.to_dict())
            return menu_list
        elif type_ == 'tree':
            mu = models.Menu.query.filter(models.Menu.level==1).all()
            for m in mu:
                menu_list.append(m.to_dict())
            return menu_list
        else:
            return to_dict_msg(20001)


menu_api.add_resource(Menu,'/menu')
