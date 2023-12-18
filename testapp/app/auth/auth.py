#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/5 22:47
# @Author  : v_bkaiwang
# @File    : auth.py
# @Software: win10 Tensorflow1.13.1 python3.6.3

from functools import wraps
from flask import request, abort, _request_ctx_stack
from flask_login import current_user

from app.auth.api import OAuth2


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            print("token is not")
            abort(403)
        res = OAuth2().get_user_info(access_token=token)
        if 'error' in request.json():
            print('get user info error')
            print(res.json())
            abort(403)
        _request_ctx_stack.top.user = res.json()
        print(current_user)
        return func(*args, **kwargs)

    return decorated_view()
