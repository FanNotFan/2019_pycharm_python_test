import sys, os
from lxml import etree
import time, random
import re, json
from multiprocessing import Process, Pool, Manager, Queue
import pymysql
from urllib import request, parse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from decimal import Decimal
from bs4 import BeautifulSoup
import html5lib


JDIndex = 'https://www.jd.com/'
JDDetaiBase = 'https://item.jd.com/'
CATEGORY = '面包'
PAGELOADEDMINTIME = 1
PAGELOADEDMAXTIME = 5
QUEUESIEZ = [100, 500]
NUMPOOLS = 2  # 进程数
BRAKER = 2
ON_OFF = 0  # 0表示不使用代理 1表示使用代理
uaPool = [{'User-Agent': 'Opera/8.0 (Windows NT 5.1; U; en)'},
          {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50'},
          {
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201'},
          {
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'},
          {
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'},
          {
              'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko)'},
          {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'},
          {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
          {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
          {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'}]
priceRequestDoc = '''
Host: p.3.cn
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.9
'''
PRICEBASEURL = 'https://p.3.cn/prices/mgets?skuIds=J_'
detailRequestDoc = '''
authority: item.jd.com
method: GET
path: /30132931830.html
scheme: https
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
accept-language: zh-CN,zh;q=0.9
cache-control: max-age=0
upgrade-insecure-requests: 1
'''

'''
    # 建表语句
    CREATE TABLE IF NOT EXISTS `jd_bread`(
	item_id VARCHAR(100) NOT NULL,
	item_fullName VARCHAR(100) NOT NULL,
	item_name VARCHAR(100) NOT NULL,
	item_price VARCHAR(100) NOT NULL,
	item_brand VARCHAR(100) NOT NULL,
	gross_weight VARCHAR(100) NOT NULL,
	item_origin VARCHAR(100) NOT NULL,
	item_certification VARCHAR(100) NOT NULL,
	processing_technology VARCHAR(100) NOT NULL,
	packing_unit VARCHAR(100) NOT NULL,
	is_suger VARCHAR(100) NOT NULL,
	item_taste VARCHAR(100) NOT NULL,
	storage_condition VARCHAR(100) NOT NULL,
	item_classification VARCHAR(100) NOT NULL,
	cookie_classification VARCHAR(100) NOT NULL,
	item_package VARCHAR(100) NOT NULL,
	applicable_people VARCHAR(100) NOT NULL,
	cake_classification VARCHAR(100) NOT NULL,
	item_QGP VARCHAR(100) NOT NULL
    )ENGINE=MyISAM DEFAULT CHARSET=utf8;
'''

class Prophet(Process):

    def __init__(self, func, category, pageQueue, breaker, name='Prophet'):
        super(Prophet, self).__init__()
        self.func = func
        self.category = category
        self.pageQueue = pageQueue
        self.breaker = breaker

    def run(self):
        self.func(self.category, self.pageQueue, self.breaker)


def getReady(category, pageQueue, braker):
    '''
    获取所有页面的商品id，并拼接成详情页的url，封装成map对象，放入队列
    '''
    time.sleep(1)
    options = webdriver.ChromeOptions()

    # 进入index页面
    js1 = "document.documentElement.scrollTop=10000"
    driver = webdriver.Chrome("/Common/Plugins/Chrome_Plugin/WebDrivers/chromedriver", options=options)
    driver.get(JDIndex)
    inputhTag = driver.find_element_by_id('key')
    buttonTag = driver.find_element_by_xpath('//*[@id="search"]/div/div[2]/button')
    inputhTag.send_keys(CATEGORY)
    buttonTag.click()  ###　进入商品列表页面 ###

    ######################### 等待商品列表页加载完全，以待下一步操作 ######################################

    for index in range(2, 101):
        # 获取index,　并点击进入
        time.sleep(PAGELOADEDMINTIME)
        indexTag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="J_bottomPage"]/span[1]/a[%d]' % index)))
        print('index button 已经被加载: ', indexTag)  # 测试index有没有被加载出来
        indexTag.click()

        # 下拉滚动条，让商品列表加载
        time.sleep(PAGELOADEDMAXTIME)
        driver.execute_script(js1)  # 拖动滚动条至底部
        lastImageTag = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="J_goodsList"]/ul/li[60]/div/div[1]/a/img')))

        # 采用正则解析商品id
        html = driver.page_source
        cobj = re.compile('<li class="gl-item.*?" data-sku="([\s\S]*?)"')  # 适合面包
        itemIdList = cobj.findall(html)
        print('获取商品ID合计：', len(itemIdList))
        urlDetailMap = map(lambda x: JDDetaiBase + x + '.html', itemIdList)
        print(urlDetailMap)
        for page in enumerate(urlDetailMap, 1):
            pageQueue.put(page)

        if index == braker:
            break


def parser(pageQueue, uaPool, priceRequestDoc, PRICEBASEURL, detailRequestDoc, open):
    '''
    解析详情页的内容
    '''
    detailUrl = pageQueue.get()[1]
    print(detailUrl)

    # 价格
    PRICEURL = PRICEBASEURL + re.search('\d+', detailUrl).group()
    priceRequestDoc = re.sub(r' ', '', priceRequestDoc)
    headers_for_price = dict(re.findall('([-\w\d]*?):(.*)', priceRequestDoc))
    headers_for_price.update(uaPool[random.randint(0, len(uaPool) - 1)])  # 获取商品价格信息请求的headers信息
    req = request.Request(PRICEURL, headers=headers_for_price)
    resp = open(req)  # 第一次响应
    print(PRICEURL, '商品价格页请求响应码：', resp.getcode())
    if resp.getcode() == 200:
        info = resp.read().decode()
    elif SERVER_ERROR_MIN <= response.status_code < SERVER_ERROR_MAX:
        for i in range(5):
            time.sleep(i ** i)  # 可以继续优化,第一次1秒,第二次10秒,第三次100秒...
            resp = open(req)
            if resp.getcode() == 200:
                break
    elif SERVER_ERROR_MIN <= response.status_code < SERVER_ERROR_MAX:
        if response.status_code == 404:
            print('page not found')
        elif response.status_code == 403:
            print('have no right')
        else:
            pass
    info = json.loads(info)
    item_price = info[0]['p']

    # 名称 品牌 是否含糖 保质期 配料 包装 商品产地...
    detailRequestDoc = re.sub(r' ', '', detailRequestDoc)
    headers_for_detail = dict(re.findall('([-\w\d:]*):(.*)', detailRequestDoc))
    headers_for_detail.update(uaPool[random.randint(0, 9)])  # 获取商品价格信息请求的headers信息
    req = request.Request(detailUrl, headers=headers_for_detail)
    resp = open(req)  # 第二个响应
    print(detailUrl, '详情页请求响应：', resp.getcode())
    if resp.getcode() == 200:
        pass
    elif SERVER_ERROR_MIN <= response.status_code < SERVER_ERROR_MAX:
        for i in range(5):
            time.sleep(i ** i)  # 可以继续优化,第一次1秒,第二次10秒,第三次100秒...
            resp = open(req)
            if resp.getcode() == 200:
                break
    elif SERVER_ERROR_MIN <= response.status_code < SERVER_ERROR_MAX:
        if response.status_code == 404:
            print(detailUrl, 'page not found')
        elif response.status_code == 403:
            print(detailUrl, 'have no right')
        else:
            pass
    parser = etree.HTMLParser(encoding='gbk')
    html = etree.parse(resp, parser=parser)
    print(html)
    elements = html.xpath("//ul[@class='parameter2 p-parameter-list']//text() | //dl[@class='clearfix']//text()")
    detailInfo = list(filter(lambda msg: len(msg.strip()) > 0 and msg, elements))
    detailInfo = ('#').join(detailInfo)
    try:
        item_name = re.search('商品名称：(.*?)#', detailInfo).group(1)
    except AttributeError:
        # print('商品没有 item_name 信息')
        item_name = 'n'
    try:
        item_id = re.search('\d+', detailUrl).group()
    except AttributeError:
        # print('商品没有 item_id 信息')
        item_id = 'n'
    try:
        gross_weight = re.search('商品毛重：(.*?)#', detailInfo).group(1)
    except AttributeError:
        # print('商品没有 gross_weight 信息')
        gross_weight = 'n'
    try:
        item_origin = re.search('商品产地：(.*?)#', detailInfo).group(1)
    except AttributeError:
        # print('商品没有 item_origin 信息')
        item_origin = 'n'
    try:
        item_certification = re.search('资质认证：(.*?)#', detailInfo).group(1)
    except AttributeError:
        # print('商品没有 item_certification 信息')
        item_certification = 'n'
    try:
        processing_technology = re.search('加工工艺：(.*?)#', detailInfo).group(1)
    except AttributeError:
        # print('商品没有 processing_technology 信息')
        processing_technology = 'n'
    try:
        packing_unit = re.search('包装单位：(.*?)#', detailInfo).group(1)
    except AttributeError:
        # print('商品没有 packing_unit 信息')
        packing_unit = 'n'
    try:
        is_suger = re.search('是否含糖：(.*?)#', detailInfo).group(1)
    except AttributeError:
        # print('商品没有 is_suger 信息')
        is_suger = 'n'
    try:
        item_taste = re.search('口味：(.*?)#', detailInfo).group(1)
    except AttributeError:
        # print('商品没有 item_taste 信息')
        item_taste = 'n'
    try:
        storage_condition = re.search('存储条件：(.*?)#', detailInfo).group(1)
    except AttributeError:
        # print('商品没有 storage_condition 信息')
        storage_condition = 'n'
    try:
        item_classification = re.search('分类：(.*?)#', detailInfo).group(1)
    except AttributeError:
        # print('商品没有 item_classification 信息')
        item_classification = 'n'
    try:
        cookie_classification = re.search('饼干分类：(.*?)#', detailInfo).group(1)
    except AttributeError:
        # print('商品没有 cookie_classification 信息')
        cookie_classification = 'n'
    try:
        item_package = re.search('包装：(.*?)#', detailInfo).group(1)
    except AttributeError:
        # print('商品没有 item_package 信息')
        item_package = 'n'
    try:
        applicable_people = re.search('适用人群：(.*?)#', detailInfo).group(1)
    except AttributeError:
        # print('商品没有 applicable_people 信息')
        applicable_people = 'n'
    try:
        cake_classification = re.search('蛋糕糕点分类：(.*?)#', detailInfo).group(1)
    except AttributeError:
        # print('商品没有 cake_classification 信息')
        cake_classification = 'n'
    try:
        item_QGP = re.search("#保质期#(.*?)#", detailInfo).group(1)
    except AttributeError:
        # print('商品没有 item_QGP 信息')
        item_QGP = 'n'

    # 大商品名称
    elementTitle = html.xpath("//title//text()")[0]
    elementTitle = elementTitle.strip()
    item_fullName = re.search('(【.*】)*(.*)?【', elementTitle).group(2)

    # 品牌
    elementBrand = html.xpath("//*[@id='crumb-wrap']/div/div[1]/div[7]/div/div/div[1]/a/text()")
    elementBrand = list(filter(lambda msg: len(msg.strip()) > 0 and msg, elementBrand))
    try:
        item_brand = elementBrand[0]
    except IndexError:
        item_brand = 'npl'
    yield {
        'item_id': item_id,
        'item_fullName': item_fullName,
        'item_name': item_name,
        'item_price': item_price,
        'item_brand': item_brand,
        'gross_weight': gross_weight,
        'item_origin': item_origin,
        'item_certification': item_certification,
        'processing_technology': processing_technology,
        'packing_unit': packing_unit,
        'is_suger': is_suger,
        'item_taste': item_taste,
        'storage_condition': storage_condition,
        'item_classification': item_classification,
        'cookie_classification': cookie_classification,
        'item_package': item_package,
        'applicable_people': applicable_people,
        'cake_classification': cake_classification,
        'item_QGP': item_QGP
    }


def disguiser():
    '''
    构建解析详情页的代理
    '''
    try:
        req = request.Request(
            'http://www.agent.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=8f75fb741de34cfb95adf347910db7a9&orderno=YZ20191169208Yi1jmu&returnType=2&count=1')
        resp = request.urlopen(req)
        jsonIP = resp.read().decode()
        jsonIP = re.sub(' ', '', jsonIP)
        ipList = re.findall('"ip":"(.*?)"', jsonIP)
        portList = re.findall('"port":"(.*?)"', jsonIP)
        value = list(map(lambda x, y: x + ':' + y, ipList, portList))
        key = ['http']
        ipDict = {key[index]: value[index] for index in range(len(key))}
        print(ipDict)
        # 1. 使用ProxyHandler，传入代理构建一个handler
        handler = request.ProxyHandler(ipDict)  # key: http/https val: ip:port
        # 2. 使用上面创建的handler构建一个opener
        opener = request.build_opener(handler)
        print(opener)
    except:
        time.sleep(6)
        req = request.Request(
            'http://www.agent.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=8f75fb741de34cfb95adf347910db7a9&orderno=YZ20191169208Yi1jmu&returnType=2&count=1')
        resp = request.urlopen(req)
        jsonIP = resp.read().decode()
        # jsonIP = '''
        # {"ERRORCODE":"0","RESULT":[{"port":"48234","ip":"115.210.67.213"}]}
        # '''
        jsonIP = re.sub(' ', '', jsonIP)
        ipList = re.findall('"ip":"(.*?)"', jsonIP)
        portList = re.findall('"port":"(.*?)"', jsonIP)
        value = list(map(lambda x, y: x + ':' + y, ipList, portList))
        key = ['http']
        ipDict = {key[index]: value[index] for index in range(len(key))}
        print(ipDict)
        # 1. 使用ProxyHandler，传入代理构建一个handler
        handler = request.ProxyHandler(ipDict)  # key: http/https val: ip:port
        # 2. 使用上面创建的handler构建一个opener
        opener = request.build_opener(handler)
    return opener


def disguiser2():
    '''
    构建selenium的代理
    '''
    req = request.Request(
        'http://www.agent.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=8f75fb741de34cfb95adf347910db7a9&orderno=YZ20191169208Yi1jmu&returnType=2&count=1')
    resp = request.urlopen(req)
    jsonIP = resp.read().decode()
    jsonIP = re.sub(' ', '', jsonIP)
    ipList = re.findall('"ip":"(.*?)"', jsonIP)
    portList = re.findall('"port":"(.*?)"', jsonIP)
    value = list(map(lambda x, y: x + ':' + y, ipList, portList))
    httpIp = value[0]
    return httpIp


def spider(pageQueue, ON_OFF, uaPool, priceRequestDoc, PRICEBASEURL, disguiser, detailRequestDoc, NUMPOOLS, BRAKER):
    '''
    通过队列获取详情页地址
    '''
    print('进程', os.getpid(), '就绪')

    STATUS_CODE = 200
    SERVER_ERROR_MIN = 500
    SERVER_ERROR_MAX = 600
    CLIENT_ERROR_MIN = 400
    CLIENT_ERROR_MAX = 500
    open = ON_OFF and disguiser().open or request.urlopen
    print(open)
    if open is not request.urlopen:
        print('代理就绪')

    for i in range(int(60 * (BRAKER - 1) / NUMPOOLS)):
        # time.sleep(random.uniform(0,5))
        result = parser(pageQueue, uaPool, priceRequestDoc, PRICEBASEURL, detailRequestDoc, open)
        print('队列中剩余：', pageQueue.qsize())
        for i in result:
            print(i)
            # 启用文件系统
            saver(i)


def rescuer(pageQueue, uaPool, priceRequestDoc, PRICEBASEURL, detailRequestDoc, r=5):
    print('队列中剩余：', pageQueue.qsize())
    if pageQueue.qsize() == 0:
        return
    else:
        open = ON_OFF and disguiser().open or request.urlopen
        print('由于代理的不稳定，需要补救者补救,')
        for i in range(pageQueue.qsize()):
            parser(pageQueue, uaPool, priceRequestDoc, PRICEBASEURL, detailRequestDoc, open)
            print('队列中剩余：', pageQueue.qsize())
        if r == 0:
            return
        return rescuer(pageQueue, uaPool, priceRequestDoc, PRICEBASEURL, detailRequestDoc, r - 1)


def saver(result):
    db = pymysql.connect("localhost", "root", "root", "jd", charset="utf8")
    cursor = db.cursor()
    print('准备插入...')
    sql = "INSERT INTO jd.jd_bread (item_id,item_fullName,item_name,item_price,item_brand,gross_weight,item_origin,\
    item_certification,processing_technology,packing_unit,is_suger,item_taste,storage_condition,item_classification,\
    cookie_classification,item_package,applicable_people,cake_classification,item_QGP) VALUES (%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,\
    %r,%r,%r,%r,%r,%r,%r);" % (
    result['item_id'], result['item_fullName'], result['item_name'], result['item_price'], result['item_brand'],
    result['gross_weight'], result['item_origin'], result['item_certification'], result['processing_technology'],
    result['packing_unit'],
    result['is_suger'], result['item_taste'], result['storage_condition'], result['item_classification'],
    result['cookie_classification'],
    result['item_package'], result['applicable_people'], result['cake_classification'], result['item_QGP'])

    cursor.execute(sql)
    db.commit()
    db.close()


def main():
    pageQueue = Manager().Queue(max(QUEUESIEZ))

    prophet = Prophet(getReady, CATEGORY, pageQueue, BRAKER)
    prophet.start()
    # prophet.join()

    pool = Pool(NUMPOOLS)

    for i in range(NUMPOOLS):
        pool.apply_async(func=spider, args=(
        pageQueue, ON_OFF, uaPool, priceRequestDoc, PRICEBASEURL, disguiser, detailRequestDoc, NUMPOOLS, BRAKER))

    pool.close()
    pool.join()

    rescuer(pageQueue, uaPool, priceRequestDoc, PRICEBASEURL, detailRequestDoc)


if __name__ == '__main__':
    main()