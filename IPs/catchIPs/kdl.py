# _*_ coding:utf-8 _*_
import urllib.request
import time
from lxml import etree
import http.cookiejar
import random
from reqInfo import myAgents


def with_handler(url):
    headers = {'User-Agent': myAgents.get_agent()}
    proxy = {'http': ''}
    cookiejar = http.cookiejar.CookieJar()
    proxy_handler = urllib.request.ProxyHandler(proxies=proxy)
    cookies_handler = urllib.request.HTTPCookieProcessor(cookiejar)
    opener = urllib.request.build_opener(cookies_handler, proxy_handler)
    req = urllib.request.Request(url, headers=headers)
    res = opener.open(req, timeout=6.66)
    return res


def get_ip(text):
    xml_etree = etree.HTML(text)
    _ips = xml_etree.xpath('//*[@data-title="IP"]/text()')
    port = xml_etree.xpath('//*[@data-title="PORT"]/text()')
    form = xml_etree.xpath('//*[@data-title="类型"]/text()')
    res = list(zip(_ips, port, form))
    return res


def collection(url):
    try:
        res = with_handler(url)
        if res.status == 200:
            text = res.read().decode()
            IPdict = {i for i in get_ip(text)}
            return IPdict
    except Exception as e:
        print('kdl链接失败', e)


def catch_pages(minpage=1, maxpage=2178):
    print(time.asctime(), file=open('catchIPs/kdl.txt', 'a', encoding='utf-8'))
    for i in range(minpage, maxpage + 1):
        time.sleep(random.randint(1, 3))
        url = 'https://www.kuaidaili.com/free/inha/{}'.format(i)
        times = 8
        while times:
            co = collection(url)
            if co:
                with open('catchIPs/kdl.txt', 'a', encoding='utf-8') as f:
                    f.write(str(co) + '\n')
                print('kdl 解析成功', url)
                break
            else:
                print('重试', url)
            times -= 1


if __name__ == '__main__':
    catch_pages()
