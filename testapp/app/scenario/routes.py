#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/4 13:30
# @Author  : v_bkaiwang
# @File    : routes.py
# @Software: win10 Tensorflow1.13.1 python3.6.3
from bson import ObjectId
from flask import jsonify, request
from flask_restful import Resource
from app import mongo
from app.scenario import api
from app.scenario import bp

_collection = 'scenario'
scenario_key = ['name', 'type', 'keys', 'showKeys', 'contrastKeys', 'remark', ]


@api.resources('/api/scenarios')
class Scenarios(Resource):
    scenario_keys = ['name', 'keys', 'remarks']

    def get(self):
        db_cur = mongo.db['scenario'].find()
        results = [result for result in db_cur]
        data = list()
        for i in range(len(results)):
            results[i].update({'key': i})
            request[i]['_id'] = str(results[i]['_id'])
            data.append(results[i])
        return jsonify({'data': data})

    def post(self):
        scenario = dict()
        for key in self.scenario_key:
            scenario[key] = request.json.get(key, "")
        mongo.db["scenario"].insert_one(scenario)
        return "", 204


@api.resources('/api/scenario/<scenario_id>')
class Scenario(Resource):

    def delete(self, scenario_id):
        mongo.db["scenario"].delete_one({'_id': ObjectId(scenario_id)})
        return '', 204

    def patch(self, scenario_id):
        updated_scenario = request.json
        del updated_scenario['_id']
        del updated_scenario['key']
        del updated_scenario['editable']
        mongo.db['scenario'].update_one({'_id': ObjectId(scenario_id)}, {'$set': updated_scenario})
        return '', 204


@bp.route('/api/scenario_tree', methods=['GET'])
def scenario_tree():
    tree = dict()
    scenarios = mongo.db[_collection].find()
    for scenario in scenarios:
        type_ = scenario['type'] if scenario['type'] else '未分类'
        if type not in tree:
            tree[type_] = list()
        tree[type_].append(scenario['name'])
    sorted(tree)
    return jsonify(tree)


