# _*_ coding:utf-8 _*_
# 同时采集多个网站的前五页
# 将采集好的代理连接百度验证有效性
import os
from ip_tool.db_action.collect_ip import collection_count, del_expire_ip

if __name__ == '__main__':
    old = collection_count('posts')
    os.system('scrapy crawlall')
    new = collection_count('posts')
    print('新增{}个'.format(new - old))

    old = collection_count('tested')
    os.system('scrapy crawl proxies_to_baidu')
    new = collection_count('tested')
    print('新增{}个'.format(new - old))

    del_expire_ip()

