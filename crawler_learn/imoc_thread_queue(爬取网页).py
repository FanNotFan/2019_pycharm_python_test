'''
Python多线程爬虫爬取慕课网+数据可视化显示
教程地址：
    https://mp.weixin.qq.com/s/1JfztEbsYEY-s5weE_x4OA
'''
import requests
import re
import json
import csv
import codecs
from bs4 import BeautifulSoup as bs
from threading import Thread
from queue import Queue
from time import time

# 初始url
start_url = 'https://coding.imooc.com/'

# 增加重试测试
requests.adapters.DEFAULT_RETRIES = 5
session = requests.session()
session.keep_alive = False

# ----------- 全局函数 --------------
def url_open(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    res = session.get(url, headers=headers)
    res.encoding = 'utf-8'
    html = res.text
    return html


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# 判断是否有下一页，有则返回页数，没有就返回None
def is_next(classes_url):
    html = url_open(classes_url)
    soup = bs(html, 'lxml')

    is_pages = soup.select('.page')
    if is_pages:
        pages = []
        # 把当前页第一页加进来
        pages.append(classes_url)
        for each in is_pages[0].contents:
            if is_number(each.get_text()) and each.get_text() != '1':
                pages.append(classes_url + each['href'][6:])
        return pages
    else:
        return None


# 得到要爬的几个大分类【前端开发，后端开发，大数据...】，得到每个分类的url，返回{分类名：url,...}的字典
def get_class(url):
    html = url_open(url)
    soup = bs(html, 'lxml')

    classes = dict()
    all_class = soup.select('.shizhan-header-nav .clearfix a')
    for each_class in all_class[1:]:
        classes[each_class.get_text()] = url + each_class['href']
    return classes


# 得到每个类别页面下的所有课程的名称和链接，存到字典中
def get_page_courses(classes_url):
    courses = dict()
    # 判断是否有下一页
    pages = is_next(classes_url)
    if pages == None:
        html = url_open(classes_url)
        soup = bs(html, 'lxml')
        all_courses = soup.select('.shizhan-course-list .shizhan-course-wrap a')
        for each in all_courses:
            # 获取课程的标题和url
            title = each.select('.shizhan-intro-box .shizan-name')[0].get_text()
            courses[title] = start_url + each['href']
    else:
        for each_page in pages:
            html = url_open(each_page)
            soup = bs(html, 'lxml')
            all_courses = soup.select('.shizhan-course-list .shizhan-course-wrap a')
            for each in all_courses:
                # 获取课程的标题和url
                title = each.select('.shizhan-intro-box .shizan-name')[0].get_text()
                courses[title] = start_url + each['href']
    # print(courses)
    return courses


# -------------- end -------------------#

# 下载器线程，用于下载每个课程的详情页面数据，并把数据传送给数据存储器线程
class DownloadThread(Thread):
    def __init__(self, name, url, class_name, queue):
        Thread.__init__(self)
        self.name = name
        self.url = url
        self.queue = queue
        self.class_name = class_name
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }

    # 下载器,IO操作，多线程适合处理这种操作
    def download(self, url):
        response = session.get(url, headers=self.headers)
        if response.ok:
            # print('ok')
            response.encoding = 'utf-8'
            return response.text

    def run(self):
        print('Donwload  ', self.name)
        # 获得返回的详情页面数据
        data = self.download(self.url)
        # 2 (name, data)
        # q.apend((name, data))
        self.queue.put((self.name, data, self.url, self.class_name))


# 数据存储器，用于对下载器传送过来的页面数据进行处理，提取出想要的信息，存储到本地
class ConvertThread(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    # 从页面数据中提取出信息
    def get_infor(self, data, url):
        soup = bs(data, 'lxml')

        # 级别难度，课程用时，学生人数，评分，价格，讲师
        level = soup.select('.nodistance')[0].get_text()
        time = soup.select('.nodistance')[1].get_text()
        std_num = soup.select('.nodistance')[2].get_text()
        score = soup.select('.nodistance')[3].get_text()
        price = soup.select('.ori-price')[0].get_text()
        # level = soup.select('.info-bar .static-item .meta-value strong')[0].get_text()
        # time = soup.select('.info-bar .static-time .meta-value strong')[0].get_text()
        # std_num = soup.select('.info-bar .statics')[0].select('.meta-value')[2].get_text()
        # score = soup.select('.info-bar .statics')[0].select('.meta-value')[3].get_text()
        # prices = soup.select('.price-box .cur-price b')
        # price = prices[0].get_text() + prices[1].get_text()
        teacher = soup.select('.nickname')[0].get_text()

        informations = {
            '课程级别': level,
            '学习人数': std_num,
            '用时': time,
            '评分': score,
            '价格': price,
            '讲师': teacher
        }
        return informations

    def save_infor_asCSV(self, infor_list):
        json_dict = dict()
        i = 0
        for each in infor_list:
            json_dict.update({i: each})
            i += 1
        f_json = json.dumps(json_dict)
        with open('imooc2.json', 'w') as f:
            f.write(f_json)

    # 存储数据到本地csv文件
    def save_infor(self, infor_list):
        wf = codecs.open('imoocc.csv', 'w', encoding="utf-8")
        writer = csv.writer(wf)

        # 把题头写进文件中
        writer.writerow(
            ['课程名称',
             '课程类别',
             '讲师',
             '课程级别',
             '学习人数',
             '评分',
             '价格',
             '用时',
             '课程链接']
        )

        # 按顺序存到列表中，存入excel
        for each in infor_list:
            row = [
                each['课程名称'],
                each['课程类别'],
                each['讲师'],
                each['课程级别'],
                each['学习人数'],
                each['评分'],
                each['价格'],
                each['用时'],
                each['课程链接']
            ]
            writer.writerow(row)

        print('存储数据完毕！')
        wf.close()

    # 存储器线程启动
    def run(self):
        # 信息列表，存放从下载器传过来的信息
        infor_list = []
        while True:
            name, data, url, class_name = self.queue.get()
            # 当没有数据传来，则结束循环
            if name == -1:
                break
            if data:
                # 从data中得到想要的信息，返回列表
                informations = self.get_infor(data, url)
                # 补充完整字典的信息，如类别，名称，url等
                informations['课程名称'] = name
                informations['课程链接'] = url
                informations['课程类别'] = class_name
                print('Saving  ', name)

                infor_list.append(informations)
        # 将数据写入文件中
        self.save_infor(infor_list)


if __name__ == '__main__':
    start_time = time()
    # 创建用于通信的队列
    q = Queue()

    # 首先得到课程所有的类别的url
    classes = get_class(start_url)

    # 依次遍历每一类别，得到内部所有课的链接
    courses = dict()
    all_threads = []
    for class_name, class_url in classes.items():
        each_course = get_page_courses(class_url)

        # 得到了所有课程的链接，用多线程下载数据
        dTHread = [DownloadThread(name, url, class_name, q) for name, url in each_course.items()]
        # 把每个类别的线程列表存到大列表中，用于后面的线程阻塞等待
        all_threads.append(dTHread)

        for t in dTHread:
            # 线程启动
            t.start()

    # 存储器线程
    cThread = ConvertThread(q)
    cThread.start()

    # 设置线程等待
    for dthread in all_threads:
        for t in dthread:
            t.join()

    # 处理完毕后，给线程发送-1， 通知结束线程
    q.put((-1, None, None, None))
    cThread.join()
    end = time()
    # 爬取结束
    input('爬取完毕,用时%ds' % (end - start_time))