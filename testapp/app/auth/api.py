#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/5 22:13
# @Author  : v_bkaiwang
# @File    : api.py
# @Software: win10 Tensorflow1.13.1 python3.6.3
import requests


class OAuth2:
    BASE_URL = 'https://login-test.alibaba.com'

    def get_user_info(self, access_token):
        data = {'access_token': access_token}
        res = requests.post(self.BASE_URL + "/rpc/oauth2/user_info.json", data=data)
        return res

    def get_access_token(self, code, redirect_uri, client_id, client_secret, grant_type='authorization_code'):
        data = {'grant_type': grant_type, 'code': code, 'redirect_uri': redirect_uri, 'client_id': client_id,
                'client_secret': client_secret}
        res = requests.post(self.BASE_URL + "/rpc/oauth2/user_info.json", data=data)
        return res

    def disable_token(self, access_token):
        data = {'access_token': access_token}
        res = requests.post(self.BASE_URL + "/rpc/oauth2/user_info.json", data=data)
        return res


oauth = OAuth2()
