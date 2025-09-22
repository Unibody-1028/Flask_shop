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

category_api.add_resource(Category,'/category')


@category.route('/category_list')
def category_list():
    return 'Hello'


