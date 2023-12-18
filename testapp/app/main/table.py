#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/12 0:56
# @Author  : v_bkaiwang
# @File    : table.py
# @Software: win10 Tensorflow1.13.1 python3.6.3
from flask import url_for
from flask_table import Table


# classes 设置元素class属性字符串列表<table>
class Bstable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-hover']


# allow_sort属性设置为true 所有列默认为尝试将标题转换成排序链接
class PerfTable(Bstable):
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        # 声明一个sort_url方法 给定一个col_key他确定标题连接中的url 如果reverse则表示刚排序完
        # 完全取决于flask视图
        if reverse:
            direction = -1
        else:
            direction = 1
        return url_for('main.feature', feature=self.feature, col_key=col_key, direction=direction)
