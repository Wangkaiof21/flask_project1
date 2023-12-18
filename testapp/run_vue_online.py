#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/4 17:25
# @Author  : v_bkaiwang
# @File    : run_vue_online.py
# @Software: win10 Tensorflow1.13.1 python3.6.3
from flask import Flask, render_template

"""设置静态文件 模板文件都指向dist目录"""
app = Flask(__name__, template_folder="./dist", static_folder="./dist", static_url_path='')

""" 将前端路由控制的url访问全部交给控制器处理响应"""


@app.errorhandler(404)
@app.route('/')
def index(err=None):
    return render_template("index.html")


app.run(host='0.0.0.0', port=5000)
