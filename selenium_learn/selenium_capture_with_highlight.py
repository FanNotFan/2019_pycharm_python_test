#!/usr/bin/env python
# encoding: utf-8
'''
@author: lennon
@license: (C) Copyright 2019-2020, Node Supply Chain Manager Corporation Limited.
@contact: v-lefan@expedia.com
@software: pycharm
@file: selenium_capture_with_highlight.py
@time: 2019-06-25 14:28
@desc: http://www.xuepython.wang/Experience/post/67.html
'''

from selenium import webdriver
import time
import sys
import re
from PIL import Image
from io import BytesIO

DEBUG_MODE = True

with open("jquery-3.4.1.min.js") as jquery_file:
    JQUERY_SCRIPT = jquery_file.read()


def log(msg):
    if DEBUG_MODE:
        print(msg)


def capture_with_highlight(url, save_fn="capture.png", keywords=None):
    def init_browser():
        browser = webdriver.PhantomJS("/Users/hiCore/Software/WebDrivers/phantomjs")
        browser.set_window_size(1400, 900)
        browser.set_page_load_timeout(40)
        browser.set_script_timeout(40)
        return browser
    browser=init_browser()
    log("正在打开页面:"+url)
    browser.get(url)  # Load page
    log("执行滚动脚本")
    browser.execute_script("""
        var y = 0;
        var step = 100;
        window.scroll(0, 0);

        function f() {
            if (y < document.body.scrollHeight) {
            y += step;
            window.scroll(0, y);
            setTimeout(f, 100);
            } else {
            window.scroll(0, 0);
            document.title += "scroll-done";
            }
        }
        setTimeout(f, 1000);
    """)

    for i in range(30):
        if "scroll-done" in browser.title:
            break
        time.sleep(1)

    log("滚动完成，判定关键词命中并添加高亮")
    if keywords:
        reg = "(" + ")|(".join(keywords) + ")"

        def loading_jquery(browser):
            has_jq = browser.execute_script(
                """return typeof(jQuery)!="undefined" """)
            if not has_jq:
                log("加载jquery脚本")
                browser.execute_script(JQUERY_SCRIPT)

        loading_jquery(browser)
        has_hit = browser.execute_script(
            """return $('body')&&/%s/.test($('body').text())""" % reg)
        if not has_hit:
            log("未在页面上找到关键词")
            browser.close()
            return False
        browser.execute_script("""
            var addHighlight=function(){
                var re=RegExp("%s")
                var hits = jQuery('body').find("*")
                                    .filter(function () {
                                        var obj = jQuery(this).clone();
                                        obj.find(':nth-child(n)').remove();
                                        return re.test(obj.text()); 
                                    })
                re.global = true
                hits.each(function () {
                    var html = jQuery(this).html()
                    html = html.replace(re, "<span style='color:yellow;font-size:1.5em;background-color:red;font-weight:bold'>%s</span>")
                    jQuery(this).html(html)
                });
            }
            addHighlight()
            """ % (reg, "".join(["$%s" % (i + 1) for i in range(len(keywords))])))
    png_data = browser.get_screenshot_as_png()
    img = Image.open(BytesIO(png_data))
    background = Image.new("RGB", img.size, (255, 255, 255))
    background.paste(img, mask=img.split()[3])
    background.save("img/"+save_fn, 'JPEG', quality=80)
    return True


if __name__ == "__main__":
    capture_with_highlight(
        "https://www.warwickhotels.com/warwick-seattle/rooms", keywords=["Executive", "Room", "sq m"])