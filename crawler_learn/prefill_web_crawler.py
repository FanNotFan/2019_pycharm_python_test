#!/usr/bin/env python
# encoding: utf-8
'''
@author: lennon
@license: (C) Copyright 2019-2020, Node Supply Chain Manager Corporation Limited.
@contact: v-lefan@expedia.com
@software: pycharm
@file: prefill_web_crawler.py
@time: 2019-08-05 17:27
@desc:
'''
import time
import csv
import xlrd
import requests
import xlwings as xw
from bs4 import BeautifulSoup
from ast import literal_eval

ROWNUMBERGOBAL = 1

# API_URL = 'http://127.0.0.1:5000/'
API_URL = 'http://10.184.144.12:48080/'

def create_excel():
    # 创建Excel文件，并命名标题行
    wb = xw.Book()
    sht = wb.sheets[0]
    sht.range('A1').value = 'URL'
    sht.range('B1').value = 'RoomName'
    sht.range('C1').value = 'RoomType'
    sht.range('D1').value = 'RoomClass'
    sht.range('E1').value = 'RoomSize'
    sht.range('F1').value = 'BedType'
    sht.range('G1').value = 'Wheelchair'
    sht.range('H1').value = 'Smoking'
    sht.range('I1').value = 'View'
    sht.range('J1').value = 'ExtraAttributes'
    sht.range('K1').value = 'NumberOfRoomType'
    return wb


def access_api(target_url: str):
    post_data = {'roomid': target_url}
    res = requests.post(API_URL, data=post_data)
    bsobj = BeautifulSoup(res.text, 'lxml')
    return bsobj


def content_parse(bsobj, target_url, rowNumber):
    input_numberofroomtype_value = bsobj.find('input', attrs={'id': 'numberOfRoomType_id'})['value']
    match_content_value = bsobj.find('input', attrs={'id': 'match_content_id'})['value']
    global ROWNUMBERGOBAL
    if match_content_value != '' and input_numberofroomtype_value != '0':
        mlist = literal_eval(match_content_value)
        len_mlist = len(mlist)
        for item in mlist:
            print("rowNumber:{}".format(rowNumber))
            rowNumber += 1
            xw.Range((rowNumber, 1)).value = target_url
            xw.Range((rowNumber, 2)).value = item['room_class']+" "+item['room_type']
            xw.Range((rowNumber, 3)).value = item['room_type']
            xw.Range((rowNumber, 4)).value = item['room_class']
            xw.Range((rowNumber, 5)).value = item['room_size']
            xw.Range((rowNumber, 6)).value = item['bed_type']
            xw.Range((rowNumber, 7)).value = item['wheel_chair_accessible']
            xw.Range((rowNumber, 8)).value = item['smoking_policy']
            xw.Range((rowNumber, 9)).value = item['booking_view']
            xw.Range((rowNumber, 10)).value = item['extra_attributes']
            xw.Range((rowNumber, 11)).value = len_mlist
            time.sleep(2)
        ROWNUMBERGOBAL = rowNumber
    else:
        print("content is null {}".format(target_url))
        rowNumber += 1
        xw.Range((rowNumber, 1)).value = target_url
        xw.Range((rowNumber, 2)).value = ''
        xw.Range((rowNumber, 3)).value = ''
        xw.Range((rowNumber, 4)).value = ''
        xw.Range((rowNumber, 5)).value = ''
        xw.Range((rowNumber, 6)).value = ''
        xw.Range((rowNumber, 7)).value = ''
        xw.Range((rowNumber, 8)).value = ''
        xw.Range((rowNumber, 9)).value = ''
        xw.Range((rowNumber, 10)).value = ''
        xw.Range((rowNumber, 11)).value = 0
        ROWNUMBERGOBAL = rowNumber


def read_csv(file_path: str):
    # 读取csv至字典
    wb = create_excel()
    csvFile = open(file_path, "r", encoding='gb18030')
    reader = csv.reader(csvFile)
    result = {}  # 建立空字典
    for item in reader:
        if reader.line_num == 1:  # 忽略第一行
            continue
        print("URL = {}".format(item[0]))
        bsobj = access_api(item[0])
        content_parse(bsobj, item[0], ROWNUMBERGOBAL)
        time.sleep(5)
    csvFile.close()
    wb.save('result.xlsx')
    wb.close()


def read_excel(excel_file_path: str):
    wb = create_excel()
    # 打开文件
    excel = xlrd.open_workbook(excel_file_path)
    # 获取sheet：
    table = excel.sheet_by_name('Rooms')  # 通过表名获取

    # 获取行数和列数：
    rows = table.nrows  # 获取行数
    cols = table.ncols  # 获取列数
    print("Excel total has {} rows.".format(rows))
    print("Excel total has {} cols.".format(cols))
    # 获取整行或整列内容
    # Row_values = table.row_values(1)  # 获取整行内容
    first_col_values = table.col_values(0)  # 获取整列内容
    del(first_col_values[0])
    for item in first_col_values:
        print("URL = {}".format(item))
        bsobj = access_api(item)
        content_parse(bsobj, item, ROWNUMBERGOBAL)
        time.sleep(5)
    excel.close()
    wb.save('result.xlsx')
    wb.close()


if __name__ == '__main__':
    # read_csv("../source/firstRooms.csv")
    read_excel("../source/Rooms_190809.xlsx")