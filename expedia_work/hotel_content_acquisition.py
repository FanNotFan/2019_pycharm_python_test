#!/usr/bin/env python
# encoding: utf-8
'''
@author: lennon
@license: (C) Copyright 2019-2020, Node Supply Chain Manager Corporation Limited.
@contact: v-lefan@expedia.com
@software: pycharm
@file: hotel_content_acquisition.py
@time: 2019-10-16 18:05
@desc:
'''
import re
import time
import xlrd
import requests
import traceback
import functools
import xlwings as xw
from lxml import etree
from bs4 import BeautifulSoup
from selenium import webdriver

ROWNUMBERGOBAL = 1
# 指定不显示地打开Excel，读取Excel文件
app = xw.App(visible=False, add_book=False)
# SHEET_NAME = 'all_room_source'
SHEET_NAME = 'Sheet7'
# API_URL = 'http://127.0.0.1:5000/'
# API_URL = 'http://10.184.144.12:48080/'
API_URL = 'http://10.184.146.22:48080/'
# Webdriver server url
WEBDRIVER_SERVER_URL = "http://10.184.144.20:4444/wd/hub"
SIMILARITY_THRESHOLD = 4
CONTENT_PARTICIPLE_PATTERN = re.compile('[A-Z][^A-Z\s]+(?:\s+\S[^A-Z\s]*)*')
RE_TITLE = re.compile(r'<!DOCTYPE html>', re.S)
RE_HEAD = re.compile(r'<head>(.*?)</head>', re.S)
RE_HEAD_01 = re.compile(r'<header(.*?)>(.*?)</header>', re.S)
RE_FOOTER = re.compile(r'<footer(.*?)>(.*?)</footer>', re.S)
RE_SCRIPT_01 = re.compile(r'<script>(.*?)</script>', re.S)  # Script
RE_SCRIPT = re.compile(r'<script .*?>(.*?)</script>', re.S)  # Script
RE_STYLE_01 = re.compile(r'<style>(.*?)</style>', re.S)
RE_STYLE = re.compile(r'<style .*?>(.*?)</style>', re.S)  # style
RE_SVG = re.compile(r'<svg .*?>(.*?)</svg>', re.S)  # svg
RE_SYMBOL = re.compile(r'<symbol .*?>(.*?)</symbol>', re.S)  # symbol
RE_LINK = re.compile(r'<link .*?>', re.S)  # link
RE_IMG = re.compile(r'<img .*?>', re.S)  # style
RE_PRICE_DIV = re.compile(r'<td class="h-price">(.*?)</td>', re.S)  # style
RE_DIALOG_DIV = re.compile(r'<div class="uitk-dialog-content-wrapper">(.*?)</div>', re.S)
RE_SECTION_DIV = re.compile(r'<section id="amenities" .*?>(.*?)</section>')
RE_WWW_AGODA_COM = re.compile(r'<div class="Review" .*?>(.*?)</div>')


def print_method_execute_time(arg):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            if arg and isinstance(arg, str):
                print('Decorator Pass Parameters：%s' % arg)
            # print('start execute')
            start_time = time.time()
            res = func(*args, **kw)
            # print('end execute')
            end_time = time.time()
            print("[Method Name: "+func.__name__+'] takes %ss' % int(end_time - start_time))
            return res
        return wrapper
    if callable(arg):
        return decorator(arg)
    return decorator


def create_excel():
    # 创建Excel文件，并命名标题行
    wb = xw.Book()
    sht = wb.sheets[0]
    sht.range('A1').value = 'URL'
    sht.range('B1').value = 'Theme'
    sht.range('C1').value = 'Content'
    return wb


def chrome_webdriver(target_website_url):
    def init_remote_browser():
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        options.add_experimental_option('excludeSwitches', ['enable-automation', "ignore-certificate-errors"])
        browser = webdriver.Remote(command_executor=WEBDRIVER_SERVER_URL,
                                   desired_capabilities=webdriver.DesiredCapabilities.CHROME, options=options)
        return browser

    try:
        target_website_url = target_website_url.strip()
        # Convenient test
        WAIT_WEBSITE_DELAY_TIME = 8
        browser = init_remote_browser()

        browser.get(target_website_url)
        time.sleep(WAIT_WEBSITE_DELAY_TIME)

        try:
            # 切换 iframe 框架
            browser.switch_to.frame("TPASection_isylgktbiframe")
            room_size = browser.find_element_by_tag_name("abbr").text
            page_content = browser.page_source
            browser.switch_to.default_content()
        except Exception as e:
            if "TPASection_isylgktbiframe" in str(e):
                page_content = browser.page_source

        browser.close()
        return page_content
    except Exception as e:
        traceback.print_exc()


def get_content_phantom_webdriver(url):
    return chrome_webdriver(url)


def get_request_content(url):
    # html = get_target_html_text(url)
    html = get_content_phantom_webdriver(url)
    if html is None:
        raise Exception("can't access website")
    html = html.replace("\n", " ")
    html = html.replace("\t", "")
    html = html.replace('&', '&amp;')
    html = html.replace('readonly', '')

    html = RE_TITLE.sub("", html)

    html = RE_HEAD.sub('', html)  # remove header
    html = RE_HEAD_01.sub('', html)

    html = RE_FOOTER.sub('', html)  # remove footer

    html = RE_SCRIPT.sub('', html)  # remove SCRIPT
    html = RE_SCRIPT_01.sub('', html)

    html = RE_STYLE.sub('', html)  # remove style
    html = RE_STYLE_01.sub('', html)

    html = RE_IMG.sub('', html)  # remove img

    html = RE_SVG.sub('', html)

    html = RE_SYMBOL.sub('', html)

    html = RE_LINK.sub('', html)

    html = RE_PRICE_DIV.sub('', html)

    html = RE_DIALOG_DIV.sub('', html)

    html = RE_SECTION_DIV.sub('', html)

    html = RE_WWW_AGODA_COM.sub('', html)
    global XPATH_HETREE
    XPATH_HETREE = etree.HTML(html)

    tree = etree.ElementTree(XPATH_HETREE)

    all_xpath_list = list()
    for e in XPATH_HETREE.iter():
        # print(tree.getpath(e))
        all_xpath_list.append(tree.getpath(e))
    return all_xpath_list


def common_content_extract(page_content: str):
    page_content = page_content.replace('\n', ' ').replace('\t', ' ').replace("&nbsp;", ' ').replace("&ndash;", ' ')
    page_content = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", " ", page_content)
    # pattern = "(?<![A-Z])[A-Z]{1}"
    # new_string = re.sub(pattern, lambda x: " " + x.group(0), page_content)
    # new_string = " ".join(new_string.split())
    # return new_string
    page_content = ' '.join(page_content.split())
    return page_content


def get_crawler_result(crawler_url, rowNumber):
    if crawler_url == '':
        raise Exception('empty parameter error')
    all_xpath_list = get_request_content(crawler_url)
    if all_xpath_list is None or len(all_xpath_list) == '':
        raise Exception("can't find any hotel")
    remove_label_content = common_content_extract(XPATH_HETREE.xpath("/html/body")[0].xpath('string(.)'))
    theme = ''
    global ROWNUMBERGOBAL
    if remove_label_content != '':
        print("rowNumber:{}".format(rowNumber))
        rowNumber += 1
        xw.Range((rowNumber, 1)).value = crawler_url
        xw.Range((rowNumber, 2)).value = theme
        xw.Range((rowNumber, 3)).value = remove_label_content
    else:
        print("content is null {}".format(crawler_url))
        rowNumber += 1
        xw.Range((rowNumber, 1)).value = crawler_url
        xw.Range((rowNumber, 2)).value = remove_label_content
        xw.Range((rowNumber, 3)).value = ''
        ROWNUMBERGOBAL = rowNumber


@print_method_execute_time
def read_excel(excel_file_path: str):
    # 打开文件
    excel = xlrd.open_workbook(excel_file_path)
    # 获取sheet：
    # table = excel.sheets()[0]   # 通过索引顺序获取
    # table = excel.sheet_by_index(0)     # 通过索引顺序获取
    table = excel.sheet_by_name(SHEET_NAME)  # 通过表名获取

    # 获取行数和列数：
    rows = table.nrows  # 获取行数
    cols = table.ncols  # 获取列数
    print("Excel total has {} rows.".format(rows))
    print("Excel total has {} cols.".format(cols))
    # 获取整行或整列内容
    # Row_values = table.row_values(1)  # 获取整行内容
    wb = create_excel()
    first_col_values = table.col_values(0)  # 获取整列内容
    del (first_col_values[0])
    counter = 0
    for item in first_col_values:
        counter += 1
        if item == '' or item.strip() == '':
            continue
        print("The {0} URL is {1}".format(counter, item))
        get_crawler_result(item, ROWNUMBERGOBAL)
        time.sleep(2)
    wb.save('../source/result_' + time.strftime('%Y%m%d%H', time.localtime(time.time())) + '.xlsx')
    # wb.close()
    app.quit()


if __name__ == '__main__':
    try:
        # read_csv("../source/firstRooms.csv", 0)
        read_excel("../source/2019-9-20all_url.xlsx")
        # read_csv("../source/full_result_300357318.csv", 2)
    except Exception as e:
        print(str(e))
