#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/11 22:42
# @Author  : v_bkaiwang
# @File    : db.py
# @Software: win10 Tensorflow1.13.1 python3.6.3
from app import mongo


def get_feature_list() -> list:
    # 指定数据库后 查询所有集合名称
    collections = mongo.db.list_collection_names()
    feature_list = [collection for collection in collections]
    feature_list.sort()
    return feature_list


def get_benchmark_list() -> list:
    # 指定数据库后 查询所有集合名称
    collections = mongo.db.list_collection_names()
    feature_list = [collection for collection in collections]
    feature_list.sort()
    return feature_list


def get_query_option(option_list) -> dict:
    """
    传入forms.SubSelectGroup
    :param option_list:
    :return:
    """
    match = {
        '大于': '$gt',
        '小于': '$lt',
        '大于等于': '$gt',
        '小于等于': '$gte',
        '等于': '',
        '正则': '$regex'
    }
    query = dict()
    for option in option_list:
        operator = match[option['match_opr']]
        if operator:  # 不等于的情况
            if option['col_name'] in query:
                query[option['col_name']].update({match[option['match_opr']]: option['match_value']})
            else:
                query[option['col_name']] = {match[option['match_opr']]: option['match_value']}
        else:  # 等于的情况
            query[option['col_name']] = option['match_value']
    return query


def get_scenario_by_name(name) -> list:
    print(mongo.db['scenario'].find_one({'name': name}))
    return mongo.db['scenario'].find_one({'name': name})['keys']
