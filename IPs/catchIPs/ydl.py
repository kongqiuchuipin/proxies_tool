# _*_ coding:utf-8 _*_
import time
import random
import requests
from reqInfo import myAgents
from lxml import etree


def get_page(url):
    headers = {'User-Agent': myAgents.get_agent()}
    try:
        req = requests.get(url, headers=headers, timeout=6)
        time.sleep(random.randint(2, 4))
        if req.status_code == 200:
            return req.text
    except Exception as e:
        print('ydl 连接失败', e)


def catch_pages(minpage=1, maxpage=7):
    url = 'http://www.ip3366.net/free/?stype=1'
    print(time.asctime(), file=open('catchIPs/ydl.txt', 'a', encoding='utf-8'))
    for i in range(minpage, maxpage + 1):
        per_url = url + '&page={}'.format(i)
        times = 8
        while times:
            page = get_page(per_url)
            if page:
                html = etree.HTML(page)
                _ip = html.xpath('//*[@id="list"]//tr/td[1]/text()')
                port = html.xpath('//*[@id="list"]//tr/td[2]/text()')
                form = html.xpath('//*[@id="list"]//tr/td[4]/text()')
                res = list(zip(_ip, port, form))
                if res:
                    print('ydl 解析成功', per_url)
                    print(res, file=open('catchIPs/ydl.txt', 'a', encoding='utf-8'))  # 输出文件
                    break
        else:
            print('重试', per_url)
            times -= 1


if __name__ == '__main__':
    catch_pages()
