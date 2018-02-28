# _*_ coding:utf-8 _*_
import time
import random
import urllib.request
from reqInfo import myAgents
from lxml import etree


def get_page(url):
    headers = {'User-Agent': myAgents.get_agent(),
               'Host': 'www.66ip.cn',
               'Referer': 'http://www.66ip.cn/4.html'}
    req = urllib.request.Request(url, headers=headers)
    time.sleep(random.randint(1, 3))
    try:
        res = urllib.request.urlopen(req, timeout=5)
        if res.status == 200:
            return res.read().decode('gbk')
    except Exception as e:
        print('ip66 连接失败', e)


def catch_pages(minpage=1, maxpage=1170):
    url = 'http://www.66ip.cn'
    print(time.asctime(), file=open('catchIPs/ip66.txt', 'a', encoding='utf-8'))
    for i in range(minpage, maxpage + 1):
        if i == 1:
            per_url = url + '/index.html'.format(i)
        else:
            per_url = url + '/{}.html'.format(i)
        times = 8
        while times:
            page = get_page(per_url)
            if page:
                html = etree.HTML(page)
                _ip = html.xpath('//*[@id="main"]/div/div[1]/table//tr/td[1]/text()')
                port = html.xpath('//*[@id="main"]/div/div[1]/table//tr/td[2]/text()')
                form = ['']*len(_ip)
                res = list(zip(_ip, port, form))[1:]
                if _ip:
                    print('ip66 解析成功', per_url)
                    print(res)
                    print(res, file=open('catchIPs/ip66.txt', 'a', encoding='utf-8'))  # 输出文件
                    break
            else:
                print('重试', per_url)
                times -= 1


if __name__ == '__main__':
    catch_pages()
