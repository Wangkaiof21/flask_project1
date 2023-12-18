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
             [None, None, None, 'MPSMAX', '0', '0', '0', None],
             ['RC_TESTWQ', '0', '0', None, '31:0', None, '0', None],
             [None, None, None, 'MPSMAX', '0', '0', '0', None]
             ]

titles = ["reg_name", "offset", "io", "rank", "dc", "vs", "g1_"]

# 下面none开头的 都是属于非none开头的子项目，需要吧非none的list转成dict，
# 且新增“sub_data”的key:[] 这个list里装的就是子项目，子项目事先经过zip转成dict

list_bodys = []
list_body = []
for i in body_list:
    if i[0] != None:
        list_bodys.append(list_body)
        list_body = []
    list_body.append(i)
list_bodys.append(list_body)
list_bodys.pop(0)

body_ = list()
for gp in list_bodys:
    ddd = []
    for i in gp:
        i = dict(zip(titles, i))
        ddd.append(i)
    body_.append(ddd)

gggg = list()
for i in body_:
    gggg.append(i[1:])

xxx = list()
for i in range(len(body_)):
    body_[i][0]["sub_data"] = gggg[i:]
    # print(body_[i][0]["sub_data"])

ff = "www.w3cschool.cc"
ee = ff.replace("w3cschool", "baidu")
print(ee)

