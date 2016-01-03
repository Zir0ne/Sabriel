"""
    分发器,实现交互协议的解析与分发,交互协议的格式如下:
    data_length(tcp only) | identification | type | protocol_data_length | data | nonce | hmac
             3                    20          1               4                    20      16
                           \______________/ \__________________________________/
                             xor by nonce                encrypted
    为了便于当前TCP通信机制下确认数据是否读取完毕,在交互协议前面添加了3个字节的数据长度指示,转为HTTP/SSL通信后,可以将
    这个字段去除. 收取数据完毕后,应当首先获取nonce,还原identification,然后根据identification检验hmac是否正确,从
    而确认数据的来源并同时检查数据的完整性.其次,解密协议数据,检查协议类型,交予合适的功能模块

    在未通过身份认证之前, identification内填充的是统一的临时身份标识. 协议数据使用预共享的固定密钥加密. hmac也用预共享
    的字串生成. 通过身份认证之后, identification内填充正式身份标识, 加密与hmac使用协商的秘密.
"""


class BadFormat(Exception):
    """ 交互协议数据格式错误, 引发该错误的可能性包括:
        1. 协议数据不完整
        2. 不能正常解密
        3. 无法校验数据来源
    """
    pass


class Dispatcher:
    """ 分发器
        解析交互协议, 检查协议数据的有效性, 并根据协议类型, 分发给指定模块
    """

    def regist_to_me(self):
        """ 功能模块调用此函数来向分发器注册, 只有向分发器注册过后, 交互协议才会分发至该模块 """
        pass

    def dispatch(self, data=bytearray()):
        """ 分发, 通信模块在完整收取一个请求后, 会调用此函数处理请求.
            在函数中, 首先调用内部函数__parse解析交互协议, 确认协议数据可靠.
            随后, 根据协议类别, 将解析好得交互协议分发给指定模块, 等待模块处理完毕
            最后, 将模块返回的数据通过内部函数__pack打包, 回传给通信模块
            @param data 原始交互协议数据
        """
        if len(data) < 56:
            raise BadFormat
        self.__parse(data)

    def __parse(self, raw_data):
        """ 解析交互协议 """
        raw_identification = raw_data[0:20]
        nonce = raw_data[-36:-16]
        hmac = raw_data[-16:]
        identification = [x ^ y for x, y in zip(raw_identification, nonce)]

    def __pack(self):
        """ 封装交互协议 """