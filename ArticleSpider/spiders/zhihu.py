# -*- coding: utf-8 -*-
import scrapy
import time
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    '''
    captcha_content = session.get('https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000),
                                  headers=headers).content
    #验证码地址：
    captcha：  "https://www.zhihu.com/captcha.gif?r={0}&type=login"format(t)                                
    '''

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000), headers=self.headers,callback=self.login)]


    def login(self,response):
        with open('captcha.gif', 'wb') as fp:
            fp.write(response.body)
        # 输入验证码
        print 'Please enter captcha: '
        captcha = raw_input()

        yield scrapy.FormRequest(
            url="https://www.zhihu.com/login/email",
            headers=self.headers,
            formdata={
                'email': '1414044032@qq.com',
                'password': 'w0776867106',
                'remember_me': 'true',
                'captcha': captcha
            },
            callback=self.check_login
        )

    def check_login(self,response):
        print response