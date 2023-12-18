#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/12 0:38
# @Author  : v_bkaiwang
# @File    : run.py
# @Software: win10 Tensorflow1.13.1 python3.6.3


body_list = [['RC_TEST', '0', '0', None, '0', None, '0', None],
             [None, None, None, 'RSVD', '31:26', 'RO', '0x0', '0'],
             [None, None, None, 'CMBS', '25', 'RC', '0x0', '0'],
             [None, None, None, 'PMRS', '24', 'RO', '0x0', None],
             [None, None, None, 'MPSMAX', '23:20', 'RC', '0', None],
             ['RC_TESTWQ', '0', '0', None, '31:0', None, '0', None],
             [None, None, None, 'MPSMAX', '0', '0', '0', None]]

titles = ["reg_name", "offset", "io", "rank", "dc", "vs", "g1_"]

# 下面none开头的 都是属于非none开头的子项目，需要吧非none的list转成dict，
# 且新增“sub_data”的key:[] 这个list里装的就是子项目，子项目事先经过zip转成dict

reg_list = list()
rio_list = list()
for i in body_list:
    if i[0] != None:
        reg_list.append(dict(zip(titles, i)))
    else:
        rio_list.append(dict(zip(titles, i)))
# print(rio_list)

body = [{'reg_name': 'RC_TEST', 'offset': '0', 'io': '0', 'rank': None, 'dc': '0', 'vs': None, 'g1_': '0', "sub_data": [
    {'reg_name': None, 'offset': None, 'io': None, 'rank': 'RSVD', 'dc': '31:26', 'vs': 'RO', 'g1_': '0x0'},
    {'reg_name': None, 'offset': None, 'io': None, 'rank': 'CMBS', 'dc': '25', 'vs': 'RC', 'g1_': '0x0'},
    {'reg_name': None, 'offset': None, 'io': None, 'rank': 'PMRS', 'dc': '24', 'vs': 'RO', 'g1_': '0x0'},
    {'reg_name': None, 'offset': None, 'io': None, 'rank': 'MPSMAX', 'dc': '23:20', 'vs': 'RC', 'g1_': '0'}]},

        {'reg_name': 'RC_TESTWQ', 'offset': '0', 'io': '0', 'rank': None, 'dc': '31:0', 'vs': None, 'g1_': '0',
         "sub_data": [

             {'reg_name': None, 'offset': None, 'io': None, 'rank': 'MPSMAX', 'dc': '0', 'vs': '0', 'g1_': '0'}]}]


def test(l1):
    n = len(l1)
    for i in l1:
        for x in range(0, n - i - 1):
            if l1[x] > l1[x + 1]:
                l1[x], l1[x + 1] = l1[x + 1], l1[x]
    return l1




# if __name__ == '__main__':
# t_list = [1, 45, 6, 7, 8, 9, 0, 9, 9, 8, 87, 7, 4, 53, 65, 6, 3, 5, 4, 6, 54]
# v_list = test(l1=t_list)
# q_list = quicksort(t_list)
