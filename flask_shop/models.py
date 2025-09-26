# db 是 Flask-SQLAlchemy 的数据库实例，用于定义模型和操作数据库
from sqlalchemy.orm import backref, foreign

from flask_shop import db
# generate_password_hash: 用于将明文密码加密为哈希值
# check_password_hash: 用于验证明文密码与哈希值是否匹配
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

class BaseModel:
    create_time = db.Column(db.DateTime,default=datetime.now)
    update_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)

class User(db.Model,BaseModel):
    """用户模型类,继承自db.Model(SQLAlchemy的模型基类)
    对应数据库中的't_user'表,存储用户的基本信息
    """
    # 定义数据库表名和表字段
    __tablename__ = 't_user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),unique=True,nullable=False)
    pwd = db.Column(db.String(128))
    nick_name = db.Column(db.String(32))
    phone = db.Column(db.String(11))
    email = db.Column(db.String(32))

    rid = db.Column(db.Integer,db.ForeignKey('t_role.id'))

    # 密码属性访问器
    @property
    def password(self):
        """通过password属性获取密码
        :return:返回存储的哈希值
        """
        return self.pwd

    # 密码设置器
    @password.setter
    def password(self,t_pwd):
        """设置密码时自动加密,当执行user.password = '明文密码'时,会自动调用该方法,将明文密码通过
        generate_password_hash加密后存入pwd
        :param t_pwd:用户输入的明文密码
        """
        self.pwd = generate_password_hash(t_pwd)

    def check_password(self,t_pwd):
        """验证明文密码与存储的哈希值是否匹配
        :param t_pwd:需要验证的明文密码
        :return:bool:匹配返回True,不匹配返回False
        """
        return check_password_hash(self.pwd,t_pwd)

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'nick_name':self.nick_name,
            'phone':self.phone,
            'email':self.email,
            # 先确保self.role不为None，再判断name不为None
            'role_name':self.role.name if (self.role is not None and self.role.name is not None) else ''
        }

trm = db.Table('t_role_menu',
    db.Column('rid',db.Integer,db.ForeignKey('t_role.id')),
    db.Column('mid', db.Integer, db.ForeignKey('t_menu.id'))


)
class Menu(db.Model):
    """
    菜单模型类,继承自SQLAlchemy的Model基类,用于存储系统中的菜单数据,支持层级结构,
    对应的数据库表名为't_menu'
    """
    __tablename__ = 't_menu'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),unique=True,nullable=False)
    level = db.Column(db.Integer)
    # 菜单路径：字符串类型，最大长度32（通常对应前端路由路径，如'/user'）
    path = db.Column(db.String(32))
    # 若为顶级菜单，pid为null
    pid = db.Column(db.Integer,db.ForeignKey('t_menu.id'))

    # 子菜单列表：通过relationship定义与自身的关联，自动查询当前菜单的所有子菜单
    # 访问方式：menu.children 可获取当前菜单的所有子菜单实例
    children = db.relationship('Menu')
    roles = db.relationship('Role',secondary=trm)

    def to_dict(self):
        """
        将菜单实例转换为字典（包含所有子菜单的嵌套结构）
        用于接口返回或数据序列化（如转换为JSON）
        :return: 包含菜单信息的字典，其中children字段为子菜单的字典列表
        """
        return {
            'id':self.id,
            'name':self.name,
            'level':self.level,
            'path':self.path,
            'pid':self.pid,
            'children':self.get_child_list()
        }
    def get_child_list(self):
        """
        递归获取当前菜单的所有子菜单，并转换为字典列表
        实现层级菜单的嵌套结构
        :return: 子菜单的字典列表（每个子菜单包含自身的子菜单）
        """
        # 获取当前菜单的所有子菜单实例（通过relationship自动查询）
        obj_child = self.children
        # 用于存储子菜单字典的列表
        data = []
        # 遍历每个子菜单实例
        for o in obj_child:
            # 递归调用to_dict()，将子菜单转换为字典（包含它的子菜单）
            data.append(o.to_dict())
        # 返回子菜单的字典列表
        return data


class Role(db.Model):
    __tablename__ = 't_role'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),unique=True,nullable=False)
    desc = db.Column(db.String(64))

    users = db.relationship('User',backref='role')
    menus = db.relationship('Menu',secondary=trm)

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'desc':self.desc,
            'menu':self.get_menu_dict()
        }

    def get_menu_dict(self):
        menu_list = []  # 用于存储最终的层级菜单结构
        # 遍历当前角色拥有的所有菜单（self.menus 是多对多关联的菜单列表）
        menus = sorted(self.menus,key= lambda temp:temp.id) # 使用sorted函数对菜单进行排序,参数key指定排序规则
        for m in menus:
            # 筛选出一级菜单（level=1）
            if m.level == 1:
                # 调用菜单自身的 to_dict() 方法，获取基础信息（id、name、path等）
                first_dict = m.to_dict()
                # 初始化一级菜单的 children 列表（用于存放它的二级菜单）
                first_dict['children'] = []
                # 再次遍历所有菜单，筛选当前一级菜单的二级菜单
                for s in menus:
                    # 二级菜单条件：level=2 且 父菜单id（pid）等于当前一级菜单的id
                    if s.level == 2 and s.pid == m.id:
                        # 将符合条件的二级菜单添加到一级菜单的 children 中
                        first_dict['children'].append(s.to_dict())
                # 将整理好的一级菜单（含二级菜单）添加到结果列表
                menu_list.append(first_dict)
        # 返回最终的层级菜单结构
        return menu_list
class Category(db.Model):
    __tablename__ = 't_category'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),nullable=False)
    level = db.Column(db.Integer)
    pid = db.Column(db.Integer,db.ForeignKey('t_category.id'))

    children = db.relationship('Category')
    attrs = db.relationship('Attribute',backref='category')
    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'level':self.level,
            'pid':self.pid
        }


class Attribute(db.Model):
    __tablename__ = 't_attribute'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32))
    val = db.Column(db.String(255))
    cid = db.Column(db.Integer,db.ForeignKey('t_category.id'))
    _type = db.Column(db.Enum('static','dynamic'))

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'val':self.val,
            'cid':self.cid,
            'type':self._type
        }


class Goods(db.Model):
    __tablename__ = 't_goods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))
    price = db.Column(db.Float)
    number = db.Column(db.Integer)
    introduce = db.Column(db.Text)
    big_log = db.Column(db.String(256))
    small_log = db.Column(db.String(256))
    status = db.Column(db.Integer)  # 商品审核状态 0:未通过  1:审核中  2:已审核
    is_promote = db.Column(db.Integer)  # 是否促销
    hot_number = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    cid_one = db.Column(db.Integer, db.ForeignKey('t_category.id'))
    cid_two = db.Column(db.Integer, db.ForeignKey('t_category.id'))
    cid_three = db.Column(db.Integer, db.ForeignKey('t_category.id'))

    category = db.relationship("Category",foreign_keys=[cid_three])
    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'price':self.price,
            'number':self.number,
            'introduce':self.introduce,
            'big_log':self.big_log,
            'small_log':self.small_log,
            'status':self.status,
            'is_promote':self.is_promote,
            'hot_number':self.hot_number,
            'weight':self.weight,
            'cid_one':self.cid_one,
            'cid_two':self.cid_two,
            'cid_three':self.cid_three,
            'attrs':[a.to_dict() for a in self.category.attrs]
        }

class Picture(db.Model):
    __tablename__ = 't_picture'
    id = db.Column(db.Integer,primary_key=True)
    path = db.Column(db.String(512))
    gid = db.Column(db.Integer,db.ForeignKey('t_goods.id'))

class GoodsAttr(db.Model):
    __tablename__ = 't_goods_attr'
    gid = db.Column(db.Integer,db.ForeignKey('t_goods.id'),primary_key=True)
    aid = db.Column(db.Integer,db.ForeignKey('t_attribute.id'),primary_key=True)

    val = db.Column(db.String(512))
    _type = db.Column(db.String(8))

class Order(db.Model,BaseModel):
    __tablename__ = 't_order'
    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.Integer,db.ForeignKey('t_user.id'))
    price = db.Column(db.Float)

    number = db.Column(db.Integer)
    pay_status = db.Column(db.Integer) #0:未支付,1:已支付
    is_send = db.Column(db.Integer) # 0:未发货,1:已发货
    fapiao_title = db.Column(db.String(32))
    fapiao_company = db.Column(db.String(128))
    fapiao_content = db.Column(db.String(512))
    addrs = db.Column(db.String(512))

    user = db.relationship('User',foreign_keys=[uid])
    order_detail = db.relationship('OrderDeatil',backref='order')
    express = db.relationship('Express',backref='order')

    def to_dict(self):
        return {
            'id':self.id,
            'uid':self.uid,
            'uname':self.user.name,
            'price':self.price,
            'number':self.number,
            'pay_status':self.pay_status,
            'is_send':self.is_send,
            'fapiao_title':self.fapiao_title,
            'fapiao_content':self.fapiao_content,
            'addrs':self.addrs
        }


class OrderDeatil(db.Model):
    __tablename__ = 't_order_detail'
    gid = db.Column(db.Integer,db.ForeignKey('t_goods.id'),primary_key=True)
    oid = db.Column(db.Integer,db.ForeignKey('t_order.id'),primary_key=True)
    number = db.Column(db.Integer)
    price = db.Column(db.Float)
    total_price = db.Column(db.Float)

class Express(db.Model):
    __tablename__ = 't_express'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(64))
    update_time = db.Column(db.String(32))
    oid = db.Column(db.Integer, db.ForeignKey('t_order.id'))
