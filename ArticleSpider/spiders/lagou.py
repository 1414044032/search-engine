# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.items import LagouJobItemLoader,LagouJobItem
from ArticleSpider.utils.common import get_md5
import datetime
class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'user_trace_token=20171015132411-12af3b52-3a51-466f-bfae-a98fc96b4f90; LGUID=20171015132412-13eaf40f-b169-11e7-960b-525400f775ce; SEARCH_ID=070e82cdbbc04cc8b97710c2c0159ce1; ab_test_random_num=0; X_HTTP_TOKEN=d1cf855aacf760c3965ee017e0d3eb96; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DsXIrWUxpNGLE2g_bKzlUCXPTRJMHxfCs6L20RqgCpUq%26wd%3D%26eqid%3Dee53adaf00026e940000000559e354cc; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_hotjob; login=false; unick=""; _putrc=""; JSESSIONID=ABAAABAAAFCAAEG50060B788C4EED616EB9D1BF30380575; _gat=1; _ga=GA1.2.471681568.1508045060; LGSID=20171015203008-94e1afa5-b1a4-11e7-9788-525400f775ce; LGRID=20171015204552-c792b887-b1a6-11e7-9788-525400f775ce',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    }
    rules = (
        Rule(LinkExtractor(allow=r'/gongsi/.*'), follow=True),
        Rule(LinkExtractor(allow=r'/zhaopin/.*'),follow=True),
        Rule(LinkExtractor(allow=r'/jobs/\d+.html'), callback='parse_job', follow=True),
    )
    def parse_job(self, response):
        item_load=LagouJobItemLoader(item=LagouJobItem(),response=response)
        item_load.add_value("url", response.url)
        item_load.add_value("url_object_id", get_md5(response.url))
        item_load.add_css("title", "div.job-name::attr(title)")
        item_load.add_css("salary", ".salary::text")
        item_load.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_load.add_xpath("work_years","//*[@class='job_request']/p/span[3]/text()")
        item_load.add_xpath("degree_need","//*[@class='job_request']/p/span[4]/text()" )
        item_load.add_xpath("job_type","//*[@class='job_request']/p/span[5]/text()")
        item_load.add_css("pulish_time", ".publish_time::text")
        item_load.add_xpath("tags", "//*[@class='position-label clearfix']/li/text()")
        item_load.add_xpath("job_advantage", "//*[@class='job-advantage']/p/text()")
        item_load.add_xpath("job_desc", "//*[@class='job_bt']/div")
        item_load.add_xpath("job_addr", "//*[@class='work_addr']/a/text()")
        item_load.add_xpath("company_url", "//*[@class='c_feature']/li/a/@title")
        item_load.add_css("company_name", ".job_company dt img::attr(alt)")
        item_load.add_value("crawl_time",datetime.datetime.now())
        item_load.add_value("crawl_update_time", datetime.datetime.now())

        lagou_item=item_load.load_item()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return lagou_item
