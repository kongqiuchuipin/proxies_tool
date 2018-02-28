# _*_ coding:utf-8 _*_

import pymongo
import datetime
import re

client = pymongo.MongoClient()
db = client['MyIPs']
today = datetime.datetime.today()


# ============================================================================================= IP整理到一个文件内
def setIPs():
    pa = re.compile(r"\'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\', \'(\d{,4})\', \'(HTTP|HTTPS|)\'")

    files = ['catchIPs/xcdl.txt', 'catchIPs/ydl.txt', 'catchIPs/kdl.txt',
             'catchIPs/ip66.txt', 'catchIPs/gbj.txt', 'catchIPs/xiaoma.txt'
             ]
    text = ''
    for file in files:
        try:
            with open(file) as f1:
               text += f1.read()
        except FileNotFoundError as e:
            print(e)
            continue
    ips = set(pa.findall(text))
    return ips


# ================================================================================================== IP录入数据库
def all_ip_to_database():
    allIP = setIPs()
    num = 0
    repeat = 0
    collection = db['posts']
    collection.ensure_index('ip')
    while allIP:
        tup = allIP.pop()
        _ip = tup[0]
        port = tup[1]
        form = tup[2]
        fi = collection.find_one({'ip': _ip})  # 去重
        if not fi:
            data = {'ip': _ip,
                    'port': port,
                    'form': form,
                    'count': 0,
                    'time': today}
            collection.insert_one(data)
            num += 1
        elif fi:
            repeat += 1
    print('更新了%s条' % num, '重复%s条' % repeat)


# ===================================================================================================== 有效IP录入数据库
def valid_ip_to_database():
    num = 0
    repeat = 0
    collection = db['tested']
    with open('inputDatabase/success.txt') as file2:
        text = file2.read()
        pa = re.compile(r"\'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\', \'(\d{,4})\', \'(HTTP|HTTPS|)\'")
        sucess_ip_tups = pa.findall(text)
    for ip_tup in sucess_ip_tups:
        _ip = ip_tup[0]
        port = ip_tup[1]
        form = ip_tup[2]
        fi = collection.find_one({'ip': _ip})
        if not fi:
            data = {'ip': _ip,
                    'port': port,
                    'form': form,
                    'count': 1,
                    'time': today}
            collection.insert_one(data)
            num += 1
        elif fi:
            collection.update_one({'ip': _ip}, {'$inc': {'count': 1}})
            repeat += 1
    print('更新了%s条' % num, '重复%s条' % repeat)


# ===================================================================================== 删除N天以前一次也没有连接成功的IP
def del_expire_ip(days=15):
    collection_posts = db['posts']
    expire = [i['ip'] for i in collection_posts.find({'time': {'$lt': today - datetime.timedelta(days)}})]
    collection_tested = db['tested']
    success = [i['ip'] for i in collection_tested.find()]
    filters = [i for i in expire if i not in success]
    for ip in filters:
        collection_posts.delete_one({'ip': ip})


if __name__ == '__main__':
    all_ip_to_database()
    # valid_ip_to_database()