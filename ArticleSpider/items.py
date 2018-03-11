# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst,Join

def add_jobbole(value):
    return value+"-LIUQI"
def get_nums(value):
    match = re.match(".*(\d+).*", value)
    if match:
        nums = match.group(1)
    else:
        nums = '0'
    return nums

def remove_comment_tags(value):
    #去掉tags中的评论
    if u"评论" in value:
        return ""
    else:
        return value
def return_value(value):
    return value

class ArticlespiderItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class JobBoleArticleItem(scrapy.Item):
    title=scrapy.Field(
        input_processor=MapCompose(add_jobbole)
    )
    create_date=scrapy.Field()
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    front_image_url=scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path=scrapy.Field()
    praise_nums=scrapy.Field()
    comment_nums=scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    collection_nums=scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags=scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    body=scrapy.Field()


class ZhihuQuestionItem(scrapy.Item):
    #知乎问题item
    zhihu_id=scrapy.Field()
    topices=scrapy.Field()
    url=scrapy.Field()
    title=scrapy.Field()
    content=scrapy.Field()
    answer_num=scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num=scrapy.Field()
    click_num=scrapy.Field()
    crawl_time=scrapy.Field()


class ZhihuAnswerItem(scrapy.Item):
    #知乎问题答案item
    zhihu_id=scrapy.Field()
    url=scrapy.Field()
    question_id=scrapy.Field()
    author_id=scrapy.Field()
    content=scrapy.Field()
    parise=scrapy.Field()
    comments_num=scrapy.Field()
    create_time=scrapy.Field()
    update_time=scrapy.Field()
    crawl_time=scrapy.Field()