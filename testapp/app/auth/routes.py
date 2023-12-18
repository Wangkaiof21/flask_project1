#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/5 23:23
# @Author  : v_bkaiwang
# @File    : routes.py
# @Software: win10 Tensorflow1.13.1 python3.6.3
from flask import jsonify, current_app, request
from flask_login import current_user

from app.auth import bp
from app.auth.api import oauth
from app.auth.auth import login_required


@bp.route('/', methods=['GET'])
@login_required
def test():
    return jsonify({'msg': 'test'})


@bp.route('/api/access_token', methoads=['GRT'])
def get_access_token():
    code = request.args.get('code')
    redirect_uri = request.args.get('redirectUri')
    client_id = current_app.config['QAUTH_LOGIN_CLIENT_ID']
    client_secret = current_app.config['QAUTH_LOGIN_CLIENT_SECRET']
    res = oauth.get_access_token(code=code, redirect_uri=redirect_uri, client_id=client_id, client_secret=client_secret)
    return jsonify(res.json())


