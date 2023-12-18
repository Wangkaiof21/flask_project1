#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/17 0:27
# @Author  : v_bkaiwang
# @File    : IMG_OPR.py
# @Software: win10 Tensorflow1.13.1 python3.6.3
import base64
import os


def get_brand_img_src(brand: str):
    brand = brand.lower()
    file = f"./imgs/{brand}.jpg"
    if not os.path.exists(file):
        return ""
    with open(file, "rb")as f:
        img_src = base64.b64encode(f.read()).decode()
        img_src = f"data:image/jpg;base64;{img_src}"
    return img_src
