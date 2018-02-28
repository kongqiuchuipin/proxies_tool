# _*_ coding:utf-8 _*_
import time
import random
import requests
from reqInfo import myAgents
from lxml import etree


def get_page(url):
    headers = {'User-Agent': myAgents.get_agent(),
               'Referer': 'http://www.yun-daili.com/free.asp?stype=1&page=1'}
    try:
        req = requests.get(url, headers=headers, timeout=6)
        time.sleep(random.randint(2, 4))
        if req.status_code == 200:
            return req.text
    except Exception as e:
        print('xiaoma 连接失败', e)


def catch_pages(minpage=1, maxpage=6):
    url = 'http://www.yun-daili.com/free.asp?stype=1'
    print(time.asctime(), file=open('catchIPs/xiaoma.txt', 'a', encoding='utf-8'))
    for i in range(minpage, maxpage + 1):
        per_url = url + '&page={}'.format(i)
        times = 8
        while times:
            page = get_page(per_url)
            if page:
                html = etree.HTML(page)
                _ip = html.xpath('//*[@id="list"]/table//tr/td[1]/text()')
                port = html.xpath('//*[@id="list"]/table//tr/td[2]/text()')
                form = [i[:-4] for i in html.xpath('//*[@id="list"]/table//tr/td[4]/text()')]
                res = list(zip(_ip, port, form))
                if res:
                    print('xiaoma 解析成功', per_url)
                    print(res, file=open('catchIPs/xiaoma.txt', 'a', encoding='utf-8'))  # 输出文件
                    break
            else:
                print('重试', per_url)
                times -= 1


if __name__ == '__main__':
    catch_pages()
