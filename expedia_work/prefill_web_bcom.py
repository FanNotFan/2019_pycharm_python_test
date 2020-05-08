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
import time
import traceback
import functools
import requests
from scrapy import Selector
from selenium import webdriver

# 增加重试测试
requests.adapters.DEFAULT_RETRIES = 5
session = requests.session()
session.keep_alive = False
WEBDRIVER_SERVER_URL = "http://10.184.144.20:4444/wd/hub"
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }


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


def get_xpath_selector(url):
    response = session.get(url, headers=headers)  # session浏览页面
    response.encoding = "GBK"
    html = response.text
    # html = chrome_webdriver(url)
    selector = Selector(text=html)
    return selector


def get_crawler_result(crawler_url):
    if crawler_url == '':
        raise Exception('empty parameter error')
    selector = get_xpath_selector(crawler_url)
    selectors = selector.xpath("//div[@class='room-info']")
    bcom_result_list = []
    for index, link in enumerate(selectors):
        url = link.xpath('normalize-space(./a/@href)').extract_first('')
        title = link.xpath('./a/text()').extract()[1].strip() if link.xpath('./a/text()').extract() else ''
        content = link.xpath('normalize-space(./div/ul/li/span/text())').extract_first('')

        detail_page_source = driver_opt(crawler_url, "//a[@href='"+url+"']")
        detail_selector = Selector(text=detail_page_source)
        room_size = detail_selector.xpath('//div[@class="hprt-lightbox-right-container"]/text()').extract()[3].strip() if detail_selector.xpath('//div[@class="hprt-lightbox-right-container"]/text()').extract() else ''
        room_view = detail_selector.xpath('normalize-space(//li[@data-name-en="City view"]/text())').extract_first('')
        smoking_policy = detail_selector.xpath('normalize-space(//div[@class="policy-section"]/span/text())').extract_first('')
        args = (url, title, content, room_size, room_view, smoking_policy)
        print('%s %s %s %s %s %s' % args)
        bcom_result = " ".join([title, content, room_size, room_view, smoking_policy])
        bcom_result_list.append(bcom_result)
    return bcom_result_list


def driver_opt(target_website_url, click_str):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    options.add_experimental_option('excludeSwitches', ['enable-automation', "ignore-certificate-errors"])
    browser = webdriver.Remote(command_executor=WEBDRIVER_SERVER_URL,
                               desired_capabilities=webdriver.DesiredCapabilities.CHROME, options=options)
    browser.get(target_website_url)

    browser.find_element_by_xpath(click_str).click()
    time.sleep(3)
    page_sorce = browser.page_source
    browser.close()
    return page_sorce


if __name__ == '__main__':
    try:
        url = 'https://www.booking.com/hotel/us/warwick-seattle-seattle-washington.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaLQCiAEBmAEJuAEYyAEM2AED6AEBiAIBqAIEuAK1t97tBcACAQ;sid=9b9aa76537e3cb36b2bdfc4b29c0a45d;dest_id=20144883;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=3;hpos=3;no_rooms=1;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1572314048;srpvid=60530d60a1820086;type=total;ucfs=1&#hotelTmpl'
        # url = 'https://www.booking.com/hotel/us/travelodge-by-the-space-needle.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaLQCiAEBmAEJuAEYyAEM2AEB6AEB-AELiAIBqAIEuAKtutntBcACAQ;sid=9b9aa76537e3cb36b2bdfc4b29c0a45d;dest_id=20144883;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=2;hpos=2;no_rooms=1;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1572232504;srpvid=22b116dbb994015d;type=total;ucfs=1&'
        bcom_result_list = get_crawler_result(url)
        print(bcom_result_list)
    except Exception as e:
        print(str(e))
