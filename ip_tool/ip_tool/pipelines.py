# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from ip_tool.db_action.collect_ip import collect
from ip_tool.items import ProxiesToBaiduItem, Ip66Item, KdlItem, XcdlItem, XiaoMaItem, YdlItem


class IpToolPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, ProxiesToBaiduItem):
            collect((item['proxy'],), 'tested')
            # with open('success', 'a', encoding='utf-8') as f:
            #     f.write(item['_ip'] + '\n')
        if isinstance(item, (Ip66Item, KdlItem, XcdlItem, XiaoMaItem, YdlItem)):
            collect(item['proxy'], 'posts')
            # with open('newIP', 'a', encoding='utf-8') as f:
            #     f.write(str(item['_ip']) + '\n')
        # return item
