'''
Token 认证工具模块
核心功能:
1. 生成包含用户uid的时效性Token(基于SECRET_KEY加密)
2. 验证Token有效性
3. 提供登录拦截装饰器(@login_required),保护需要登录的接口
'''

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,request
from flask_shop.models import User
from flask_shop.utils.message import to_dict_msg
import functools


def generate_auth_token(uid,expiration):
    '''
    生成用户身份token
    :param uid: 用户id
    :param expiration:token有效期,单位:秒
    :return:加密后的token字符串
    '''
    # 创建加密对象,传入密钥和token有效期
    s = Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
    # 生成token
    # dumps()：将字典数据{'id': uid}加密为字节流
    # decode()：将字节流转换为字符串(便于前端存储和传输)
    return s.dumps({'id':uid}).decode()

def verify_auth_token(token_str) -> User | None:
    '''
    验证token有效性,并返回对应的用户实例
    :param token_str: 前端传入的token
    :return: 验证成功返回User实例,失败则返回None(或者触发异常)
    '''
    # 创建解密对象,使用与加密相同的SECRET_KEY
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        # 解密token,loads()将token字符串解密为原始字典数据
        data = s.loads(token_str)
        # 若token过期 则抛出异常
    except Exception as e:
        print(f"Token验证失败：{str(e)}")
        return to_dict_msg(10004,msg='token无效或已过期')

    # token解密成功后,根据解析出的用户id获取用户实例
    usr = User.query.filter_by(id=data['id']).first()
    # 返回用户实例,不存在则返回None
    return usr

def login_required(view_func):
    '''
    登录拦截装饰器:用于装饰需要登录才能访问的接口函数
    作用:自动验证请求头中的token,未登录/token无效则直接返回错误,不执行接口逻辑
    :param view_func:被装饰的接口函数
    :return:包装后的验证函数
    '''

    # 用@装饰器保留原函数元信息(如函数名,__doc__)
    # 避免装饰后函数名变为verify_token影响代码调试
    @functools.wraps(view_func)
    def verify_token(*args,**kwargs):
        '''
        内部验证函数,执行token验证逻辑
        :param args: 被装饰函数的位置参数
        :param kwargs: 被装饰函数的关键字参数
        :return: 验证成功则执行接口函数,否则返回错误响应
        '''

        try:
        # 从请求头中获取Token,前端需在请求头中携带token
        # 若请求头中没有token，会抛出KeyError异常
            token = request.headers['token']
        except Exception:
            return to_dict_msg(10003)
        # 验证token有效性
        user = verify_auth_token(token)
        # 判断用户是否存在
        if not user:
            # 用户不存在则返回错误码
            return to_dict_msg(10004, msg="token无效或已过期")
        # token验证通过,则执行原接口函数
        return view_func(*args,**kwargs)
    # 返回包装后的验证函数
    return verify_token