# db 是 Flask-SQLAlchemy 的数据库实例，用于定义模型和操作数据库
from flask_shop import db
# generate_password_hash: 用于将明文密码加密为哈希值
# check_password_hash: 用于验证明文密码与哈希值是否匹配
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

class BaseModel:
    create_time = db.Column(db.DateTime,default=datetime.now)
    update_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)

class User(db.Model,BaseModel):
    '''用户模型类,继承自db.Model(SQLAlchemy的模型基类)
    对应数据库中的't_user'表,存储用户的基本信息
    '''
    # 定义数据库表名和表字段
    __tablename__ = 't_user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),unique=True,nullable=False)
    pwd = db.Column(db.String(128))
    nick_name = db.Column(db.String(32))
    phone = db.Column(db.String(11))
    email = db.Column(db.String(32))

    # 密码属性访问器
    @property
    def password(self):
        '''通过password属性获取密码
        :return:返回存储的哈希值
        '''
        return self.pwd

    # 密码设置器
    @password.setter
    def password(self,t_pwd):
        '''设置密码时自动加密,当执行user.password = '明文密码'时,会自动调用该方法,将明文密码通过
        generate_password_hash加密后存入pwd
        :param t_pwd:用户输入的明文密码
        '''
        self.pwd = generate_password_hash(t_pwd)

    def check_password(self,t_pwd):
        '''验证明文密码与存储的哈希值是否匹配
        :param t_pwd:需要验证的明文密码
        :return:bool:匹配返回True,不匹配返回False
        '''
        return check_password_hash(self.pwd,t_pwd)

class Menu(db.Model):
    __tablename__ = 't_menu'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(32),unique=True,nullable=False)
    level = db.Column(db.Integer,nullable=False)
    path = db.Column(db.String(32))

    pid = db.Column(db.Integer)
    children = db.relationship('Menu')

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'level':self.level,
            'path':self.path,
            'pid':self.pid,
            'children':self.get_child_list()
        }
    def get_child_list(self):
        obj_child = self.children
        data = []
        for o in obj_child:
            data.append(o.to_dict())

        return data
