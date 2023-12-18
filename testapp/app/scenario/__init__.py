#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/4 13:30
# @Author  : v_bkaiwang
# @File    : __init__.py.py
# @Software: win10 Tensorflow1.13.1 python3.6.3
from flask import Blueprint
from flask_restful import Api

# 创建了一个名为main的蓝图 __name定义蓝图
bp = Blueprint("environment", __name__)
api = Api(bp)

from app.scenario import routes