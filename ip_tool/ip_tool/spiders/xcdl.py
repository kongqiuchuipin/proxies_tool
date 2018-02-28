# _*_ coding:utf-8 _*_
import scrapy
from ip_tool.items import XcdlItem


class XcdlSpider(scrapy.Spider):
    name = 'xcdl'
    download_delay = 2

    def start_requests(self):
        _url = 'http://www.xicidaili.com/nn/{}'
        for i in range(1, 6):
            url = _url.format(i)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        item = XcdlItem()
        _ip = response.xpath('//*[@id="ip_list"]//tr/td[2]/text()').extract()
        port = response.xpath('//*[@id="ip_list"]//tr/td[3]/text()').extract()
        form = response.xpath('//*[@id="ip_list"]//tr/td[6]/text()').extract()
        res = list(zip(_ip, port, form))
        item['proxy'] = res
        return item


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(XcdlSpider)
    process.start()
