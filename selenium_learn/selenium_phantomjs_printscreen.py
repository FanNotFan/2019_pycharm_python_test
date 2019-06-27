#!/usr/bin/env python
# encoding: utf-8
'''
@author: lennon
@license: (C) Copyright 2019-2020, Node Supply Chain Manager Corporation Limited.
@contact: v-lefan@expedia.com
@software: pycharm
@file: selenium_phantomjs_printscreen.py
@time: 2019-06-25 10:43
@desc:
'''

c = 0
# 网页打开后停留时间，单位是秒
delay = 1

# 从selenium库导入webdirver
from selenium import webdriver
import time


def init_browser():
    # 使用webdirver.PhantomJS()方法新建一个phantomjs的对象，这里会使用到phantomjs.exe，环境变量path中找不到phantomjs.exe，则会报错
    browser = webdriver.PhantomJS("/Users/hiCore/Software/WebDrivers/phantomjs")
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
    target_url = "https://www.expedia.com/"
    printscreen(target_url)