from flask_shop.order import order, order_api
from flask_shop import models, db
from flask import request
from flask_restful import Resource
from flask_shop.utils.message import to_dict_msg


@order.route('/order_list')
def order_list():
    id = request.args.get('id')
    if id:
        order = models.Order.query.get(id)
        if order:
            return to_dict_msg(200, data=order.to_dict(), msg='获取订单成功')
        else:
            return to_dict_msg(10019)

    orders = models.Order.query.all()
    return to_dict_msg(200, data=[o.to_dict() for o in orders], msg='获取订单列表成功')


@order.route('/express')
def get_express():
    oid = request.args.get('id')
    if oid:
        exps = models.Express.query.filter((models.Express.oid == oid)).order_by(models.Express.update_time.desc()).all()
        if exps:
            return to_dict_msg(200,data=[e.to_dict() for e in exps])
        else:
            return to_dict_msg(200,msg='数据不存在')
    else:
        return to_dict_msg(10002)