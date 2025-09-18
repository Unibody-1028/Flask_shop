'''
1.需要加密的数据  uid
2.加密算法       python模块
3.密钥          flask_app  SECRET_KEY
'''

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,request
from flask_shop.models import User
from itsdangerous import BadSignature,SignatureExpired  # 导入异常类
from flask_shop.utils.message import to_dict_msg
import functools


def generate_auth_token(uid,expiration):
    # 创建加密对象
    s = Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
    # 生成token
    return s.dumps({'id':uid}).decode()

def verify_auth_token(token_str) -> User | None:
    # 创建解密对象
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token_str)
    except Exception as e:
        print(f"Token验证失败：{str(e)}")
        return to_dict_msg(10004,msg='token无效或已过期')

    # 获取用户实例
    usr = User.query.filter_by(id=data['id']).first()
    return usr

def login_required(view_func):
    @functools.wraps(view_func) #用@装饰器保留原函数元信息
    def verify_token(*args,**kwargs):
        try:
            token = request.headers['token']
        except Exception:
            return to_dict_msg(10003)

        user = verify_auth_token(token)
        if not user:
            # 根据不同错误类型返回错误码
            return to_dict_msg(10004, msg="token无效或已过期")

        return view_func(*args,**kwargs)

    return verify_token