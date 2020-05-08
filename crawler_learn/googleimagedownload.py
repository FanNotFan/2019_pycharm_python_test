# ****本脚本还是存有一些问题的，没有很好解决google的反爬机制以及google的翻页问题
# *******本脚本运行时需要本机安装 Chrome 浏览器以及Chrome的驱动，同时需要selenium库的支撑********
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import urllib.request
from bs4 import BeautifulSoup as bs
import re
import os
import base64

# ****************************************************
base_url_part1 = 'https://www.google.com/search?q='
base_url_part2 = '&source=lnms&tbm=isch'  # base_url_part1以及base_url_part2都是固定不变的，无需更改
search_query = '发票'  # 检索的关键词，可自己输入你想检索的关键字
location_driver = '/Users/hiCore/Software/WebDrivers/chromedriver_81'  # Chrome驱动程序在电脑中的位置


class Crawler:
    def __init__(self):
        self.url = base_url_part1 + search_query + base_url_part2

    # 启动Chrome浏览器驱动
    def start_brower(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-infobars")
        # 启动Chrome浏览器
        driver = webdriver.Chrome(executable_path=location_driver, chrome_options=chrome_options)
        # 最大化窗口，因为每一次爬取只能看到视窗内的图片
        driver.maximize_window()
        # 浏览器打开爬取页面
        driver.get(self.url)
        return driver

    def downloadImg(self, driver):
        t = time.localtime(time.time())
        foldername = str(t.__getattribute__("tm_year")) + "-" + str(t.__getattribute__("tm_mon")) + "-" + \
                     str(t.__getattribute__("tm_mday"))  # 定义文件夹的名字
        picpath = '/Users/hiCore/Downloads/GoogleImage/%s' % (foldername)  # 下载到的本地目录
        # 路径不存在时创建一个
        if not os.path.exists(picpath): os.makedirs(picpath)
        # 下载图片的本地路径 ~/Downloads/GoogleImage/xxx

        # 记录下载过的图片地址，避免重复下载
        img_url_dic = {}
        x = 0
        # 当鼠标的位置小于最后的鼠标位置时,循环执行
        pos = 0
        for i in range(1):  # 此处可自己设置爬取范围
            pos = i * 500  # 每次下滚500
            js = "document.documentElement.scrollTop=%d" % pos
            driver.execute_script(js)
            time.sleep(1)
            # 获取页面源码
            html_page = driver.page_source
            # 利用Beautifulsoup4创建soup对象并进行页面解析
            soup = bs(html_page, "html.parser")
            # 通过soup对象中的findAll函数图像信息提取
            imglist = soup.findAll('img', {'class': 'rg_i'})

            # ??这段代码问题?
            for imgurl in imglist:
                try:
                    print(x, end=' ')
                    if imgurl['src'] not in img_url_dic:
                        target = '{}/{}.jpg'.format(picpath, x)
                        # print ('Downloading image to location: ' + target + '\nurl=' + imgurl['src'])
                        img_url_dic[imgurl['src']] = ''
                        urllib.request.urlretrieve(imgurl['src'], target)
                        time.sleep(1)
                        x += 1
                except KeyError:
                    print("ERROR!")
                    continue

    def run(self):
        print(
            '\t\t\t**************************************\n\t\t\t**\t\tWelcome to Use Spider\t\t**\n\t\t\t**************************************')
        driver = self.start_brower()
        self.downloadImg(driver)
        driver.close()
        print("Download has finished.")


if __name__ == '__main__':
    craw = Crawler()
    craw.run()
