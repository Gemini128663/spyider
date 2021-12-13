import urllib.request
import ast
import requests
import os

from datetime import *
from queue import Queue
from urllib.parse import quote
from threading import Thread
from bs4 import BeautifulSoup


def getbing(lb, keyword, number):
    list1 = []
    queue = Queue()  # 网页线程队列
    queue1 = Queue()  # 图片网址线程队列
    queue2 = Queue()  # 图片名字线程队列
    request_queuq = Queue()  # 结束时的队列
    for i in range(int(number)):
        url1 = "https://cn.bing.com/images/async?q=" + quote(keyword) + "&first=" + str(
            i * 35) + "&count=35&cw=1536&ch=254&relp=35&tsc"
        queue.put(url1)
    for i in range(5):
        """使用十个线程来执行run方法消化任务队列，run方法有两个参数，一个任务队列，一个保存结果的队列"""
        thread = Thread(target=getbing1, args=(lb, queue, request_queuq, keyword, queue1, queue2, list1))
        thread.daemon = True  # 守护线程
        thread.start()  # 启动线程

    queue.join()

    print("queue队列结束时大小是" + "{:.2f}".format(queue.qsize()))
    print("result_queue结束时大小是" + "{:.2f}".format(request_queuq.qsize()))


def getbing1(lb, in_q, out_q, keyword, in_q1, in_q2, list1):
    start = datetime.now()

    headers = {"Referer": "Referer: http://desk.zol.com.cn/dongman/1920x1080/",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/95.0.4638.69 Safari/537.36"}
    path = 'D:\\spider_photos\\bing/' + keyword + "/"
    isExists = os.path.exists(path)
    if not isExists:
        try:
            os.makedirs(path)
            lb.insert('end', '创建文件目录成功,开始下载.')
        except FileExistsError:
            pass
    while in_q.empty() is not True:
        resq = requests.get(url=in_q.get(), headers=headers, timeout=5)
        print(in_q.qsize())  # 输出队列大小

        html = resq.text
        soup = BeautifulSoup(html, 'lxml')
        tags = soup.find_all(name='a')
        for tag in tags:
            # print(tag.attrs.get("m"))
            # print(type(tag.attrs.get("m")))
            try:
                md = ast.literal_eval(tag.attrs.get("m")).get("md5")  # ast模块可以将字符串转换成字典，然后查找MD5值
                pathname = path + md + '.jpg'  # 图片路径
                image_url = ast.literal_eval(tag.attrs.get("m")).get("turl")  # 查找图片地址
                in_q1.put(image_url)  # 放入队列
                in_q2.put(pathname)
                """urllib.request.urlretrieve(image_url, pathname)
                urllib.request.urlcleanup()  # 清除urlretrieve()所产生的缓存
                # print(md + "下载完成")
                lb.insert("end", md + "下载完成")"""
                # out_q.put(str(threading.current_thread().getName()) + '-' + str(image_url)) 结束队列
            except:
                pass
        in_q.task_done()

    for i in range(3):
        thread1 = Thread(target=getbing2, args=(lb, in_q1, in_q2))  # target为响应函数，args为函数参数
        thread1.daemon = True
        thread1.start()  # 启动线程
    in_q1.join()  # 和.task_done()方法一起用
    end = datetime.now()
    print(end - start)
    list1.append((end - start).seconds + (end - start).microseconds / 1000000)  # 返回秒和微秒
    if len(list1) == 5:
        '''计算平均时间'''
        print(len(list1))
        lb.insert('end', "耗时" + "{:.2f}".format(sum(list1) / 5) + '.s')
        print(sum(list1) / 5)


def getbing2(lb, in_q1, in_q2):
    while in_q1.empty() or in_q2.empty() is not True:
        '''如果图片网址队列和图片名字线程队列不为空'''
        img_url = in_q1.get()  # 取出一个并删除
        name = in_q2.get()
        try:
            urllib.request.urlretrieve(img_url, name)
            urllib.request.urlcleanup()
            lb.insert('end', name + '下载完成')
        except:
            pass
        in_q1.task_done()  # 和.join()方法一起用，.join()在其前部函数
        in_q2.task_done()
