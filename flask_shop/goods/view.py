from flask import request
from flask_shop.goods import goods,goods_api     # 导入蓝图,Api实例
from flask_shop import models,db
from flask_restful import Resource
from flask_shop.utils.message import to_dict_msg


@goods.route('/goods_list')
def get_goods_list():
    try:
        name = request.args.get('name')

        if name:
            # 如果提供了name,则根据商品名进行相似匹配
            goods = models.Goods.query.filter(models.Goods.name.like(f'%{name}%')).all()
        else:
            # 否则查询全部商品的信息
            goods = models.Goods.query.all()

        goods_list = [ gds.to_dict() for gds in goods]
        return to_dict_msg(200,goods_list,msg='获取商品列表成功!!!')
    except Exception as e:
        return to_dict_msg(20000)

class Goods(Resource):
    def delete(self):
        try:
            id = request.form.get('id')
            goods = models.Goods.query.get(id)
            if goods:
                db.session.delete(goods)
                db.session.commit()
                return to_dict_msg(200,msg='删除商品成功!!!')
            else:
                return to_dict_msg(10019)
        except Exception as e:
            return to_dict_msg(20000)

goods_api.add_resource(Goods,'/goods')