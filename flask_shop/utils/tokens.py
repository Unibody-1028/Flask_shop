'''
1.需要加密的数据  uid
2.加密算法       python模块
3.密钥          flask_app  SECRET_KEY
'''

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_shop.models import User
from itsdangerous import BadSignature,SignatureExpired  # 导入异常类

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
    except SignatureExpired:
        print("Token已过期")
        return None
    except BadSignature:
        print("Token无效（可能被篡改）")
        return None
    except Exception as e:
        print(f"Token验证失败：{str(e)}")
        return None

    # 获取用户实例
    usr = User.query.filter_by(id=data['id']).first()
    return usr
