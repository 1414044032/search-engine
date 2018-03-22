# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst,Join
import datetime
from ArticleSpider.utils.common import extract_num,extract_num2
from w3lib.html import remove_tags
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

    def get_insert_sql(self):

        insert_sql = """
                        insert into bolearticle(url_object_id,url,title,create_date,front_image_url,praise_nums,comment_nums,collection_nums,tags,body)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                         """
        parms=(
        self["url_object_id"], self["url"], self["title"], self["create_date"], self["front_image_url"],
        self["praise_nums"], self["comment_nums"], self["collection_nums"], self["tags"], self["body"])
        return insert_sql,parms
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
    #插入知乎
    def get_insert_sql(self):
        insert_sql = """
                        insert into zhihu_question(zhihu_id,topics,url,title,content,answer_num,comments_num,watch_user_num,click_num,crawl_time)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE content=VALUES (content),answer_num=VALUES (answer_num), comments_num=VALUES (comments_num), watch_user_num=VALUES (watch_user_num),click_num=VALUES (watch_user_num) 
                         """
        zhihu_id=self["zhihu_id"][0]
        topics="".join(self["topices"])
        url="".join(self["url"])
        title="".join(self["title"])
        content="".join(self["content"])
        test1=self["answer_num"]
        answer_num=extract_num("".join(self["answer_num"]))
        test=self["comments_num"]
        comments_num=extract_num("".join(self["comments_num"]))
        watch_user_num=extract_num2(self["watch_user_num"][0])
        click_num=extract_num2(self["watch_user_num"][-1])
        crawl_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        parms = (zhihu_id,topics,url,title,content,answer_num,comments_num,watch_user_num,click_num,crawl_time)
        return insert_sql, parms

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

    def get_insert_sql(self):
        insert_sql = """
                        insert into zhihu_answer(zhihu_id,url,question_id,author_id,content,praise_num,comments_num,create_time,update_time,crawl_time)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE content=VALUES (content),comments_num=VALUES (comments_num),praise_num=VALUES (praise_num),
                        update_time=VALUES (update_time)
                         """
        create_time=datetime.datetime.fromtimestamp(self["create_time"]).strftime("%Y-%m-%d %H:%M:%S")
        update_time=datetime.datetime.fromtimestamp(self["update_time"]).strftime("%Y-%m-%d %H:%M:%S")
        parms=(self["zhihu_id"],
        self["url"],
        self["question_id"],
        self["author_id"],
        self["content"],
        self["parise"],
        self["comments_num"],
        create_time,
        update_time,
        self["crawl_time"].strftime("%Y-%m-%d %H:%M:%S"))
        return insert_sql, parms


def remove_sprit(value):
    # 去斜杠
    return value.replace("/","")

    #去掉html标签
def remove_html_tags(value):
    return


def handle_jobdesc(value):
    # 去换行
    job_desc_list=value.split("\n")
    job_desc_list=[item.strip() for item in job_desc_list if item.strip()!="查看地图"]
    return "".join(job_desc_list)


def add_none(value):
    # 个别招聘信息无标签处理
    if value is None or value == '':
        return "无标签"
    return value

def remove_lagu(value):
    #删除“发布于拉勾网标签”
    publish_list=value.split(" ")
    return publish_list[0].strip()

class LagouJobItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class LagouJobItem(scrapy.Item):
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field(
        input_processor=MapCompose(remove_sprit),
    )
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_sprit),
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_sprit),
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_sprit),
    )
    job_type = scrapy.Field(
        input_processor=MapCompose(remove_sprit),
    )
    pulish_time = scrapy.Field(
        input_processor=MapCompose(remove_lagu)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(add_none),
        output_processor=Join(",")
    )
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field(
        input_processor=MapCompose(remove_tags,handle_jobdesc),
    )
    job_addr = scrapy.Field()
    company_url = scrapy.Field()
    company_name = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
                        insert into lagou(url,url_object_id,title,salary,job_city,work_years,degree_need,job_type,pulish_time,tags,job_advantage,job_desc,job_addr,company_url,company_name,crawl_time,crawl_update_time)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE title=VALUES (title),salary=VALUES (salary),job_city=VALUES (job_city),work_years=VALUES (work_years),
                        degree_need=VALUES (degree_need),tags=VALUES (tags),
                        job_advantage=VALUES (job_advantage),job_desc=VALUES (job_desc),
                        job_addr=VALUES (job_addr),company_url=VALUES (company_url),
                        crawl_update_time=VALUES (crawl_update_time)
                         """

        parms=(
            self["url"],
            self["url_object_id"],
            self["title"],
            self["salary"],
            self["job_city"],
            self["work_years"],
            self["degree_need"],
            self["job_type"],
            self["pulish_time"],
            self["tags"],
            self["job_advantage"],
            self["job_desc"],
            self["job_addr"],
            self["company_url"],
            self["company_name"],
            self["crawl_time"].strftime("%Y-%m-%d %H:%M:%S"),
            self["crawl_update_time"].strftime("%Y-%m-%d %H:%M:%S")

        )
        return insert_sql, parms