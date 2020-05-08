#!/usr/bin/env python
# encoding: utf-8
'''
@author: lennon
@license: (C) Copyright 2019-2020, Node Supply Chain Manager Corporation Limited.
@contact: v-lefan@expedia.com
@software: pycharm
@file: LR_prefill_web_crawler.py
@time: 2019-09-03 17:34
@desc:
'''
import time
import xlrd
import requests
import functools
import xlwings as xw
from bs4 import BeautifulSoup
from ast import literal_eval

ROWNUMBERGOBAL = 1
# 指定不显示地打开Excel，读取Excel文件
app = xw.App(visible=False, add_book=False)
SHEET_NAME = 'Sheet1'
API_URL = 'http://127.0.0.1:5000/'
SAVE_FILE_PATH = '../source/result_' + time.strftime('%Y%m%d', time.localtime(time.time())) + '.xlsx'
# API_URL = 'http://10.184.144.12:48080/'

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
    sht.range('B1').value = 'Xpath'
    sht.range('C1').value = 'Completeness'
    sht.range('D1').value = 'ActualCompleteness'
    sht.range('E1').value = 'Purity'
    sht.range('F1').value = 'CompletenessGain'
    sht.range('G1').value = 'NumberOfRooms'
    sht.range('H1').value = 'RoomClass'
    sht.range('I1').value = 'RoomType'
    sht.range('J1').value = 'RoomSize'
    sht.range('K1').value = 'BedType'
    sht.range('L1').value = 'Wheelchair'
    sht.range('M1').value = 'Smoking'
    sht.range('N1').value = 'View'
    sht.range('O1').value = 'ExtraAttributes'
    sht.range('P1').value = 'Score'
    sht.range('Q1').value = 'Admitted'
    return wb


def access_api(target_url: str):
    post_data = {'roomid': target_url}
    res = requests.post(API_URL, data=post_data)
    bsobj = BeautifulSoup(res.text, 'lxml')
    return bsobj

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
    for item in first_col_values:
        if item == '' or item.strip() == '':
            continue
        print("URL = {}".format(item))
        bsobj = access_api(item)
        content_parse_logic_regression(bsobj, item, ROWNUMBERGOBAL)
        time.sleep(5)
    wb.save(SAVE_FILE_PATH)
    # wb.close()
    app.quit()


def content_parse_logic_regression(bsobj, target_url, rowNumber):
    input_numberofroomtype_value = bsobj.find('input', attrs={'id': 'numberOfRoomType_id'})['value']
    train_result_dict_id_value = bsobj.find('input', attrs={'id': 'satisfactorily_xpath_dict_id'})['value']
    print(train_result_dict_id_value)
    global ROWNUMBERGOBAL
    if train_result_dict_id_value != '' and input_numberofroomtype_value != '0':
        train_result_dict = literal_eval(train_result_dict_id_value)
        print("rowNumber:{}".format(rowNumber))
        for item in train_result_dict.values():
            # print(item)
            rowNumber += 1
            xw.Range((rowNumber, 1)).value = target_url
            xw.Range((rowNumber, 2)).value = item['xpath']
            xw.Range((rowNumber, 3)).value = item['completeness']
            xw.Range((rowNumber, 4)).value = item['actual_completeness']
            xw.Range((rowNumber, 5)).value = item['purity']
            xw.Range((rowNumber, 6)).value = item['completeness_gain']
            xw.Range((rowNumber, 7)).value = item['number_of_room']
            xw.Range((rowNumber, 8)).value = item['dict_room_attributes']['room_class']
            xw.Range((rowNumber, 9)).value = item['dict_room_attributes']['room_type']
            xw.Range((rowNumber, 10)).value = item['dict_room_attributes']['room_size']
            xw.Range((rowNumber, 11)).value = item['dict_room_attributes']['bed_type']
            xw.Range((rowNumber, 12)).value = item['dict_room_attributes']['wheel_chair_accessible']
            xw.Range((rowNumber, 13)).value = item['dict_room_attributes']['smoking_policy']
            xw.Range((rowNumber, 14)).value = item['dict_room_attributes']['booking_view']
            xw.Range((rowNumber, 15)).value = item['dict_room_attributes']['extra_attributes']
            xw.Range((rowNumber, 16)).value = item['score']
            xw.Range((rowNumber, 17)).value = item['Admitted']
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
        xw.Range((rowNumber, 11)).value = ''
        xw.Range((rowNumber, 12)).value = ''
        xw.Range((rowNumber, 13)).value = ''
        xw.Range((rowNumber, 14)).value = ''
        xw.Range((rowNumber, 15)).value = ''
        xw.Range((rowNumber, 16)).value = ''
        xw.Range((rowNumber, 17)).value = ''
        ROWNUMBERGOBAL = rowNumber


if __name__ == '__main__':
    try:
        # read_csv("../source/firstRooms.csv", 0)
        read_excel("../source/enSupplierWebs0917.xlsx")
        # read_csv("../source/full_result_300357318.csv", 2)
    except Exception as e:
        print(str(e))
