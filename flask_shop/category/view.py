from tkinter.font import names

from flask import request
from flask_shop.category import category,category_api    # 导入蓝图,Api实例
from flask_shop import models,db
from flask_restful import Resource
from flask_shop.utils.message import to_dict_msg




class Category(Resource):
    def post(self):
        try:
            name = request.form.get('name').strip() if request.form.get('name').strip() else ''
            level = int(request.form.get('level').strip()) if request.form.get('level').strip() else None
            pid = int(request.form.get('pid').strip()) if request.form.get('pid') else None

            if all([name,level]):
                c = models.Category(name=name,level=level,pid=pid)
                db.session.add(c)
                db.session.commit()
                return to_dict_msg(200,msg='增加商品类别成功')
            return to_dict_msg(10002)
        except Exception as e:
            return to_dict_msg(20000)

    def get(self):
        try:
            cid = request.args.get('cid')
            c = models.Category.query.get(cid)
            if c:
                return to_dict_msg(200,c.to_dict(),'获取商品分类信息成功')
            else:
                return to_dict_msg(status=10019)

        except Exception as e:
            return to_dict_msg(20000)

    def put(self):
        """
        处理PUT请求,用于更新商品分类信息
        接收分类ID和新名称,验证后更新数据库中对应的名称
        :return: JSON响应信息
        """
        try:
            # 从表单中获取分类ID和新名称
            cid = request.form.get('cid')
            name = request.form.get('name')
            # 根据id查询对应的数据
            c = models.Category.query.get(cid)
            # 判断分类是否存在
            if c:
                # 如果提供了新的名称,则更新分类名称,否则保持原名称不变
                if name is not None:
                    c.name = name
                # 提交事务,将修改保存到数据库
                db.session.commit()
                return to_dict_msg(status=200,msg='更新商品分类信息成功!!!')
            # 若分类不存在,返回错误信息:数据不存在
            return to_dict_msg(status=10019)
        except Exception as e:
            return to_dict_msg(20000)

    def delete(self):
        try:
            cid = request.form.get('cid')
            if cid is not None:
                c = models.Category.query.get(cid)
            else:
                return to_dict_msg(10002)
            if c:
                db.session.delete(c)
                db.session.commit()
                return to_dict_msg(200,msg='删除商品分类成功')
        except Exception as e:
            return to_dict_msg(20000)


category_api.add_resource(Category,'/category')


@category.route('/category_list')
def category_list():
    return 'Hello'


