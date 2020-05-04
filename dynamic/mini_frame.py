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
from pymysql import connect

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
    conn = connect(host='localhost', port=3306, user='root', password='123', database='stock_db', charset='utf8')
    cs = conn.cursor()
    cs.execute("select * from info")
    stock_info = cs.fetchall()
    cs.close()
    conn.close()
    data_content = ''
    tr_template = """<tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>
            <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="000007">
        </td>
        </tr>
    """
    for info in stock_info:
        data_content += tr_template % (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7])
    content = re.sub(r'\{%content%\}', data_content, content)
    return content


@route('/center.html')
def center():
    with open('./templates/center.html', 'r', encoding='utf-8') as f:
        content = f.read()
    conn = connect(host='localhost', port=3306, user='root', password='123', database='stock_db', charset='utf8')
    cs = conn.cursor()
    cs.execute(
        "select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info from info as i inner join focus as f on i.id=f.info_id")
    stock_info = cs.fetchall()
    cs.close()
    conn.close()
    data_content = ''
    tr_template = """<tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>
            <a type="button" class="btn btn-default btn-xs" href="/update/300268.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
        </td>
        <td>
            <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="300268">
        </td>
        </tr>
    """
    for info in stock_info:
        data_content += tr_template % (info[0], info[1], info[2], info[3], info[4], info[5], info[6])
    content = re.sub(r'\{%content%\}', data_content, content)
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
