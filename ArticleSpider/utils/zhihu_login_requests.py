#-*- coding : utf-8-*-
# 模拟登陆知乎
import requests
import time
try:
    import cookielib
except :
    import http.cookiejar as cookielib

import re
def get_gif(data):
    with open('captcha.gif', 'wb') as fb:
        fb.write(data)
    return raw_input('captcha')

def zhihu_login(account,password,oncaptcha):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    session=requests.session()
    session.cookies=cookielib.LWPCookieJar(filename="cookies.txt")
    try:
        session.cookies.load(ignore_discard=True)
    except:
        print("cookies未能加载")
    #session.get('https://www.zhihu.com/#signin',headers=headers)
    captcha_content=session.get('https://www.zhihu.com/captcha.gif?r=%d&type=login'%(time.time()*1000),headers=headers).content
    data={
        "email": account,
        "password": password,
        "remember_me": True,
        "captcha": oncaptcha(captcha_content)
    }
    msg=session.post('https://www.zhihu.com/login/email',data,headers=headers).content.decode('utf-8').encode('utf-8')
    session.cookies.save()
    print msg
    msg=eval(msg)
    if msg.get('msg'):
        print msg['msg']
if __name__ == "__main__":
    zhihu_login('1414044032@qq.com','w0776867106',get_gif)

