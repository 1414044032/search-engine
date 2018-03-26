# -*- coding: utf-8 -*-
import scrapy

class PortalSpider(scrapy.Spider):
    name = 'portal'
    allowed_domains = ['prcportal.pccw.com']
    start_urls = ['https://prcportal.pccw.com']

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}


    def start_requests(self):
        yield scrapy.FormRequest(url="https://prcportal.pccw.com", cookies=self.cookies, callback=self.parse_page)

    def check_login(self,response):

        pass


    def parse(self, response):
        pass


