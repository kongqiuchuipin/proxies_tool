# _*_ coding:utf-8 _*_
import pymongo
import datetime

client = pymongo.MongoClient()
db = client['MyIPs']
today = datetime.datetime.today()


def collection_count(collection_name):  # 计数
    collection = db[collection_name]
    return collection.count()


def collect(proxies, collection_name):  # 收集
    for proxy in proxies:
        collection = db[collection_name]
        collection.ensure_index('ip')
        existence = collection.find_one({'ip': proxy[0]})
        doc = {'ip': proxy[0],
               'port': proxy[1],
               'form': proxy[2],
               'time': today}
        if collection_name == 'posts' and not existence:  # 所有的ip
            doc['count'] = 0
            collection.insert_one(doc)
        if collection_name == 'tested' and not existence:  # 测试好的且没有数据库记录的
            doc['count'] = 1
            collection.insert_one(doc)
        if collection_name == 'tested' and existence:  # 测试好的且有数据库记录的count+1
            collection.update_one({'ip': proxy[0]}, {'$inc': {'count': 1}})


def del_expire_ip(days=15):  # 过滤掉N天前的无效ip
    collection_posts = db['posts']
    expire = [i['ip'] for i in collection_posts.find({'time': {'$lt': today - datetime.timedelta(days)}})]
    collection_tested = db['tested']
    success = [i['ip'] for i in collection_tested.find()]
    filters = [i for i in expire if i not in success]
    for ip in filters:
        collection_posts.delete_one({'ip': ip})
