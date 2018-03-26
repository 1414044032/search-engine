# -*- coding: utf-8 -*-
import scrapy
import re
from ArticleSpider.items import JobBoleArticleItem,ArticlespiderItemLoader
from scrapy import Request
try:
    from urllib import parse
except:
    import urlparse as parse
from scrapy.loader import ItemLoader
from ArticleSpider.utils.common import get_md5
class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']
    custom_settings={
        "COOKIES_ENABLED" : False
    }
    def parse(self, response):
        """
        获取下一页url并交给Scrapy下载
        获取文章url并下载后解析
        :param response:
        :return:
        """
        post_nodes=response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            image_url=post_node.css("img::attr(src)").extract_first("")
            post_url=post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url,post_url),meta={"font_image_url":image_url},callback=self.parse_article)
        #提取下一页URl
        next_url=response.xpath('.//a[@class="next page-numbers"]/attribute::href').extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)
    def parse_article(self,response):
        article_item=JobBoleArticleItem()
        #提取文章相关字段
        #标题
        # title=response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        # #response.css('.entry-header h1::text').extract()
        # #创建时间
        # creat_date= response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().split(" ")[0]
        # # response.css('.entry-meta-hide-on-mobile::text').extract()[0]
        # #点赞数
        # praise_nums=response.xpath('//div[@class="post-adds"]/span/h10/text()').extract()[0]
        # #response.css('.vote-post-up h10::text').extract()
        # #收藏数
        # collection=response.css('.bookmark-btn::text').extract_first("")
        # collection_match=re.match(".*(\d+).*",collection)
        # if collection_match:
        #     collection_nums=collection_match.group(1)
        # else:
        #     collection_nums='0'
        # #评论数
        # comments = response.xpath('//a[@href="#article-comment"]/span/text()').extract_first("")
        # comments_match = re.match(".*(\d+).*", comments)
        # if comments_match:
        #     comments_nums = comments_match.group(1)
        # else:
        #     comments_nums = '0'
        # #正文
        # body=response.xpath('//div[@class="entry"]').extract()[0]
        # #图片
        front_image_url=response.meta.get("font_image_url","")
        # #标签列表
        # tag_list=response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # #去掉标签中的评论
        # tag_list=[element for element in tag_list if not element.strip().endswith(u"评论")]
        # #取出标签有逗号分割
        # tags=",".join(tag_list)
        # article_item['title']=title
        # article_item['create_date']=creat_date
        # article_item['url']=response.url
        # article_item['front_image_url']=[front_image_url]
        # article_item['praise_nums']=praise_nums
        # article_item['collection_nums']=collection_nums
        # article_item['comment_nums']=comments_nums
        # article_item['body']=body
        # article_item['tags']=tags
        # article_item['title']=title
        # article_item[ 'url_object_id']=get_md5(response.url)
        #通过ItemLoadtem
        item_loader=ArticlespiderItemLoader(item=JobBoleArticleItem(),response=response)
        item_loader.add_xpath('title','//div[@class="entry-header"]/h1/text()')
        item_loader.add_xpath('create_date','//p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_value('url',response.url)
        item_loader.add_value('url_object_id',get_md5(response.url))
        item_loader.add_xpath('praise_nums','//div[@class="post-adds"]/span/h10/text()')
        item_loader.add_value('front_image_url',[front_image_url])
        item_loader.add_value('collection_nums','.bookmark-btn::text')
        item_loader.add_xpath('comment_nums','//a[@href="#article-comment"]/span/text()')
        item_loader.add_xpath('tags','//p[@class="entry-meta-hide-on-mobile"]/a/text()')
        item_loader.add_xpath('body','//div[@class="entry"]')
        article_item=item_loader.load_item()
        yield article_item