#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/4 17:37
# @Author  : v_bkaiwang
# @File    : count.py
# @Software: win10 Tensorflow1.13.1 python3.6.3

import os
import xlrd
import xlwt
from xlutils.copy import copy

"""
需求:
1 .将log数据中循环多次的期望指令集 按照（存在记1/丢失记0）的形式记录 指令集时严格顺序的 最后展示每条指令集的丢包率
2.将记录好的状态数据 写入excel中
实现逻辑:
a.确定变量 设定初始的期望指令集以该指令集于指令集中的索引，每遍历一次，就更新索引指向下一位元素
b.通过判定便利的元素是否为期望指令集，以及当前索引与期望索引大小比较（若当前索引大于期望索引 即指令集丢失反之 当前索引到期望索引
指令均丢失 意味着已经进入下一个指令集）
c.记录状态码，通过字符串添加的形式 记录每个指令状态，就添加到状态码中
d.当状态码满一组指令集长度时，将其记录到结果列表中，并清空状态码重新记录
Excel记录:
先构建展示用的表头信息Excel文件，创建后将数据写入
"""


def count(check_data, expect_data: list):
    """
    在传入的check_data数据中 检查期望集在数据中出现的状态 记录相应的状态码（存在记1/丢失记0）
    :param check_data: 查看文件读出来的数据
    :param expect_data: 期望数据集
    :return: 记录了状态码的数据集
    """
    expect_index = 0
    expect_element = expect_data[expect_index]
    status = ''
    result_data = []
    for element in check_data:
        if element in expect_data:
            current_index = expect_data.index(element)
            if element == expect_element:
                status = status + "1"
                expect_index, expect_element = expect_value(current_index, expect_data)
            else:
                # 当前索引小于期望索引 即期望索引已经丢失 且进入了下一组期望集  故先使用期望索引补全状态码记录一次添加于结果集
                status = status + (len(expect_data) - len(status)) * "0"
                result_data, status = status_record(result_data, status)
                # 使用当前索引再将新一轮的状态码进行拼接
                status = status + "0" * current_index + "1"
                expect_index, expect_element = expect_value(current_index, expect_data)
            if len(status) == len(expect_data):  # 满期望元素长度，便记录一组状态码添加于结果集
                result_data, status = status_record(result_data, status)
    if expect_data != 0:  # 若遍历查看的数据结束后 期望索引不为0 即后续的期望值均丢失
        status += "0" * (len(expect_data) - expect_index)
        result_data.append(status)
    print(f'Result:{result_data}')
    return result_data


def data_get(_file):
    """
    读取数据
    :param _file: path
    :return:所有的数据集

    """
    with open(_file, 'r', encoding="utf-8") as file:
        read_data = file.read()
    data = [line for line in read_data.splitlines()]
    return data


def expect_value(current_index, expect_data):
    """
    更新期望信息 以保证期望数据符合预期的数据顺序
    :param current_index: 当前索引
    :param expect_data: 期望数据
    :return: 期望索引 期望元素
    """
    expect_index = current_index + 1
    expect_index = expect_index % len(expect_data)
    expect_element = expect_data[expect_index]
    return expect_index, expect_element


def status_record(result_data, status):
    """
    记录并清空状态码
    :param result_data: 将状态码添加到结果集
    :param status: 当前状态码
    :return: 添加状态码后的结果集和清空后的状态码变量

    """
    result_data.append(status)
    status = ""
    return result_data, status


def data_deal(result_data, expect_data: list):
    """
    数据展示处理
    :param result_data: 各个指令集状态码集合
    :param expect_data: 期望数据集合
    :return:
    """
    show_data = {}
    for element in result_data:
        for index in range(len(element)):
            if element[index] == "1":
                if expect_data[index] not in show_data:
                    show_data[expect_data[index]] = 1
                else:
                    show_data[expect_data[index]] += 1
    for key, times in show_data.items():
        show_data[key] = "{:.3%}".format(1 - (times / len(result_data)))
    print(show_data)
    return show_data


def excel_create(expect_data, result_data, show_data):
    """
    构建excel表格的表头和样式 并直接将数据写入 生成相应的excel
    :param expect_data: 期望数据
    :param result_data: 结果集
    :param show_data: 展示集
    :return:
    """
    # 创建workbook对象
    excel = xlwt.Workbook(encoding='utf-8')
    # 创建sheet
    sheet = excel.add_sheet(u'PLR', cell_overwrite_ok=True)
    row0 = [u'serial number', u'order address', u'status']
    column0 = [str(number + 1) for number in range(len(result_data))] + ['Packet loss Ratio']
    expect_info = [info for info in expect_data]
    # 写入第一行
    for column in range(len(row0)):
        sheet.write(0, column, row0[column], style_set(color=5))
    # 写入第一列
    row , column = 1, 0
    while row < len(expect_info) * len(column0) and column < len(column0):
        sheet.write_merge(row, row+ len(expect_info)- 1,0,0,column0[column],style_set())
        row+=len(expect_info)
        column += 1
    # 写入第二列
    raw = 0
    while raw < len(expect_info) * len(expect_info):
        for index in range(0, len(expect_info)):
            sheet.write(index+raw+1,1,expect_info[index],style_set())

        raw+=len(expect_info)
    # 写入数据
    data_write(sheet, row0, result_data, expect_info, show_data)
    excel.save("PLR.xls")

