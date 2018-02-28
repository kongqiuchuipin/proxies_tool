# _*_ coding:utf-8 _*_
import scrapy
from ip_tool.items import YdlItem


class YdlSpider(scrapy.Spider):
    name = 'ydl'
    # download_delay = 2

    def start_requests(self):
        _url = 'http://www.ip3366.net/free/?stype=1&page={}'
        for i in range(1, 6):
            url = _url.format(i)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        item = YdlItem()
        _ip = response.xpath('//*[@id="list"]//tr/td[1]/text()').extract()
        port = response.xpath('//*[@id="list"]//tr/td[2]/text()').extract()
        form = response.xpath('//*[@id="list"]//tr/td[4]/text()').extract()
        res = list(zip(_ip, port, form))
        item['proxy'] = res
        return item


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(YdlSpider)
    process.start()
