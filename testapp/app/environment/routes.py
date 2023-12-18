# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/4 13:30
# @Author  : v_bkaiwang
# @File    : routes.py
# @Software: win10 Tensorflow1.13.1 python3.6.3
from bson import ObjectId
from flask import jsonify, request
from flask_restful import Resource
from app import mongo
from app.environment import api
from app.scenario import bp


@api.resources('/api/environments')
class Environments(Resource):
    """
    {'tag':'kunPeng920',
    'cpu':'AARCH64',
    'socket_num':'2',
    'mem_type':'DDR4',
    'mem_size':'128GB',
    'mem_channel_num':'4',
    'core_version':'6.1',
    'gcc_version':'9.2.1',
    'glibc_version':'2.3',
    'remark':''
    }


    """
    scenario_keys = ['tag',
                     'cpu',
                     'socket_num',
                     'mem_type',
                     'mem_size',
                     'mem_channel_num',
                     'core_version',
                     'gcc_version',
                     'glibc_version',
                     'remark']

    def get(self):
        db_cur = mongo.db['environment'].find()
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
        mongo.db["environment"].insert_one(scenario)
        return "", 204


@api.resources('/api/environment/<environment_id>')
class Environment(Resource):

    def delete(self, environment_id):
        mongo.db["environment"].delete_one({'_id': ObjectId(environment_id)})
        return '', 204

    def patch(self, environment_id):
        updated_scenario = request.json
        del updated_scenario['_id']
        del updated_scenario['key']
        del updated_scenario['editable']
        mongo.db['environment'].update_one({'_id': ObjectId(environment_id)}, {'$set': updated_scenario})
        return '', 204



