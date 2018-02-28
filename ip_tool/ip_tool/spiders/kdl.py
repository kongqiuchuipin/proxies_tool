# _*_ coding:utf-8 _*_
import scrapy
from ip_tool.items import KdlItem


class KdlSpider(scrapy.Spider):
    name = 'kdl'
    download_delay = 2

    def start_requests(self):
        _url = 'https://www.kuaidaili.com/free/inha/{}'
        for i in range(1, 6):
            url = _url.format(i)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        item = KdlItem()
        _ip = response.xpath('//*[@data-title="IP"]/text()').extract()
        port = response.xpath('//*[@data-title="PORT"]/text()').extract()
        form = response.xpath('//*[@data-title="类型"]/text()').extract()
        res = list(zip(_ip, port, form))
        item['proxy'] = res
        return item


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(KdlSpider)
    process.start()
