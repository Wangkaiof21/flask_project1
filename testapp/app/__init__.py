#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/11 22:41
# @Author  : v_bkaiwang
# @File    : __init__.py.py
# @Software: win10 Tensorflow1.13.1 python3.6.3
# from flask import Flask
# from flask_bootstrap import Bootstrap
# from flask_cors import CORS
# from flask_pymongo import PyMongo
#
# from config import Config
#
# cors = CORS()
# bootstrap = Bootstrap()
# mongo = PyMongo()
#
#
# def creat_app(cofig_class=Config):
#     app = Flask(__name__)
#     # from_object
#     app.config.from_object(cofig_class)
#     # init_app 方法支持应用创建工厂方法
#     bootstrap.init_app(app)
#     mongo.init_app(app)
#     cors.init_app(app)
#
#     from app.main import bp as main_bp
#     from app.environment import bp as environment_bp
#     from app.scenario import bp as scenario_bp
#     from app.specification import bp as specification_bp
#     from app.test_results import bp as test_results_bp
#
#     # 导入并注册蓝图
#     app.register_blueprint(main_bp)
#     app.register_blueprint(environment_bp)
#     app.register_blueprint(scenario_bp)
#     app.register_blueprint(specification_bp)
#     app.register_blueprint(test_results_bp)
#     return app
