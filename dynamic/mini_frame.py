#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time    :2020/5/4 10:16
# @Author  :Coco
# @FileName: mini_frame.py

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

import re

URL_FUNC_DICT = {}


def route(url):
    def set_func(func):
        URL_FUNC_DICT[url] = func
        def call_func(*args, **kwargs):
            return func(*args, *kwargs)

        return call_func

    return set_func


@route('/index.html')
def index():
    with open('./templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    my_stock_info = '哈哈哈哈恍恍惚惚'
    content = re.sub(r'\{%content%\}', my_stock_info, content)
    return content


@route('/center.html')
def center():
    with open('./templates/center.html', 'r', encoding='utf-8') as f:
        content = f.read()
    my_stock_info = '没得数据 哈哈哈哈哈哈哈哈哈哈或或或或或或或或或或或或或或或或'
    content = re.sub(r'\{%content%\}', my_stock_info, content)
    return content


def application(env, start_reponse):
    # 传递过来的是web_server_wsgi 中的 set_response_header 方法
    # def set_response_header(self, status, headers):
    start_reponse('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
    # 从字典中获取文件名
    file_name = env['PATH_INFO']
    try:
        return URL_FUNC_DICT[file_name]()
    except Exception as e:
        return '产生了异常%s' % str(e)
