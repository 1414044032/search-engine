# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
import MySQLdb
from twisted.enterprise import adbapi
class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleIMagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        try:
            if "front_image_url" in item:
                for ok,value in results:
                    image_file_path=value["path"]
                item["front_image_path"]=image_file_path
                return item
        except Exception as e:
            print e
            item["front_image_path"] ="图片不可用"
            return item

class JsonWithEncodingPipline(object):
    def __init__(self):
        self.file=codecs.open('article.json','w',encoding="utf-8")
    def process_item(self,item,spider):
        lines=json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_close(self,spider):
        self.file.close()


class MysqlPipline(object):
    def __init__(self):
        self.conn=MySQLdb.connect('127.0.0.1','root','123456','article',charset="utf8",use_unicode=True)
        self.cursor=self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql="""
        insert into bolearticle(url_object_id,url,title,create_date,front_image_url,front_image_path,praise_nums,comment_nums,collection_nums,tags,body)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
         """
        self.cursor.execute(insert_sql,(item["url_object_id"],item["url"],item["title"],item["create_date"],
            item["front_image_url"],item["front_image_path"],item["praise_nums"],item["comment_nums"],item["collection_nums"],item["tags"],item["body"]))
        self.conn.commit()


class MysqlTwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool
    @classmethod
    def from_settings(cls,setting):
        dbparms=dict(
                host=setting["MYSQL_HOST"],
                db=setting["MYSQL_DBNAME"],
                user=setting["MYSQL_USER"],
                passwd=setting["MYSQL_PASSWORD"],
                charset='utf8',
                cursorclass=MySQLdb.cursors.DictCursor,
                use_unicode=True,
        )
        dbpool=adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool)
    #mysql异步插入执行
    def process_item(self, item, spider):
        query=self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)


    def handle_error(self,failure,item,spider):
        #处理异步插入的异常
        print failure

    def do_insert(self,cursor,item):
        insert_sql = """
                insert into bolearticle(url_object_id,url,title,create_date,front_image_url,praise_nums,comment_nums,collection_nums,tags,body)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                 """
        cursor.execute(insert_sql, (
        item["url_object_id"], item["url"], item["title"], item["create_date"], item["front_image_url"],
        item["praise_nums"], item["comment_nums"], item["collection_nums"], item["tags"], item["body"]))
