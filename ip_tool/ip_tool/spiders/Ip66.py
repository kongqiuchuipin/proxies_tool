# _*_ coding:utf-8 _*_
import scrapy
from ip_tool.items import Ip66Item


class Ip66Spider(scrapy.Spider):
    name = 'ip66'

    def start_requests(self):
        first_page = 'http://www.66ip.cn/index.html'
        yield scrapy.Request(first_page)
        _url = 'http://www.66ip.cn/{}.html'
        for i in range(2, 6):
            url = _url.format(i)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        item = Ip66Item()
        _ip = response.xpath('//*[@id="main"]/div/div[1]/table//tr/td[1]/text()').extract()
        port = response.xpath('//*[@id="main"]/div/div[1]/table//tr/td[2]/text()').extract()
        form = [''] * len(_ip)
        res = list(zip(_ip, port, form))[1:]
        item['proxy'] = res
        return item


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(Ip66Spider)
    process.start()
