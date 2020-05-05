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
import logging
import urllib.parse

URL_FUNC_DICT = {}


def route(url):
    def set_func(func):
        URL_FUNC_DICT[url] = func

        def call_func(*args, **kwargs):
            return func(*args, *kwargs)

        return call_func

    return set_func


@route(r'/index.html')
def index(ret):
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
            <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s">
        </td>
        </tr>
    """
    for info in stock_info:
        data_content += tr_template % (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[1])
    content = re.sub(r'\{%content%\}', data_content, content)
    return content


@route(r'/center.html')
def center(ret):
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
            <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
        </td>
        <td>
            <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
        </td>
        </tr>
    """
    for info in stock_info:
        data_content += tr_template % (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[0], info[0])
    content = re.sub(r'\{%content%\}', data_content, content)
    return content


@route(r'/add/(\d+)\.html')
def add_focus(ret):
    # 获取股票id
    stock_code = ret.group(1)
    conn = connect(host='localhost', port=3306, user='root', password='123', database='stock_db', charset='utf8')
    cs = conn.cursor()
    # 判断数据库中是否存在该数据
    sql = '''select * from info where code = %s'''
    cs.execute(sql, [stock_code, ])
    if not cs.fetchone():
        cs.close()
        conn.close()
        return '没有鱼丸，没有粉丝'
    # 判断该股票是否是已关注
    sql = '''select * from info as i inner join focus as f on i.id=f.info_id where i.code=%s'''
    cs.execute(sql, [stock_code, ])
    if cs.fetchone():
        cs.close()
        conn.close()
        return '该股票已经关注，请勿重复操作'
    sql = '''insert into focus (info_id) select id from info where code=%s'''
    cs.execute(sql, [stock_code, ])
    conn.commit()
    cs.close()
    conn.close()
    return '关注成功'


@route(r'/del/(\d+)\.html')
def del_focus(ret):
    # 获取股票id
    stock_code = ret.group(1)
    conn = connect(host='localhost', port=3306, user='root', password='123', database='stock_db', charset='utf8')
    cs = conn.cursor()
    # 判断数据库中是否存在该数据
    sql = '''select * from info where code = %s'''
    cs.execute(sql, [stock_code, ])
    if not cs.fetchone():
        cs.close()
        conn.close()
        return '没有鱼丸，没有粉丝'
    # 判断该股票是否是已关注
    sql = '''select * from info as i inner join focus as f on i.id=f.info_id where i.code=%s'''
    cs.execute(sql, [stock_code, ])
    if not cs.fetchone():
        cs.close()
        conn.close()
        return '未关注过该股票，无法取消'
    sql = '''delete from focus where info_id = (select id from info where code=%s)'''
    cs.execute(sql, [stock_code, ])
    conn.commit()
    cs.close()
    conn.close()
    return '成功取消关注'


@route(r'/update/(\d+)\.html')
def show_update_apge(ret):
    # 获取股票id
    stock_code = ret.group(1)
    # 打开update网页
    with open('./templates/update.html', 'r', encoding='utf-8') as f:
        content = f.read()
    conn = connect(host='localhost', port=3306, user='root', password='123', database='stock_db', charset='utf8')
    cs = conn.cursor()
    sql = '''select f.note_info from focus as f inner join info as i on i.id=f.info_id where i.code=%s'''
    cs.execute(sql, [stock_code, ])
    stock_info = cs.fetchone()
    note_info = stock_info[0]
    cs.close()
    conn.close()
    content = re.sub(r"\{%note_info%\}", note_info, content)
    content = re.sub(r"\{%code%\}", stock_code, content)
    return content


@route(r'/update/(\d+)/(.*)\.html')
def save_update(ret):
    # 获取股票id
    stock_code = ret.group(1)
    comment = ret.group(2)
    comment = urllib.parse.unquote(comment)
    conn = connect(host='localhost', port=3306, user='root', password='123', database='stock_db', charset='utf8')
    cs = conn.cursor()
    sql = '''update focus set note_info = %s where info_id = (select id from info where code = %s)'''
    cs.execute(sql, [comment, stock_code])
    conn.commit()
    cs.close()
    conn.close()
    return '修改成功'


def application(env, start_reponse):
    # 传递过来的是web_server_wsgi 中的 set_response_header 方法
    # def set_response_header(self, status, headers):
    start_reponse('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
    # 从字典中获取文件名
    file_name = env['PATH_INFO']
    logging.basicConfig(level=logging.INFO,
                        filename='./log.txt',
                        filemode='a',
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    logging.info("访问的是，%s" % file_name)
    try:
        # 从字典中获取穿过来的url请求数据
        for url, func in URL_FUNC_DICT.items():
            ret = re.match(url, file_name)
            if ret:
                return func(ret)
        else:
            logging.warning('没有对应的函数')
            return '请求的url:%s没有对应的函数' % file_name
    except Exception as e:
        return '产生了异常%s' % str(e)
