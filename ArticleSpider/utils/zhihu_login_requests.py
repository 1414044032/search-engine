#-*- coding : utf-8-*-

import requests

try:
    import cookielib
except :
    import http.cookiejar as cookielib

import re

def zhihu_login(account,password):
    if re.match("^1\d{10}",account):
        print("手机登录")
