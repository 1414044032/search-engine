# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
import datetime
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

    #question的第一页请求url
    start_answer_url="http://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"
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
                #有关含有question的页面下载后进行提取
                request_url=match_obj.group(1)
                question_id=match_obj.group(2)

                yield scrapy.Request(request_url,headers=self.headers,meta={"question_id":question_id},callback=self.parse_question)
            else:
                #不是问题页进行访问跟踪,继续提取。
                yield scrapy.Request(url,headers=self.headers,callback=self.parse)
    def parse_question(self,response):
        #处理question页面，提取item
        item_loader=ItemLoader(item=ZhihuQuestionItem(),response=response)
        item_loader.add_css("title","h1.QuestionHeader-title::text")
        item_loader.add_css("content","div.QuestionHeader-detail")
        item_loader.add_value("url",response.url)
        question_id=response.meta.get("question_id", "")
        item_loader.add_value("zhihu_id",question_id)
        item_loader.add_css("answer_num","h4.List-headerText span::text")
        #评论格式：  69 条评论
        item_loader.add_css("comments_num",".QuestionHeader-Comment button::text")
        item_loader.add_css("watch_user_num",".NumberBoard-itemValue::text")
        item_loader.add_css("topices",".QuestionHeader-topics .Popover div::text")

        question_item=item_loader.load_item()
        yield scrapy.Request(self.start_answer_url.format(question_id,5,0),headers=self.headers,callback=self.parse_answer)
        yield question_item


    def parse_answer(self,response):
        #处理answer，answer返回的为json数据
        answer_json=json.loads(response.text)
        is_end=answer_json["paging"]["is_end"]
        answer_totals=answer_json["paging"]["totals"]
        answer_next=answer_json["paging"]["next"]
        #提取answer的具体字段
        for answers in answer_json["data"]:
            print answers
            answer_item=ZhihuAnswerItem()
            answer_item["zhihu_id"]=answers["id"]
            answer_item["url"]=answers["url"]
            answer_item["question_id"]=answers["question"]["id"]
            answer_item["author_id"]=answers["author"]["id"] if "id" in answers["author"] else None
            answer_item["content"]=answers["content"] if "content" in answers["content"] else None
            answer_item["parise"]=answers["voteup_count"]
            answer_item["comments_num"]=answers["comment_count"]
            answer_item["create_time"]=answers["created_time"]
            answer_item["update_time"] = answers["updated_time"]
            answer_item["crawl_time"]=datetime.datetime.now()

            yield answer_item

        #如果不是最后一页
        if not is_end:
            scrapy.Request(answer_next,headers=self.headers,callback=self.parse_answer)

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