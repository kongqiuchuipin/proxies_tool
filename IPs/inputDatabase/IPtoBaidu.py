# _*_ coding:utf-8 _*_
# 尝试用代理连接到百度

import time
import requests
import random
import re
from reqInfo.myAgents import get_agent
import threading
import pymongo

cont = 1


# =============================================================================================== 链接百度
def request_baidu(ip_tup):
    url = 'https://www.baidu.com/'
    proxies = {'https': 'https://' + ip_tup[0] + ':' + ip_tup[1],
               'http': 'http://' + ip_tup[0] + ':' + ip_tup[1]}
    headers = {'User-Agent': get_agent()}
    try:
        time.sleep(random.randint(2, 3))
        with requests.get(url, headers=headers, timeout=6.66, proxies=proxies) as request:
            return request.text
    except Exception as e:
        print('*****', e)


def check(ip_tup):
    text = request_baidu(ip_tup)
    res = set()
    if text:
        pa = re.compile('<title>百度一下，你就知道</title>')  # re匹配
        search = pa.search(text)
        if search:
            with threading.Lock():
                res.add(ip_tup)
                print(ip_tup, 'is useful')
                print(str(ip_tup), file=open('inputDatabase/success.txt', 'a', encoding='utf-8'))  # 输出
    else:
        print('无效：{}'.format(ip_tup))
    return res


def factory(ip_tups):  # 返回有效的代理
    global cont
    res = set()
    for ip_tup in ip_tups:
        c = check(ip_tup)
        with threading.Lock():
            cont += 1
            print(cont)
            if c:
                res.update(c)
    return res


# ========================================================================= 定义thread子类 result
class Mythread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        self.res = None

    def result(self):
        return self.res

    def run(self):
        self.res = self.func(*self.args)


# =================================================================================== 线程
def pro():
    client = pymongo.MongoClient()  # 从数据库导入IP
    db = client['MyIPs']
    collection = db['posts']
    proxies = list({tuple((tup['ip'], tup['port'], tup['form'])) for tup in collection.find()})
    res = set()
    thread = []

    while proxies:  # 线程数=len(ip_tups)/50
        ip_tups, proxies = proxies[:100], proxies[100:]
        t = Mythread(func=factory, args=(ip_tups,))
        thread.append(t)
    for t in thread:
        t.start()
    for t in thread:
        t.join()
        g = t.result()
        if g:
            res.update(t.result())
    return res


# ==================================================================================================
if __name__ == '__main__':
    print(pro())
