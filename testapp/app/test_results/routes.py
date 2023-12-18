#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/18 22:57
# @Author  : v_bkaiwang
# @File    : routes.py
# @Software: win10 Tensorflow1.13.1 python3.6.3
from bson import ObjectId
from flask import Flask, jsonify, request
from flask_restful import Resource

from app import mongo
from app.scenario import api, bp

_collection = 'cpu_test_results'
test_result_keys = ['_id', 'name', '测试芯片', '是否有效', '测试起始时间', 'osVersion', 'qlibcVersion', 'IP']


@bp.route('/api/test_results_cols')
def get_test_results_col():
    return jsonify(test_result_keys)


@api.resources('/api/test_results')
class TestResults(Resource):

    def get(self):
        db_cur = mongo.db[_collection].find()
        results = [result for result in db_cur]
        data = list()
        for i in range(len(results)):
            results[i].update({'key': i})
            results[i]['_id'] = str(results[i]['_id'])
            data.append(results[i])
        return jsonify({'data': data})

    def post(self):
        test_result = dict()
        for key in test_result_keys[1:]:
            test_result[key] = request.json.get(key, '')
        mongo.db[_collection].insert_one(test_result)
        return '', 204
