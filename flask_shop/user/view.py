import re
from flask import request
from flask_shop.user import user,user_api     # 导入蓝图,Api实例
from flask_shop import models,db
from flask_restful import Resource
from flask_shop.utils.message import to_dict_msg

@user.route('/')
def index():
    return 'Hello_User'

class User(Resource):
    def get(self):
        pass

    # 客户端发送POST请求到绑定的url时,自动执行此方法
    def post(self):
        # 获取前端参数(默认值设置为空,避免None错误)

        name = request.form.get('name','').strip()
        pwd = request.form.get('pwd','').strip()
        real_pwd = request.form.get('real_pwd','').strip() # 确认密码
        nick_name = request.form.get('nick_name','').strip()
        phone = request.form.get('phone','').strip()
        email = request.form.get('email','').strip()
        # 验证数据的正确性
        if not all([name,pwd,real_pwd]):
            return to_dict_msg(10000)
        if len(name) < 1 or len(name)>16:
            return to_dict_msg(10011)
        if len(pwd) < 6 :
            return to_dict_msg(10012)
        if pwd != real_pwd:
            return to_dict_msg(10013)
        if not re.match(r'^1[3456789]\d{9}$',phone):
            return to_dict_msg(10014)
        print(phone)
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',email):
            return to_dict_msg(10015)
        # 验证用户名是否已经存在
        existing_user = models.User.query.filter_by(name=name).first()
        # print(existing_user)
        if existing_user:
            return to_dict_msg(10030)

        try:
            # 使用models内定义的User类创建对象
            usr = models.User(
                name=name,
                password=pwd,
                phone=phone,
                email=email,
                nick_name=nick_name)
            db.session.add(usr)
            db.session.commit()
        except Exception as e:
            # 发生错误时回滚会话，避免数据不一致
            db.session.rollback()
            # 记录错误日志
            print(f"注册失败：{str(e)}")
            return to_dict_msg(20000)
        return to_dict_msg(status=200,msg='用户注册成功')








# 将User资源类与URL路径'/user'绑定
user_api.add_resource(User,'/user')
'''
客户端访问http://域名/蓝图前缀/user时,
如果发送POST请求:执行User.post()方法
如果发送GET请求:执行User.get()方法

'''


@user.route('/login',methods=['POST'])
def login():
    name = request.form.get('name')
    pwd = request.form.get('pwd')

    if not all([name,pwd]):
        return {'status':10000,'msg':'数据不完整'}
    if len(name) >1:
        usr = models.User.query.filter_by(name=name).first()
        if usr:
            if usr.check_password(pwd):
                return {'status':200,'msg':'登录成功'}

        return {'status':10001,'msg':'用户名或密码错误'}
