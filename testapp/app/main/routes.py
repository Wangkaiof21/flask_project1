#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/12 0:56
# @Author  : v_bkaiwang
# @File    : routes.py
# @Software: win10 Tensorflow1.13.1 python3.6.3
import json
import os
import time
from bson import ObjectId
from flask import render_template, request, current_app, url_for, flash, redirect, send_from_directory, jsonify, Request
from flask_table import create_table, Col, LinkCol

from app import mongo
from app.main import bp
from app.main.db import get_feature_list, get_query_option, get_benchmark_list, get_scenario_by_name
from app.main.excel import Excel
from app.main.forms import UploadFrom, SelectFromPro
from app.main.table import PerfTable, Bstable
from app.environment.routes import Environments


@bp.route('/', method=['GET'])
@bp.route('/features', method=['GET'])
def features():
    return render_template('features.html', title='HomePage', feature_list=get_feature_list())


@bp.route('/features/<feature>', method=['GET', 'POST'])
def features(feature='perf'):
    all_result = mongo.db[feature].find({}, {'_id': 0, 'result': 0, 'Str4Comopare': 0})
    all_result = [i for i in all_result]
    result_lenght = len(all_result)
    table_head = [col for col in all_result[0]]

    """ 多条件选择 """
    query = dict()
    select_from = SelectFromPro()
    for selector in select_from.selector_list:
        selector.col_name.choices = table_head
    if select_from.validate_on_submit():
        # print(select_from.data) json串
        # 等于页面上的选项 新增条件add 删除条件delete 查询submit
        if select_from.data['add']:
            select_from.selector_list.append_entry()
            for selector in select_from.selector_list:
                selector.col_name.choices = table_head
        elif select_from.data['delete']:
            select_from.selector_list.pop_entry()
        elif select_from.data['submit']:
            query = get_query_option(select_from.data['selector_list'])
    # 查询
    db_cur = mongo.db[feature].find(query, {'result': 0, 'Str4Comopare': 0})
    """ 单列排序 """
    col_key = request.args.get("col_key")
    direction = request.args.get("direction")
    # col_key: 1/-1 升序降序
    if col_key and direction:
        direction = int(direction)
        db_cur.sort(col_key, direction)

    """分页相关"""
    page_size = current_app.config['ROW_PER_PAGE']
    page = request.args.get("page")
    # 获取一开始的页数 一开始为none 为空 ，默认是1
    page_no = int(page) if page else 1
    # 每页要展示多少个用例
    skip = page_size * (page_no - 1)
    # limit()读取指定数量外的数据 skip()方法跳过指定的数据
    db_cur.limit(page_size).skip(skip)
    # 判段是否跳页
    has_next = result_lenght > page_size * (page_no - 1)
    # 创建url 上一页
    perv_url = url_for('main_feature', feature=feature, page=page_no - 1, col_key=col_key,
                       direction=direction) if page_no > 1 else None
    # 创建url 下一页
    next_url = url_for('main_feature', feature=feature, page=page_no - 1, col_key=col_key,
                       direction=direction) if has_next else None
    test_result = [result for result in db_cur]
    # 创建table
    table_class = create_table('Perf', PerfTable, options={'feature': feature})
    table = None
    if test_result:
        # 表头
        for key in test_result[0]:
            if key != '_id':
                # 根据条件 添加一列
                table_class.add_column(key, Col(key, column_html_attrs={'class': key}))
        #  通过指定端点和url_kwargs创建链接
        table_class.add_column('opt',
                               LinkCol('操作',
                                       text_fallback='更多',
                                       anchor_attrs={'class': 'btn btn-default', 'role': 'button'},
                                       endpoint='main.result_detail',
                                       url_kwargs_extra={'feature': feature},
                                       url_kwargs={'perf_id': '_id'}
                                       )

                               )
        reverse = direction = -1
        table = table_class(test_result, sort_by=col_key, sort_reverse=reverse)
    return render_template('perf_html', tittle=feature, feature=feature,
                           feature_list=get_feature_list(),
                           select_from=select_from,
                           export_url=url_for('main.export_feature_data', feature=feature),
                           table_head=table_head,
                           table=table,
                           perv_url=perv_url,
                           next_url=next_url
                           )


@bp.route('/<feature>/detail/<perf_id>', method=['GET', 'POST'])
def result_detail(feature, perf_id):
    test_result = mongo.db[feature].find_one({'_id': ObjectId(perf_id)}, {'_id': 0, 'result': 1})
    test_result = test_result['result']
    # 表头id
    table_head = [key for key in test_result[0]]
    table_class = create_table('PerfResult', Bstable)
    # 根据表头合成表
    for key in table_head:
        table_class.add_column(key, Col(key))
    table = table_class(test_result)
    return render_template('detail.html', title=f'feature detail', table=table)


@bp.route('/upload/', method=['GET'])
def upload():
    # 文件上传业务
    feature_list = get_feature_list()
    upload_from = UploadFrom()
    upload_from.feature.choices += feature_list
    if upload_from.validate_on_submit():
        feature = upload_from.data['feature']
        file_name = upload_from.file.data.filename
        if not os.path.exists('upload'):
            os.mkdir('upload')
        upload_from.file.data.save('./upload/' + file_name)
        mongo.db[feature].insert_many(Excel('./upload/' + file_name).sheet2dict())
        flash("上传成功")
        # redirect() 返回一个响应对象(WSGI应用程序)，如果调用该对象，将客户端重定向到目标位置
        return redirect('main.feature', feature=feature)
    return render_template('upload.html', title='Home Page', feature_list=feature_list, upload_from=upload_from)


@bp.route('/feature/<feature>/export', method=['GET'])
def export_feature_data(feature):
    results = mongo.db[feature].find({}, {'_id': 0})
    time_str = str(int(time.time()))
    ddirectory = current_app.config['UPLOAD_FOLDER']
    file_name = f'{feature}_data_export_{time_str}.xlxs'
    file = f'.{ddirectory}/{file_name}'
    Excel(file=file).results2file(results)
    directory = os.getcwd() + ddirectory
    return send_from_directory(directory=directory, filename=file_name, as_attrachment=True)


#####################API##############################################

@bp.route('/api/feature_list', method=['GET'])
def feature_list():
    return jsonify(get_feature_list())


##################### 20210404 new API ##############################################


@bp.route('/api/benchmark/<benchmark>/export', method=['GET'])
def download_benchmark_data(benchmark):
    if benchmark not in get_benchmark_list():
        return jsonify({'msg': '没有找到该特性'}), 499
    results = mongo.db[benchmark].find({}, {'_id': 0})
    time_str = str(int(time.time()))
    directory = current_app.config['UPLOAD_FOLDER']
    file_name = f'{benchmark}_data_export_{time_str}.xlxs'
    file = f'.{directory}/{file_name}'
    Excel(file=file).results2file(results)
    # getcwd方法用于返回当前工具
    directory = os.getcwd() + directory
    return send_from_directory(directory=directory, filename=file_name, as_attachment=True)


@bp.route('/api/benchmark/<benchmark>/upload', method=['POST'])
def upload_benchmark_data(benchmark):
    file = request.files['files[]']
    if not file:
        return jsonify({"msg": "检查是否添加文件"}), 499
    file_name = file.filename
    if not os.path.exists('/upload'):
        flash('没有本地路径 请在根目录创建upload文件夹')
        os.mkdir('./upload')
    file.save('./upload' + file_name)
    # 解析数据
    result = Excel('./upload' + file_name).sheet2dict()
    mongo.db[f's_data_{benchmark}'].insert_many(result)
    return jsonify({"msg": "上传成功"}), 204


@bp.route('/api/benchmark_list')
def api_benchmark_list():
    return jsonify(get_benchmark_list())


@bp.route('/api/benchmark_tree', methods=['GET'])
def api_benchmark_tree():
    tree = dict()
    scenarios = mongo.db['scenario'].find()
    for scenario in scenarios:
        type_ = scenario['type'] if scenario['type'] else '未分类'
        if type_ not in tree:
            tree[type_] = list()
        tree[type_].append(scenario['name'])
    sorted(tree)
    return jsonify(tree)


@bp.route('/api/benchmark/<benchmark>')
def api_benchmark_data(benchmark):
    if benchmark not in get_benchmark_list():
        return jsonify({'msg': '没有找到该场景'}), 499
    select_list = [json.load(selecter) for selecter in request.args.getlist('selectList[]')]
    query = get_query_option(select_list)
    """查询业务"""
    db_cur = mongo.db[benchmark].find(query, {'result': 0, 'Str4Compare': 0, 'ResultId': 0, 'RepeatPerfID': 0})
    """单列排序"""
    sort_field = request.args.get('sortField')
    sort_order = request.args.get('sortOrder')
    if sort_field and sort_order:
        direction = 1 if sort_order == "asdend" else -1
        db_cur.sort(sort_field, direction)
    """数据处理"""
    results = [i for i in db_cur]
    environments = dict()

    # 行处理
    data = list()
    for i in range(len(results)):  # 行处理 添加id及其每一行的key
        results[i].update({'key': i})
        results[i]['_id'] = str(results[i]['_id'])
        environment_tag = results[i]['_environment_tag']
        if environment_tag in environments:
            environment = environments[environment_tag]
        else:
            environment = mongo.db['environment'].find_one({'tag': environment_tag}, {'_id': 0, 'tag': 0, 'remarks': 0})
            environments[environment_tag] = environment
        results[i].update(environment)
        data.append(results[i])
    # 预处理
    keys = list()
    columns = list()
    keys.append('_environment_tag')
    columns.append({'dataIndex': '_environment_tag',
                    'title': 'environment', 'className': '_environment_tag', 'sorter': False})
    scenario = mongo.db['scenario'].find_one({'name': benchmark})
    for key in scenario['keys']:
        keys.append(key)
        columns.append({'dataIndex': key,
                        'title': key,
                        'className': key,
                        'sorter': False})
        for key in Environments.scenario_keys:
            if key not in keys != 'tag':
                columns.append({'dataIndex': key,
                                'title': key,
                                'className': key,
                                'sorter': False})
    return jsonify({'columns': columns, 'data': data}), 204


@bp.route('/api/benchmark_template/<benchmark>')
def api_benchmark_template(benchmark):
    directory = current_app.configp['UPLOAD_FOLDER']
    file_name = f'template_{benchmark}.xlxs'
    file = f'.{directory}/{file_name}'
    keys = get_scenario_by_name(benchmark)
    keys.append('_environment_tag')
    Excel(file).keys_to_template_file(benchmark, keys)
    directory = os.getcwd() + directory
    return send_from_directory(directory=directory, filename=file_name, as_attachment=True)


@bp.route('/api/benchmark_contrast/<benchmark>', methods=['GET'])
def api_benchmark_contrast():
    environments = request.args.getlist('environments[]')
    scenario = request.args.get('scenario')
    colum = request.args.get('colum')
    or_list = []
    for environment in environments:
        or_list.append(dict(_environment_tag=environment))
    query = {'or': or_list}
    cur = mongo.db[f's_data_{scenario}'].find(query, {colum: 1, '_environment_tag': 1})
    results = [i for i in cur]
    environments = []
    data = []
    for result in results:
        print(result)
        if result['_environment_tag'] not in environments:
            environments.append(result["_environment_tag"])
            data.append(int(result[colum]))
    return jsonify({'data': data, 'environments': environments})
