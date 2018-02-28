# _*_ coding:utf-8 _*_
# 链接到百度, 验证代理
import scrapy
import re
from ip_tool.useragent_and_proxies import myIPs
from ip_tool.items import ProxiesToBaiduItem


class TextToBaidu(scrapy.Spider):
    name = 'proxies_to_baidu'
    custom_settings = {'CONCURRENT_REQUESTS_PER_DOMAIN': 1000,
                       'CONCURRENT_REQUESTS': 2000}

    def start_requests(self):
        _url = 'https://www.baidu.com'  # 测试同一页面 Request中dont_filter=True
        proxies = myIPs.proxy_set()
        while proxies:
            proxy = proxies.pop()
            yield scrapy.Request(
                url=_url, callback=self.parse, dont_filter=True,
                meta={'one_proxy': proxy, 'proxy': proxy[0]+':'+proxy[1]}
            )

    def parse(self, response):
        text = response.text
        item = ProxiesToBaiduItem()
        search = re.search('使用百度前必读', text)
        if search:
            item['proxy'] = response.meta['one_proxy']
            return item
