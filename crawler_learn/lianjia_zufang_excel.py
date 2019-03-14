# 导入关联库
import requests
from bs4 import BeautifulSoup
import xlwings as xw
import time

# 创建Excel文件，并命名标题行
wb = xw.Book()
sht = wb.sheets[0]
sht.range('A1').value = '房源名称'
sht.range('B1').value = '价格'
sht.range('C1').value = '租赁方式'
sht.range('D1').value = '房屋类型'
sht.range('E1').value = '房屋面积'
sht.range('F1').value = '房屋朝向'
sht.range('G1').value = '发布时间'
sht.range('H1').value = '入住时间'
sht.range('I1').value = '租期'
sht.range('J1').value = '看房'
sht.range('K1').value = '楼层'
sht.range('L1').value = '电梯'
sht.range('M1').value = '车位'
sht.range('N1').value = '用水'
sht.range('O1').value = '用电'
sht.range('P1').value = '燃气'
sht.range('Q1').value = '采暖'
sht.range('R1').value = '地铁'
sht.range('S1').value = '经纪人'
sht.range('T1').value = '联系电话'

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/xxxxxxxxx Safari/537.36'}

# 深圳域
WEBSITE_DOMAIN = 'https://sz.lianjia.com'


# 构造爬取网页链接的函数
def get_html(url, pages):
    res = requests.get(url, headers=header)
    bsobj = BeautifulSoup(res.text, 'lxml')
    urls = bsobj.select('.content__list--item > a')

    location = 2
    for url in urls:
        url = url.get('href')
        if 'apartment' in url:
            continue
        url = (WEBSITE_DOMAIN + '{}').format(url)
        print('crawler url = ' + url)
        get_info(url, location, page=pages)
        location += 1


# 构造爬取详细网页网页信息的函数
def get_info(url, location, page=0):
    res = requests.get(url, headers=header)
    bsobj = BeautifulSoup(res.text, 'lxml')

    # title
    title = bsobj.find('p', {'class': 'content__title'}).get_text().replace(' ', '') if bsobj.find('p', {
        'class': 'content__title'}) is not None else 0
    # 价格
    price = ''
    for child in bsobj.find('p', {'class': 'content__aside--title'}).children:
        price += child.string
    # 租赁方式
    rentalMethod = bsobj.find('p', {'class': 'content__article__table'}).find_all('span')[0].get_text() if bsobj.find(
        'p', {'class': 'content__article__table'}) is not None else 0
    # 房屋类型
    house_type = bsobj.find('p', {'class': 'content__article__table'}).find_all('span')[1].get_text()
    # 房屋面积
    area = bsobj.find('p', {'class': 'content__article__table'}).find_all('span')[2].get_text()
    # 房屋朝向
    houseOrientation = bsobj.find('p', {'class': 'content__article__table'}).find_all('span')[3].get_text()
    # 发布时间
    publishTime = bsobj.find_all('li', {'class': 'fl oneline'})[1].get_text().split('：')[1]
    # 入住时间
    checkInTime = bsobj.find_all('li', {'class': 'fl oneline'})[2].get_text().split('：')[1]
    # 租期
    leasePeriod = bsobj.find_all('li', {'class': 'fl oneline'})[4].get_text().split('：')[1]
    # 看房
    lookHouse = bsobj.find_all('li', {'class': 'fl oneline'})[5].get_text().split('：')[1]
    # 楼层
    floorOfHouse = bsobj.find_all('li', {'class': 'fl oneline'})[7].get_text().split('：')[1]
    # 电梯
    elevator = bsobj.find_all('li', {'class': 'fl oneline'})[8].get_text().split('：')[1]
    # 车位
    parkSpace = bsobj.find_all('li', {'class': 'fl oneline'})[10].get_text().split('：')[1]
    # 用水
    useWater = bsobj.find_all('li', {'class': 'fl oneline'})[11].get_text().split('：')[1]
    # 用电
    electricity = bsobj.find_all('li', {'class': 'fl oneline'})[13].get_text().split('：')[1]
    # 燃气
    gas = bsobj.find_all('li', {'class': 'fl oneline'})[14].get_text().split('：')[1]
    # 采暖
    heating = bsobj.find_all('li', {'class': 'fl oneline'})[16].get_text().split('：')[1]
    # 地铁
    subwayHouse = bsobj.find('i', {'class': 'content__item__tag--is_subway_house'}).get_text().strip()
    # 经纪人
    broker = bsobj.find('p', {'class': 'content__aside__list--subtitle oneline'}).get_text().strip().replace(' ', '')
    # 联系电话
    phone = bsobj.find_all('p', {'class': 'content__aside__list--bottom oneline'})[0].get_text()

    rowNumber = page * 30 + location

    # 存储数据到Excel中
    xw.Range((rowNumber, 1)).value = title
    xw.Range((rowNumber, 2)).value = price
    xw.Range((rowNumber, 3)).value = rentalMethod
    xw.Range((rowNumber, 4)).value = house_type
    xw.Range((rowNumber, 5)).value = area
    xw.Range((rowNumber, 6)).value = houseOrientation
    xw.Range((rowNumber, 7)).value = publishTime
    xw.Range((rowNumber, 8)).value = checkInTime
    xw.Range((rowNumber, 9)).value = leasePeriod
    xw.Range((rowNumber, 10)).value = lookHouse
    xw.Range((rowNumber, 11)).value = floorOfHouse
    xw.Range((rowNumber, 12)).value = elevator
    xw.Range((rowNumber, 13)).value = parkSpace
    xw.Range((rowNumber, 14)).value = useWater
    xw.Range((rowNumber, 15)).value = electricity
    xw.Range((rowNumber, 16)).value = gas
    xw.Range((rowNumber, 17)).value = heating
    xw.Range((rowNumber, 18)).value = subwayHouse
    xw.Range((rowNumber, 19)).value = broker
    xw.Range((rowNumber, 20)).value = phone


# 运行程序
if __name__ == '__main__':
    urls = [WEBSITE_DOMAIN + '/zufang/pg{}'.format(i) for i in range(1, 101)]
    for i, url in enumerate(urls):
        get_html(url, i)
        time.sleep(1)
    wb.save('lianjia_sz_zufang.xlsx')
    wb.close()
