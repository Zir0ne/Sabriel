"""
    提供密码操作支持
"""

from cryptography import exceptions as     crypt_exceptions
from cryptography.hazmat.backends   import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hmac


def hash_mac(key=bytes(), message=bytes()):
    """ 提供hmac支持, 采用sha1 hash算法
        @param  key     密钥, 应当为20字节随机生成的字节串
        @param  message 原始消息
        @return         20字节hash值
    """
    try:
        h = hmac.HMAC(key, hashes.SHA1(), backend=default_backend())
        h.update(message)
        return h.finalize()
    except crypt_exceptions.UnsupportedAlgorithm:
        print("The default backend is not support SHA1 authenticated-MAC")
        return None


def hash_mac_verify(key=bytes(), message=bytes(), signature=bytes()):
    """ 验证给定的签名是否正确
        @param key       密钥, 应当为20字节随机生成的字节串
        @param message   原始消息
        @param signature 需要验证的, 原始消息的签名
        @return          返回True或者False
    """
    try:
        h = hmac.HMAC(key, hashes.SHA1(), backend=default_backend())
        h.update(message)
        h.verify(signature)
        return True
    except crypt_exceptions.InvalidSignature:
        return False
    except TypeError:
        print("The signature should be byte array")
        return False
