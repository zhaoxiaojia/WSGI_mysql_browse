#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time    :2020/5/4 10:04
# @Author  :Coco
# @FileName: web_server_wsgi.py

# @Software: PyCharm
"""
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓ ┏┓
            ┏┛┻━┛┻━┓
            ┃   ☃  ┃
            ┃ ┳┛ ┗┳ ┃
            ┃   ┻   ┃
            ┗━┓   ┏━┛
               ┃     ┗━━┓
               ┃        ┣┓
               ┃　      ┏┛
               ┗┓┓━━┳┓━┛
                 ┃┫  ┃┫
                 ┗┛  ┗┛
"""

import socket
import sys
import re
import multiprocessing


class WSGIServer:

    def __init__(self, port, app):
        # 创建tcp 套接字 并关闭后立即释放端口
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 绑定端口
        self.tcp_server_socket.bind(('', port))
        # 设置为监听套接字
        self.tcp_server_socket.listen(128)
        self.application = app

    def server_client(self, new_socket):
        # 获取请求信息
        request = new_socket.recv(1024).decode('utf-8')
        # 从请求信息中获取需要请求的页面
        if not request:
            return
        request_lines = request.splitlines()
        file_name = ''
        ret = re.match(r'[^/]+(/[^ ]*)', request_lines[0])
        if ret:
            file_name = ret.group(1)
            if file_name == '/':
                file_name = '/index.html'
        # 判断请求是否为静态网页
        if not file_name.endswith('.html'):
            # 当请求为静态网页是，从static文件夹下读取响应数据并返回
            try:
                with open('./static' + file_name, 'rb') as f:
                    content = f.read()
            except Exception as e:
                # 返回 file not found
                response = 'HTTP/1.1 404 NOT FOUND \r\n'
                response += '\r\n'
                response += '-----FILE NOT FOUND-----'
                new_socket.send(response.encode('utf-8'))
            else:
                # 返回改静态文件
                response = 'HTTP/1.1 200 OK\r\n'
                response += '\r\n'
                new_socket.send(response.encode('utf-8'))
                new_socket.send(content)
        else:
            # 将文件名存入字典
            env = dict()
            # {"PATH_INFO": "/index.html"}
            env['PATH_INFO'] = file_name
            # 从mini_frame中获取返回主体
            body = self.application(env, self.set_response_header)
            # 定义头文件
            header = 'HTTP/1.1 %s\r\n' % self.status
            # 补充头文件信息

            for temp in self.headers:
                header += '%s:%s\r\n' % (temp[0], temp[1])
            header += '\r\n'
            response = header + body
            new_socket.send(response.encode('utf-8'))
        new_socket.close()

    def set_response_header(self, status, headers):
        self.status = status
        self.headers = [("server", "mini_web v8.8")]
        self.headers += headers

    def run_forever(self):
        while True:
            new_socket, client_addr = self.tcp_server_socket.accept()
            p = multiprocessing.Process(target=self.server_client, args=(new_socket,))
            p.start()
            new_socket.close()
        self.tcp_server_socket.close()


if __name__ == '__main__':
    # 判断输入是否符合要求
    # python3 xxxx.py 7890 mini_frame:application
    if len(sys.argv) == 3:
        try:
            port = int(sys.argv[1])
            frame_app = sys.argv[2]
        except Exception as e:
            print('端口输入有误')

    else:
        print("请按照以下方式运行:")
        print("python3 xxxx.py 7890 mini_frame:application")
    ret = re.match(r'([^:]+):(.*)', frame_app)
    if ret:
        # 从输入中提取类名
        frame_name = ret.group(1)
        # 从输入中提取方法名
        app_name = ret.group(2)
    else:
        print("请按照以下方式运行:")
        print("python3 xxxx.py 7890 mini_frame:application")
    sys.path.append('./dynamic')
    frame = __import__(frame_name)
    app = getattr(frame, app_name)
    wsgi = WSGIServer(port, app)
    wsgi.run_forever()
