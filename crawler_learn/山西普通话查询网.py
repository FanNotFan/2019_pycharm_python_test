#!/usr/bin/env python
# encoding: utf-8
'''
@author: lennon
@license: (C) Copyright 2019-2020, Node Supply Chain Manager Corporation Limited.
@contact: v-lefan@expedia.com
@software: pycharm
@file: 山西普通话查询网.py
@time: 2019-09-26 15:58
@desc:
'''
import os
import time
import csv
import xlrd
import requests
import xlwings as xw
from bs4 import BeautifulSoup
from ast import literal_eval
import requests
from bs4 import BeautifulSoup
import xlwings as xw
import time
import re
import pymysql

SERVER_URL = 'http://www-x-sxpth-x-cn.img.abc188.com/'
SHEET_NAME = 'Sheet1'

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/xxxxxxxxx Safari/537.36'}

def saveToMysqlMethod():
    connect = pymysql.connect(user='root', password='root', host='localhost', port=3306, db='python', charset='utf8')
    conn = connect.cursor()
    conn.execute("create database if not exists ShanXiPTH character set utf8;")
    conn.execute("use ShanXiPTH;")
    creat_table_sql = """create table if not exists studentInfo (
            id INT PRIMARY KEY AUTO_INCREMENT,
            sname VARCHAR(200),
            sidnumber VARCHAR(200),
            admissionTicketNumber VARCHAR(200),
            room_size VARCHAR(200),
            room_direction VARCHAR(200),
            room_total_floor VARCHAR(200),
            elecator VARCHAR(200),
            room_fixtures VARCHAR(200),
            viliage_name VARCHAR(200),
            raiway_distance VARCHAR(300),
            url VARCHAR(200))"""
    conn.execute('drop table if exists studentInfo;')
    conn.execute(creat_table_sql)

    for i in 400:
        print('正在插入第{}条数据'.format(i))
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
        connect.execute(sql)
        connect.commit()
    connect.close()


def request_download(image_url, sname):
    r = requests.get(image_url)
    with open('./image/'+sname+'.jpg', 'wb') as f:
        f.write(r.content)


def read_excel(excel_file_path: str):
    # 打开文件
    excel = xlrd.open_workbook(excel_file_path)
    # 获取sheet：
    table = excel.sheet_by_name(SHEET_NAME)  # 通过表名获取

    # 获取行数和列数：
    rows = table.nrows  # 获取行数
    cols = table.ncols  # 获取列数
    print("Excel total has {} rows.".format(rows))
    print("Excel total has {} cols.".format(cols))
    # 获取整行或整列内容
    # Row_values = table.row_values(1)  # 获取整行内容
    first_col_values = table.col_values(0)  # 获取整列内容
    del(first_col_values[0])
    for sname in first_col_values:
        sname = sname.strip()
        if sname == '':
            continue
        image_url = SERVER_URL + sname + '.jpg'
        print("image_url = {}".format(image_url))
        request_download(image_url, sname)
        time.sleep(5)


if __name__ == '__main__':
    os.makedirs('./image/', exist_ok=True)
    read_excel("../source/studentInfo.xlsx")
    # result = {'item_id': '5097736', 'item_fullName': '三只松鼠手撕面包饼干蛋糕零食大礼包酵母面包早餐口袋软面包礼盒1000g/盒', 'item_name': '三只松鼠面包', 'item_price': '29.80', 'item_brand': 'npl', 'gross_weight': '1.42kg', 'item_origin': '安徽省合肥市', 'item_certification': '其它', 'processing_technology': '其它', 'packing_unit': '箱装', 'is_suger': '含糖', 'item_taste': '原味', 'storage_condition': '常温', 'item_classification': '面包', 'cookie_classification': '其它', 'item_package': '礼盒装', 'applicable_people': '休闲娱乐', 'cake_classification': '西式糕点', 'item_QGP': '180天'}
    # saveToMysqlMethod(result)