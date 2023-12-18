#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/11 22:41
# @Author  : v_bkaiwang
# @File    : __init__.py.py
# @Software: win10 Tensorflow1.13.1 python3.6.3

from flask import Blueprint
bp = Blueprint('main', __name__)
from app.main import routes
