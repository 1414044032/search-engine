# -*- coding: utf-8 -*-
import scrapy

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def parse(self, response):
        pass
    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        captcha_content = session.get('https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000),
                                      headers=headers).content
        return [scrapy.FormRequest(
            url="https://www.zhihu.com/login/email",
            formdata={
                "email": "1414044032@qq.com",
                "password": "w0776867106",
                "remember_me": True,
                "captcha": oncaptcha(captcha_content)
            }

        )]