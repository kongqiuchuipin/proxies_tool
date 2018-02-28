# _*_ coding:utf-8 _*_
from catchIPs import kdl, xcdl, ydl, gbj, xiaoma, ip66
from inputDatabase import executeDb, IPtoBaidu
import threading


def remove_text():
    import os
    for i in ['catchIPs/xcdl.txt', 'catchIPs/ydl.txt', 'catchIPs/kdl.txt',
              'catchIPs/ip66.txt', 'catchIPs/gbj.txt', 'catchIPs/xiaoma.txt'
              ]:
        try:
            os.remove(i)
        except FileNotFoundError as e:
            print(e)
            continue


def tool():
    spiders = [kdl, xcdl, ydl, xiaoma, ip66]
    threads = []
    for s in spiders:
        t = threading.Thread(target=s.catch_pages, args=(1, 5))  # 参数是页数
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    tool()

    print('采集完成'.center(100, '='))

    executeDb.all_ip_to_database()  # 将所有的IP录入数据库posts中
    print('所有入库'.center(100, '='))

    IPtoBaidu.pro()  # 对所有库中的IP测试，链接百度，链接成功的IP保存到success.txt中
    print('测试完毕'.center(100, '='))

    executeDb.valid_ip_to_database()  # 将tested.txt中的数据保存到数据库tested中，并将数据库tested写入缓存文件lastTested
    print('更新成功'.center(100, '='))

    executeDb.del_expire_ip(15)  # 删除N天以前一次也没有连接成功的IP

    remove_text()  # 删除多余的txt文件
    print('All Done')
