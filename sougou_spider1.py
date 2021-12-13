import requests
import urllib.request
import os
from datetime import *
from queue import Queue
from urllib.parse import quote
from threading import Thread



def getsougou(lb, keyword, number, path):
    list1 = []
    queue = Queue()  # 线程队列
    queue1 = Queue()
    queue2 = Queue()
    request_queuq = Queue()
    for i in range(int(number)):
        url = "https://pic.sogou.com/napi/pc/searchList?mode=13&dm=4&cwidth=1536&cheight=864&start=" + str(
            i * 48) + "&xml_len=48&query=" + quote(keyword)
        queue.put(url)

    for i in range(5):
        """使用十个线程来执行run方法消化任务队列，run方法有两个参数，一个任务队列，一个保存结果的队列"""
        thread = Thread(target=getsougou1, args=(lb, queue, request_queuq, keyword, queue1, queue2, list1))
        thread.daemon = True
        thread.start()
    queue.join()


def getsougou1(lb, in_q, out_q, keyword, in_q1, in_q2, list1):
    start = datetime.now()
    headers = {"Referer": "Referer: http://desk.zol.com.cn/dongman/1920x1080/",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/95.0.4638.69 Safari/537.36"}
    path = 'D:\\spider_photos\\sougou/' + keyword + "/"
    isExists = os.path.exists(path)
    if not isExists:
        try:
            os.makedirs(path)
            lb.insert('end', '创建文件目录成功,开始下载.')
        except FileExistsError:
            pass
    while in_q.empty() is not True:
        imgs = requests.get(url=in_q.get(), headers=headers, timeout=5).json()  # 请求状态码，返回值为200
        print(in_q.qsize())
        for i in imgs['data']['items']:
            # jd = json.loads(imgs.text)  # jd数据类型为字典
            pathname = path + i['name']
            in_q1.put(i['oriPicUrl'])
            in_q2.put(pathname)
            """try:
                urllib.request.urlretrieve(i['oriPicUrl'], pathname)
                urllib.request.urlcleanup()  # 清除urlretrieve()所产生的缓存
                lb.insert('end', i['name']+"下载完成")
                out_q.put(str(threading.current_thread().getName()) + '-' + i['name'])
            except:
                pass"""
        in_q.task_done()

    for i in range(3):
        thread1 = Thread(target=getsougou2, args=(lb, in_q1, in_q2))
        thread1.daemon = True
        thread1.start()

    in_q2.join()
    end = datetime.now()
    print(end - start)
    list1.append((end - start).seconds + (end - start).microseconds / 1000000)
    if len(list1) == 5:
        print(len(list1))
        lb.insert('end', "耗时" + "{:.2f}".format(sum(list1) / 5) + '.s')
        print(sum(list1) / 5)


def getsougou2(lb, in_q1, in_q2):
    while in_q1.empty() or in_q2.empty() is not True:
        img_url = in_q1.get()
        name = in_q2.get()
        try:
            urllib.request.urlretrieve(img_url, name)
            urllib.request.urlcleanup()
            lb.insert('end', name + '下载完成')
        except:
            pass
        in_q1.task_done()
        in_q2.task_done()
