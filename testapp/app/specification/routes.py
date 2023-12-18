#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/18 22:50
# @Author  : v_bkaiwang
# @File    : routes.py
# @Software: win10 Tensorflow1.13.1 python3.6.3
from bson import ObjectId
from flask import Flask, jsonify, request
from flask_restful import Resource

from app import mongo
from app.scenario import api, bp
from app.test_results.routes import test_result_keys
from app.specification.IMG_OPR import get_brand_img_src

_collection = 'cpu_specifications'
specifications_key = []


@bp.route('/api/specifications_col')
def get_specifications_col():
    return jsonify(specifications_key)


@bp.route('/api/specifications_contract')
def contract_specification():
    """根据请求入参解析mongodeb的query入参"""
    contract_specifications = request.args.getlist('contractSpecifications[]')
    contract_types = request.args.getlist('contractTypes[]')
    or_list = [{'name': specification} for specification in contract_specifications]
    query = {'$or': or_list} if or_list else dict()
    """数据库 查询规格信息"""
    cur = mongo.db[_collection].find(query, {'_id': 0})
    specifications = [i for i in cur]
    """生成表头"""
    colums = ['型号'] + [specification for specification in specifications]

    data_source = list()
    """处理规格信息"""
    if '规格' in contract_types:
        data_source.append({'信息分类': '规格信息'})
        keys = [key for key in specifications_key[1:7]]
        for key in keys:
            row_data = {'型号': key}
            for specification in specifications:
                row_data.update({specification['name']: specification.get(key)})
            data_source.append(row_data)

        data_source.append({'信息分类': 'Core'})
        keys = [key for key in specifications_key[7:23]]
        for key in keys:
            row_data = {'型号': key}
            for specification in specifications:
                row_data.update({specification['name']: specification.get(key)})
            data_source.append(row_data)

        data_source.append({'信息分类': 'DDR'})
        keys = [key for key in specifications_key[23:26]]
        for key in keys:
            row_data = {'型号': key}
            for specification in specifications:
                row_data.update({specification['name']: specification.get(key)})
            data_source.append(row_data)

        data_source.append({'信息分类': 'PCIe'})
        keys = [key for key in specifications_key[26:29]]
        for key in keys:
            row_data = {'型号': key}
            for specification in specifications:
                row_data.update({specification['name']: specification.get(key)})
            data_source.append(row_data)

        data_source.append({'信息分类': '跨P'})
        keys = [key for key in specifications_key[29:32]]
        for key in keys:
            row_data = {'型号': key}
            for specification in specifications:
                row_data.update({specification['name']: specification.get(key)})
            data_source.append(row_data)

        data_source.append({'信息分类': '功耗&封装'})
        keys = [key for key in specifications_key[32:35]]
        for key in keys:
            row_data = {'型号': key}
            for specification in specifications:
                row_data.update({specification['name']: specification.get(key)})
            data_source.append(row_data)

    if '性能' in contract_types:
        """获取1-1表关系 芯片名-测试记录"""
        specification_test_results = dict()
        for specification in specifications:
            test_result = mongo.db['cpu_test_result'].find_one('测试芯片', specification['name'], {'是否发布': True})
            specification_test_results[specification['name']] = test_result if test_result else None
        """处理测试记录"""
        data_source.append({'信息分类': '测试记录'})
        keys = [key for key in test_result_keys[4:]]
        for key in keys:
            row_data = {'型号': key}
            for specification in specifications:
                specification_name = specification['name']
                result_data = specification_test_results[specification_name]
                values = result_data.get(key) if result_data else ''
                row_data.update({specification_name: values})
            data_source.append(row_data)

        """数据库查询场景信息"""
        scenarios_cur = mongo.db['scenario'].find()
        scenarios = [scenario for scenario in scenarios_cur]

        """获取1-1-n表关系 芯片名-测试记录-各场景测试数据"""
        specification_result_data = dict()
        for specification in specifications:
            specification_name = specification['name']
            specification_data = dict()
            for scenario in scenarios:
                if specification_test_results[specification_name]:
                    _test_result_id = str(specification_test_results[specification_name]['_id'])
                    test_data = mongo.db[f's_data_{scenario["name"]}'].find_one({'_test_result_id': _test_result_id},
                                                                                {'_id': 0})
                    specification_data[scenario['name']] = test_data
                else:
                    specification_data[scenario['name']] = None
            specification_result_data[specification_name] = specification_data
        """处理测试数据"""
        for scenario in scenarios:
            scenario_keys = scenario['contrastKey']
            scenario_name = scenario['name']
            data_source.append({'信息分类': scenario_name})
            for key in scenario_keys:
                row_data = {'型号': key}
                for specification in specifications:
                    specification_name = specification['name']
                    scenario_data = specification_result_data[specification_name][scenario_name]
                    values = scenario_data.get(key) if scenario_data else ''
                    row_data.update({specification_name: values})
                data_source.append(row_data)
    return jsonify({'columns': colums, 'dataSource': data_source})


@bp.route('/api/specifications_tree')
def get_specifications_tree():
    tree = dict()
    specifications = mongo.db[_collection].find().sort("name")
    for specification in specifications:
        type_ = specification['厂家'] if specification['厂家'] else "其他"
        if type_ not in tree:
            brand = dict()
            brand["imgsrc"] = get_brand_img_src(type_)
            brand['specifications'] = list()
            tree[brand] = brand
        tree[type_]["specifications"].append({'_id': str(specification["_id"]), "name": specification["name"]})
    result = dict()
    for brand in sorted(tree):
        result[brand] = tree[brand]
    return jsonify(result)


@bp.route('/api/specifications')
class Specifications(Resource):
    def get(self):
        db_cur = mongo.db[_collection].find()
        results = [result for result in db_cur]
        data = list()
        for i in range(len(results)):
            results[i].update({'key': i})
            request[i]['_id'] = str(results[i]['_id'])
            data.append(results[i])
        return jsonify({'data': data})

    def post(self):
        scenario = dict()
        for key in specifications_key:
            scenario[key] = request.json.get(key, "")
        mongo.db["scenario"].insert_one(scenario)
        return "", 204


@api.resources('/api/specification/<specification_id>')
class Specification(Resource):

    def delete(self, specification_id):
        mongo.db[_collection].delete_one({'_id': ObjectId(specification_id)})
        return '', 204

    def patch(self, specification_id):
        updated_scenario = request.json
        del updated_scenario['_id']
        del updated_scenario['key']
        del updated_scenario['editable']
        mongo.db['environment'].update_one({'_id': ObjectId(specification_id)}, {'$set': updated_scenario})
        return '', 204
