# _*_ coding:utf-8 _*_
import scrapy
from ip_tool.items import XiaoMaItem


class XiaoMaSpider(scrapy.Spider):
    name = 'xiaoma'
    # download_delay = 2

    def start_requests(self):
        _url = 'http://www.yun-daili.com/free.asp?stype=1&page={}'
        for i in range(1, 6):
            url = _url.format(i)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        item = XiaoMaItem()
        _ip = response.xpath('//*[@id="list"]/table//tr/td[1]/text()').extract()
        port = response.xpath('//*[@id="list"]/table//tr/td[2]/text()').extract()
        form = [i[:-2] for i in response.xpath('//*[@id="list"]/table//tr/td[4]/text()').extract()]
        res = list(zip(_ip, port, form))
        item['proxy'] = res
        return item


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(XiaoMaSpider)
    process.start()
