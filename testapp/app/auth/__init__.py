#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/5 21:31
# @Author  : v_bkaiwang
# @File    : __init__.py.py
# @Software: win10 Tensorflow1.13.1 python3.6.3
from flask import Blueprint
from flask_restful import Api

bp = Blueprint('auth', __name__)
api = Api(bp)

from app.auth import routes
