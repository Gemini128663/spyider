import tkinter as tk
import sys
import threading
import os

from tkinter.filedialog import askdirectory
from tkinter import ttk
from sougou_spider1 import getsougou
from bing_spider1 import getbing
from baidu_spider1 import baidu

root = tk.Tk()


class abc:
    def __init__(self, root):
        self.root = root

    def setting(self):
        self.root.title("图片采集系统")
        self.root.minsize("600", '400')
        self.root.maxsize('600', '400')

        self.path = tk.StringVar()  # 文件夹选择
        self.path.set(os.path.abspath("."))  # 默认设置为当前路径
        self.label = tk.Label(text=" 保存路径:  ").place(x=10, y=180)
        self.label1 = tk.Button(self.root, text="选择文件夹", command=self.choise).place(x=460, y=175)
        self.os_entry = tk.Entry(self.root, textvariable=self.path,
                                 width=50)  # state参数为是否锁定entry,state="readonly",# textvariable参数为框里是否可见
        self.os_entry.place(x=100, y=180)

        self.lb = tk.Listbox(self.root)  # 滚动listbox里面内容，滚动条跟着移动
        self.sb = tk.Scrollbar(self.root)  # 创建Scrollbar组件，滚动条组件
        self.sb.pack(side='right', fill='y')  # 右对齐，填满整个y轴
        self.lb.pack(side='bottom', fill=tk.BOTH, ipady=8)
        self.sb.config(command=self.lb.yview)  # 移动滚动条，与内容相关联
        self.lb.config(yscrollcommand=self.sb.set)

        self.label2 = tk.Label(text="关键词:").place(x=200, y=40)  # 创建标签
        self.tips = tk.Label(text="Tips:爬取的图片已经默认保存在D:\\spider_photos").place(x=150, y=140)
        self.number = tk.Label(text="爬取的图片数量：").place(x=150, y=70)
        self.number_entry = tk.Entry()  # 爬取数量的输入框
        self.number_entry.place(x=250, y=70)  # 位置

        self.comboxlist = ttk.Combobox(self.root, width=17)  # 初始化,创建一个下拉列表, textvariable=number
        self.comboxlist.set("壁纸")
        self.comboxlist["values"] = (' 壁纸', '大笑', '微笑', "无表情")  # 下拉列表选项
        self.comboxlist.place(x=250, y=40)  # 下拉列表位置

        self.var = tk.StringVar()  # 定义一个var用来将radiobutton的值和Label的值联系在一起.
        # 创建三个radiobutton选项，其中variable=var, value='sougou'的意思就是，当我们鼠标选中了其中一个选项，把value的值放到变量var中，然后赋值给variable
        self.r1 = tk.Radiobutton(self.root, text='sougou', variable=self.var, value='sougou')  # 复选框sougou
        self.r1.place(x=100, y=10)
        self.r1.select()
        self.r2 = tk.Radiobutton(self.root, text='bing', variable=self.var, value='bing').place(x=250, y=10)  # 复选框bing
        self.r3 = tk.Radiobutton(self.root, text='baidu', variable=self.var, value='baidu').place(x=400,
                                                                                                  y=10)  # 复选框baidu

        self.button = tk.Button(text="开始爬取", command=lambda: self.thread_it(self.spider), state=tk.ACTIVE).place(x=200,
                                                                                                                 y=100)  # 创建按钮，
        self.button1 = tk.Button(text="结束爬取", command=self.end).place(x=350, y=100)  # 创建按钮，

    def end(self):
        sys.exit()

    def spider(self):
        """API"""
        keyword = self.comboxlist.get()  # 获取关键词输入框内的字符串
        number = self.number_entry.get()  # 获取数量
        path = self.path.get()  # 保存路径，暂时没写
        print(path)
        if self.var.get() == "sougou":  # 获取单选的
            getsougou(self.lb, keyword, number, path)
            # self.lb.insert('end',time)
        elif self.var.get() == 'bing':
            getbing(self.lb, keyword, number)

        else:
            baidu(self.lb, keyword, number)

    def thread_it(self, func, *args):  # 传入函数名和参数
        # 创建线程
        t = threading.Thread(target=func, args=args)
        # 守护线程
        t.setDaemon(True)
        # 启动
        t.start()

    def choise(self):
        """图片保存文件夹函数"""
        path_ = askdirectory()  # 使用askdirectory()方法返回文件夹的路径

        if path_ == "":
            self.path.get()  # 当打开文件路径选择框后点击"取消" 输入框会清空路径，所以使用get()方法再获取一次路径
        else:
            self.path_ = path_.replace("/", "\\")  # 实际在代码中执行的路径为“\“ 所以替换一下
            self.path.set(self.path_)

            # print(self.os_entry.get())
        return path_


gui = abc(root)
gui.setting()
tk.mainloop()
