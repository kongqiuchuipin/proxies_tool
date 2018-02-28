# _*_ coding:utf-8 _*_
# 同时执行多个爬虫
from scrapy.commands import ScrapyCommand


class MyCommand(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of spiders'

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)

    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)

    def run(self, args, opts):
        spider_loader = self.crawler_process.spider_loader
        spider_list = spider_loader.list()
        spider_list.remove('proxies_to_baidu')  # 先移除proxies_to_baidu, 最后单独执行
        for s in spider_list:
            self.crawler_process.crawl(s)
        self.crawler_process.start()

