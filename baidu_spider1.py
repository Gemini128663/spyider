import requests
import urllib.request
import os

from urllib.parse import quote
from queue import Queue
from threading import Thread
from datetime import *
import time

def baidu(lb, keyword, number):

    list1 = []
    queue = Queue()
    queue1 = Queue()
    queue2 = Queue()

    for i in range(int(number)):
        url = 'https://image.baidu.com/search/index?' + 'tn=resultjson_com&logid=4986985791187363072&ipn=rj&ct=201326592&is=&fp=result&fr=&word=' + quote(
            keyword) + '&cg=wallpaper&queryWord=' + quote(
            keyword) + '&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn=' + str(
            30 * i) + '&rn=30&gsm=3c&1637118225971='.format(
            keyword, keyword, 30 * i)

        queue.put(url)

    for i in range(5):
        thread1 = Thread(target=baidu1, args=(lb, queue, queue1, queue2, keyword,list1))
        thread1.daemon = True
        thread1.start()

    queue.join()


def baidu1(lb, in_q, in_q1, in_q2, keyword,list1):
    start = datetime.now()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        'Referer': 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fr=&sf=1&fmq=1526269427171_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=' + quote(
            keyword)}
    path = 'D:\\spider_photos\\baidu\\' + keyword + "\\"

    isExists = os.path.exists(path)
    if not isExists:
        try:
            os.makedirs(path)
            lb.insert('end', '创建文件目录成功,开始下载.')
        except FileExistsError:
            pass

    while in_q.empty() is not True:

        #try:
        res = requests.get(url=in_q.get(), headers=headers, timeout=5).json()
        print(in_q.qsize())
        #except Exception as e:
            #print("异常信息e：{}".format(e))

        for img_number in range(0, len(res['data']) - 1):
            img_url = res['data'][img_number]['middleURL']
            img_name = path + res['data'][img_number]['cs']+'.jpg'


            in_q1.put(img_url)
            in_q2.put(img_name)
        in_q.task_done()
    print(in_q1.qsize())

    for i in range(3):
        thread2 = Thread(target=baidu2,args=(lb, in_q1, in_q2))
        thread2.daemon = True
        thread2.start()
    in_q1.join()
    in_q2.join()
    end = datetime.now()
    list1.append((end - start).seconds + (end - start).microseconds / 1000000)
    if len(list1) == 5:
        print(len(list1))
        lb.insert('end', "耗时" + "{:.2f}".format(sum(list1) / 5) + '.s')
        print(sum(list1) / 5)
def baidu2(lb,in_q1,in_q2):
    list1 = []
    while in_q1.empty() or in_q2.empty() is not True:

        img_url = in_q1.get()
        name = in_q2.get()

        urllib.request.urlretrieve(img_url, name)
        urllib.request.urlcleanup()
        lb.insert('end', name + '下载完成')

        in_q1.task_done()
        in_q2.task_done()
