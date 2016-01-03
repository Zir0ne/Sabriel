"""
    通信模块,提供如下功能:
    1. 通信数据加密,隐藏,来源识别
    2. 基于HTTP/SSL
    当前为了简便与快速的验证整体框架功能,实现为基于TCP的明文通信机制
"""

import socketserver
import threading
import time
import struct

from dispatcher import Dispatcher


class RequestHandler(socketserver.StreamRequestHandler):
    """ 处理通信请求,解析载荷数据,还原交互协议数据,交予分发器,收取响应,回复 """

    # 分发器的实例
    protocol_dispatcher = Dispatcher()

    def handle(self):
        """ 重写处理请求的函数,实现我们自定义的处理方式 """
        try:
            count_of_bytes = struct.unpack("<L", bytes(self.request.recv(3)))
            protocol_data = bytearray(self.request.recv(count_of_bytes))
            while len(protocol_data) < count_of_bytes:
                remain_data = bytearray(self.request.recv(count_of_bytes))
                protocol_data += remain_data
            RequestHandler.protocol_dispatcher.dispatch(data=protocol_data)
        except:
            pass


class ThreadingTcpServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """ 多线程并发型TCP服务器 """

    # 最多可以处理10个客户端的并发请求,注意是并发请求,并不是最大客户端数量
    request_queue_size = 10


if __name__ == "__main__":
    listener = ThreadingTcpServer(("127.0.0.1", 9090), RequestHandler)
    # 另起线程来运行TCP服务器
    server_thread = threading.Thread(target=listener.serve_forever)
    # 当主线程退出时,也停止server_thread
    server_thread.daemon = True
    server_thread.start()
    time.sleep(3)
    listener.shutdown()
    listener.server_close()
