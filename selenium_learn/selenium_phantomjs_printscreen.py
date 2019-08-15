#!/usr/bin/env python
# encoding: utf-8
'''
@author: lennon
@license: (C) Copyright 2019-2020, Node Supply Chain Manager Corporation Limited.
@contact: v-lefan@expedia.com
@software: pycharm
@file: selenium_phantomjs_printscreen.py
@time: 2019-06-25 10:43
@desc: https://my.oschina.net/u/2396236/blog/1790714
'''

c = 0
# 网页打开后停留时间，单位是秒
delay = 1

# 从selenium库导入webdirver
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


def init_browser():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36',
        'referer': 'http://google.com'
    }
    # 使用copy()防止修改原代码定义dict
    cap = DesiredCapabilities.PHANTOMJS.copy()

    for key, value in headers.items():
        cap['phantomjs.page.customHeaders.{}'.format(key)] = value

    # 不载入图片，爬页面速度会快很多
    # cap["phantomjs.page.settings.loadImages"] = False

    # 方式二
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # dcap["phantomjs.page.settings.userAgent"] = (
    #     "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
    # )
    # 使用webdirver.PhantomJS()方法新建一个phantomjs的对象，这里会使用到phantomjs.exe，环境变量path中找不到phantomjs.exe，则会报错
    browser = webdriver.PhantomJS(executable_path="/Users/hiCore/Software/WebDrivers/phantomjs",
                                  desired_capabilities=cap)
    # browser = webdriver.PhantomJS(service_log_path="log/" + "capture.png" + ".log")
    # browser.set_window_size(1400, 900)
    # 设置phantomjs浏览器全屏显示
    browser.maximize_window()
    browser.set_page_load_timeout(40)
    browser.set_script_timeout(40)
    return browser


def printscreen(target_url: str):
    browser = init_browser()

    # 使用get()方法，打开指定页面。注意这里是phantomjs是无界面的，所以不会有任何页面显示
    browser.get(target_url)

    time.sleep(delay)

    # 设置phantomjs浏览器全屏显示
    browser.maximize_window()

    # 使用save_screenshot将浏览器正文部分截图，即使正文本分无法一页显示完全，save_screenshot也可以完全截图
    browser.save_screenshot("img/target_website.png")

    browser.close()


if __name__ == '__main__':
    target_url = "https://www.hyatt.com/en-US/hotel/pennsylvania/the-bellevue-hotel/phlph/rooms"
    printscreen(target_url)
