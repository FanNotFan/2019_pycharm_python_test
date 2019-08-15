#!/usr/bin/env python
# encoding: utf-8
'''
@author: lennon
@license: (C) Copyright 2019-2020, Node Supply Chain Manager Corporation Limited.
@contact: v-lefan@expedia.com
@software: pycharm
@file: excel_tool.py
@time: 2019-08-09 14:24
@desc:
'''

import xlwt
import xlrd

# 设置表格样式
def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


# 写Excel
def write_excel():
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('学生', cell_overwrite_ok=True)
    row0 = ["姓名", "年龄", "出生日期", "爱好"]
    colum0 = ["张三", "李四", "恋习Python", "小明", "小红", "无名"]
    # 写第一行
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))
    # 写第一列
    for i in range(0, len(colum0)):
        sheet1.write(i + 1, 0, colum0[i], set_style('Times New Roman', 220, True))

    sheet1.write(1, 3, '2006/12/12')
    sheet1.write_merge(6, 6, 1, 3, '未知')  # 合并行单元格
    sheet1.write_merge(1, 2, 3, 3, '打游戏')  # 合并列单元格
    sheet1.write_merge(4, 5, 3, 3, '打篮球')

    f.save('test.xls')


# https://www.testwo.com/blog/7269
def read_excel(file_path: str):
    # 打开文件
    excel = xlrd.open_workbook(file_path)
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
        print(item)

    pass


if __name__ == '__main__':
    # write_excel()
    read_excel("../source/Rooms_190809.xlsx")
