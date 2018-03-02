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