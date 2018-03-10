# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
from scrapy.loader import ItemLoader
from ArticleSpider.items import ZhihuAnswerItem,ZhihuQuestionItem
try:
    from urllib import parse
except:
    import urlparse as parse
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
        """
        提取html页面中所有的url，并访问url进行进一步爬取，
        提取的url中格式含有/question/xxx 就下载，然后进入解析函数。
        """
        #获取全部的url
        all_urls=response.css('a::attr(href)').extract()
        all_urls=[parse.urljoin(response.url,url) for url in all_urls]
        all_urls=filter(lambda x :True if x.startswith(u"https") else False,all_urls)
        for url in all_urls:
            print(url)
            match_obj=re.match("(.*zhihu.com/question/(\d+))(/|$).*",url,re.DOTALL)
            if match_obj:
                request_url=match_obj.group(1)
                question_id=match_obj.group(2)

                yield scrapy.Request(request_url,headers=self.headers,meta={"question_id":question_id},callback=self.parse_question)

    def parse_question(self,response):
        #处理question页面，提取item
        item_loader=ItemLoader(item=ZhihuQuestionItem(),response=response)
        item_loader.add_css("title","h1.QuestionHeader-title::text")
        item_loader.add_css("content","div.QuestionHeader-detail")
        item_loader.add_value("url",response.url)
        item_loader.add_value("zhihu_id",response.meta.get("question_id",""))
        item_loader.add_css("answer_num","h4.List-headerText span::text")
        item_loader.add_css("comments_num",".QuestionHeader-Comment button::text")
        item_loader.add_css("watch_user_num",".NumberBoard-itemValue::text")
        item_loader.add_css("topices",".QuestionHeader-topics .Popover div::text")

        question_item=item_loader.load_item()
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
        #验证是否登录成功
        test_json=json.loads(response.text)
        if "msg" in test_json and test_json["msg"]==u"登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url,dont_filter=True,headers=self.headers)