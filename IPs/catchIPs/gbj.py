# _*_ coding:utf-8 _*_
import time
import random
import urllib.request
from reqInfo import myAgents
from lxml import etree


def get_page(url):
    headers = {'User-Agent': myAgents.get_agent()}
    req = urllib.request.Request(url, headers=headers)
    time.sleep(random.randint(2, 4))
    try:
        res = urllib.request.urlopen(req, timeout=6)
        if res.status == 200:
            return res.read().decode()
    except Exception as e:
        print('xcdl 连接失败', e)


def catch_pages(minpage=1, maxpage=3000):
    url = 'http://www.xicidaili.com/nn'
    print(time.asctime(), file=open('catchIPs/xcdl.txt', 'a', encoding='utf-8'))
    for i in range(minpage, maxpage + 1):
        per_url = url + '/{}'.format(i)
        times = 8
        while times:
            page = get_page(per_url)
            if page:
                html = etree.HTML(page)
                _ip = html.xpath('//*[@id="ip_list"]//tr/td[2]/text()')
                port = html.xpath('//*[@id="ip_list"]//tr/td[3]/text()')
                form = html.xpath('//*[@id="ip_list"]//tr/td[6]/text()')
                res = list(zip(_ip, port, form))
                if res:
                    print('xcdl 解析成功', per_url)
                    print(res, file=open('catchIPs/xcdl.txt', 'a', encoding='utf-8'))  # 输出文件
                    break
            else:
                print('重试', per_url)
                # times -= 1


if __name__ == '__main__':
    catch_pages(780)
