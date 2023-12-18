#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/4 17:26
# @Author  : v_bkaiwang
# @File    : run_online.py
# @Software: win10 Tensorflow1.13.1 python3.6.3
from app import creat_app

app = creat_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
