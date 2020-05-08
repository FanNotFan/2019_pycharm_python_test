# !/usr/bin/env python
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
from scrapy import Selector
from selenium import webdriver

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


# def get_xpath_selector(url):
#     response = session.get(url, headers=headers)  # session浏览页面
#     response.encoding = "GBK"
#     html = response.text
#     # html = chrome_webdriver(url)
#     selector = Selector(text=html)
#     return selector


def get_crawler_result(selector):
    selectors = selector.xpath("//div[@class='room-info']")
    bcom_result_list = []
    detail_url_list = []
    for index, link in enumerate(selectors):
        url = link.xpath('normalize-space(./a/@href)').extract_first('')
        title = link.xpath('./a/text()').extract()[1].strip() if link.xpath('./a/text()').extract() else ''
        content = link.xpath('normalize-space(./div/ul/li/span/text())').extract_first('')
        detail_url_list.append(url)
        bcom_result = " ".join([title, content])
        bcom_result_list.append(bcom_result)
    return bcom_result_list, detail_url_list


def driver_opt(target_website_url):
    if target_website_url == '' or target_website_url.strip() == '':
        raise Exception('empty parameter error')
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    options.add_experimental_option('excludeSwitches', ['enable-automation', "ignore-certificate-errors"])
    browser = webdriver.Remote(command_executor=WEBDRIVER_SERVER_URL,
                               desired_capabilities=webdriver.DesiredCapabilities.CHROME, options=options)
    browser.get(target_website_url)
    page_sorce_home = browser.page_source
    selector = Selector(text=page_sorce_home)
    bcom_result_list, detail_url_list = get_crawler_result(selector)

    content_list = []
    for item in detail_url_list:
        browser.find_element_by_xpath("//a[@href='"+item+"']").click()
        time.sleep(2)
        page_sorce = browser.page_source
        detail_selector = Selector(text=page_sorce)
        room_size = detail_selector.xpath('//div[@data-room-id="'+item[3:]+'"]/div[@class="hprt-lightbox-right-container"]/text()').extract()[3].strip() if detail_selector.xpath('//div[@data-room-id="'+item[3:]+'"]/div[@class="hprt-lightbox-right-container"]/text()').extract() else ''
        room_view = detail_selector.xpath('normalize-space(//div[@data-room-id="'+item[3:]+'"]//li[@data-name-en="City view"]/text())').extract_first('')
        smoking_policy = detail_selector.xpath('normalize-space(//div[@data-room-id="'+item[3:]+'"]//div[@class="policy-section"]/span/text())').extract_first('')
        args = (room_size, room_view, smoking_policy)
        print('%s %s %s ' % args)
        content_list.append(' '.join([room_size, room_view, smoking_policy]))
        browser.back()
        time.sleep(3)
    browser.close()

    content_all = []
    for content_one, content_two in zip(bcom_result_list, content_list):
        content = ' '.join([content_one, content_two])
        content_all.append('<div>'+content+'</div>')
    return '\n'.join(content_all)


if __name__ == '__main__':
    try:
        url = 'https://www.booking.com/hotel/us/belltown-inn.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaLQCiAEBmAEJuAEYyAEM2AED6AEBiAIBqAIEuALWxd_tBcACAQ;sid=9b9aa76537e3cb36b2bdfc4b29c0a45d;dest_id=20144883;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=4;hpos=4;no_rooms=1;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1572332256;srpvid=890430f00ef00011;type=total;ucfs=1&'
        # url = 'https://www.booking.com/hotel/us/the-westin-seattle.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaLQCiAEBmAEJuAEYyAEM2AED6AEBiAIBqAIEuALWxd_tBcACAQ;sid=9b9aa76537e3cb36b2bdfc4b29c0a45d;dest_id=20144883;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=9;hpos=9;no_rooms=1;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1572332256;srpvid=890430f00ef00011;type=total;ucfs=1&'
        # url = 'https://www.booking.com/hotel/us/laquinta.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaLQCiAEBmAEJuAEYyAEM2AED6AEBiAIBqAIEuALWxd_tBcACAQ;sid=9b9aa76537e3cb36b2bdfc4b29c0a45d;dest_id=20144883;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=6;hpos=6;no_rooms=1;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1572332256;srpvid=890430f00ef00011;type=total;ucfs=1&#hotelTmpl'
        # url = 'https://www.booking.com/hotel/us/warwick-seattle-seattle-washington.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaLQCiAEBmAEJuAEYyAEM2AED6AEBiAIBqAIEuAK1t97tBcACAQ;sid=9b9aa76537e3cb36b2bdfc4b29c0a45d;dest_id=20144883;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=3;hpos=3;no_rooms=1;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1572314048;srpvid=60530d60a1820086;type=total;ucfs=1&#hotelTmpl'
        # url = 'https://www.booking.com/hotel/us/travelodge-by-the-space-needle.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaLQCiAEBmAEJuAEYyAEM2AEB6AEB-AELiAIBqAIEuAKtutntBcACAQ;sid=9b9aa76537e3cb36b2bdfc4b29c0a45d;dest_id=20144883;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=2;hpos=2;no_rooms=1;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1572232504;srpvid=22b116dbb994015d;type=total;ucfs=1&'
        bcom_result_list = driver_opt(url)
        print(bcom_result_list)
    except Exception as e:
        print(str(e))
        traceback.print_exc()
