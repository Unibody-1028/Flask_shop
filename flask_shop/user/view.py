import re
from flask import request
from flask_shop.user import user,user_api     # 导入蓝图,Api实例
from flask_shop import models,db
from flask_restful import Resource,reqparse
from flask_shop.utils.message import to_dict_msg
from flask_shop.utils.tokens import generate_auth_token,login_required,verify_auth_token


@user.route('/')
def index():
    return 'Hello_User'

class User(Resource):
    '''
    用户信息API资源类，继承自flask_restful.Resource
    提供三种HTTP方法：
    - GET：根据ID查询单个用户的详细信息
    - POST：处理用户注册功能，创建新用户
    - PUT: 修改用户信息
    '''

    # 客户端发送GET请求到'.../url_prefix/user',自动执行此方法
    def get(self):
        '''
        处理GET请求,根据用户ID查询用户信息
        :return:格式化的JSON响应，包含查询到的用户信息和提示消息
        '''
        try:
            # 获取并处理请求参数中的id,从查询字符串中获取'id'参数，并去除前后空格
            # 并转换为int类型以确保id是整数，符合数据库字段类型
            id = int(request.args.get('id').strip()) # request是Flask提供的全局对象,用于处理客户端的http请求
            # 使用id查询用户
            # 使用SQLAlchemy的filter_by方法精确匹配id，first()返回第一个匹配的用户对象
            usr = models.User.query.filter_by(id=id).first()
            if usr:
                # 若查询到用户，调用用户对象的to_dict()方法转换为字典，返回成功响应
                return to_dict_msg(200,usr.to_dict(),'获取用户信息成功')
            else:
                # 若未查询到用户，返回空列表和提示信息
                return to_dict_msg(200,[],'没有此用户')
        except Exception as e:
            print(e)
            return to_dict_msg(10000)

    # 客户端发送POST请求到'.../url_prefix/user',自动执行此方法
    def post(self):
        '''
        处理POST请求，实现用户注册功能
        接收前端表单数据，验证合法性后创建新用户
        :return: 注册结果的格式化响应
        '''

        # 获取前端提交的表单数据,默认值设置为空,避免None错误
        name = request.form.get('name','').strip()
        pwd = request.form.get('pwd','').strip()
        real_pwd = request.form.get('real_pwd','').strip() # 确认密码
        nick_name = request.form.get('nick_name','').strip()
        phone = request.form.get('phone','').strip()
        email = request.form.get('email','').strip()
        # 数据合法性校验
        if not all([name,pwd,real_pwd]):
            return to_dict_msg(10000)
        if len(name) < 1 or len(name)>16:
            return to_dict_msg(10011)
        if len(pwd) < 6 :
            return to_dict_msg(10012)
        if pwd != real_pwd:
            return to_dict_msg(10013)
        # 验证手机号格式
        if not re.match(r'^1[3456789]\d{9}$',phone):
            return to_dict_msg(10014)
        # 验证邮箱格式
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',email):
            return to_dict_msg(10015)
        # 验证用户名唯一性
        existing_user = models.User.query.filter_by(name=name).first()
        # print(existing_user)
        if existing_user:
            return to_dict_msg(10030)

        try:
            # 使用models内定义的User类创建对象
            usr = models.User(
                name=name,
                password=pwd, # 设置密码时会自动触发User的password.setter实现自动加密
                phone=phone,
                email=email,
                nick_name=nick_name)
            db.session.add(usr) # 添加到会话
            db.session.commit() # 提交事务(保存到数据库)
        except Exception as e:
            # 发生错误时回滚会话，避免数据不一致
            db.session.rollback()
            # 记录错误日志
            print(f"注册失败：{str(e)}")
            return to_dict_msg(20000)
        return to_dict_msg(status=200,msg='用户注册成功')

    # 客户端发送PUT请求到'.../url_prefix/user',自动执行此方法
    def put(self):
        try:
            id = int(request.form.get('id').strip())
            email = request.form.get('email').strip() if request.form.get('email') else ''
            phone = request.form.get('phone').strip() if request.form.get('phone') else ''
            # 根据id获取用户实例
            usr = models.User.query.get(id)
            if usr:
                usr.email = email
                usr.phone = phone
                db.session.commit()
                return to_dict_msg(200,msg='修改数据成功!')
            else:
                return to_dict_msg(10016)
        except Exception:
            return to_dict_msg(20002)




# 将User资源类与URL路径'/user'绑定
user_api.add_resource(User,'/user')
'''
客户端访问http://域名/蓝图前缀/user时,
如果发送POST请求:执行User.post()方法
如果发送GET请求:执行User.get()方法
'''

class UserList(Resource):
    '''
    获取用户API资源类
    提供GET方法用于获取用户列表,支持条件查询和分页功能
    '''
    def get(selfs):
        '''
        处理GET请求,获取用户列表
        支持通过name参数筛选用户,通过pnum和nsize实现分页
        :return: 格式化的JSON响应,包括分页信息和用户列表数据
        '''
        # 初始化请求参数解析器,用于提取和验证url中的查询参数
        parser = reqparse.RequestParser()
        parser.add_argument('name',type=str)  # 用于用户名模糊查询
        parser.add_argument('pnum',type=int)  # 指定当前页码
        parser.add_argument('nsize',type=int) # 指定每页的记录数
        try:
            # 解析请求参数
            args = parser.parse_args()
            # 提取参数值，对可选参数设置默认值
            name = args.get('name') # 默认为None
            pnum = args.get('pnum') if args.get('pnum') else 1 # 默认值为1
            nsize = args.get('nsize') if args.get('nsize') else 2 # 默认值为2
            # 根据查询条件查询用户数据，并实现分页
            if name:
                # 如果提供了name,就按照name进行模糊查询
                # 使用paginate(pnum,nsize)实现分页
                user_p = models.User.query.filter(models.User.name.like(f'%{name}%')).paginate(pnum,nsize)
            else:
                # 若未提供name参数，查询所有用户并分页
                user_p = models.User.query.paginate(pnum,nsize)
            # 构造响应数据
            data = {
                'pnum': pnum,  # 当前页码
                'totalPage': user_p.total,  # 总记录数（来自分页对象）
                # 将用户对象列表转换为字典列表（调用User模型的to_dict()方法）
                'users': [u.to_dict() for u in user_p.items]
            }
            # 返回成功响应（使用自定义函数格式化，状态码200表示成功）
            return to_dict_msg(200,data,'获取用户列表成功')

        except Exception as e:
            # 捕获异常，打印错误信息并返回通用错误响应
            print(e)
            return to_dict_msg(10000)

# 将UserList资源注册到用户API蓝图（user_api），并映射到URL路径'url_prefix/user_list'
# 客户端可通过GET请求访问该路径获取用户列表
user_api.add_resource(UserList,'/user_list')


# 用户登录接口,处理POST请求,验证用户身份并生成token
@user.route('/login',methods=['POST'])
def login():
    '''
    用户登录接口:接收前端提交的用户名和密码,验证通过后生成token
    params:(form-data)
            -name:用户名
            -pwd:密码
    :return:
    '''

    # 从请求体中获取用户名和密码
    name = request.form.get('name')
    pwd = request.form.get('pwd')
    # 验证用户名和密码非空
    if not all([name,pwd]):
        return to_dict_msg(status=10002)
    # 验证用户名长度
    if len(name) >1:
        # 通过用户名精确查找数据库获取用户实例
        usr = models.User.query.filter_by(name=name).first()
        # 若查找到用户
        if usr:
            # 调用User模型的check_password方法验证密码
            if usr.check_password(pwd):
                # 密码验证通过则生成token
                token = generate_auth_token(usr.id,expiration=3600)
                # 返回成功响应
                return to_dict_msg(status=200,data={'token':token})
        # 错误响应
        return to_dict_msg(status=10001)


# 获取用户信息接口,需要登录才能访问
@user.route('/get_user_info',methods=['GET'])
@login_required # 等价于get_user_info = login_required(get_user_info)
# 作用:先执行login_required逻辑(验证请求中的token是否有效),通过后才执行get_user_info
def get_user_info():
    """
    获取用户信息接口:需要携带有效token才能访问,验证token后返回用户信息

    :return:
    """

    # 获取用户信息
    name = request.form.get('name')
    pwd = request.form.get('pwd')
    # 验证用户信息非空
    if not all([name,pwd]):
        return to_dict_msg(status=10002)
    # 验证用户名长度并根据name查询用户
    if len(name) >1:
        usr = models.User.query.filter_by(name=name).first()
        # 如果查询到用户
        if usr:
            # 验证密码
            if usr.check_password(pwd):
                # 获取token并验证token有效性
                token = request.headers.get('token')
                if verify_auth_token(token) is not None:
                    # token验证通过,返回成功响应
                    return to_dict_msg(status=200,msg='获取user信息成功')
    # 获取用户信息失败,返回业务错误码
    return to_dict_msg(10004)

