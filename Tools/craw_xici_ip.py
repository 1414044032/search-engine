#-*- coding : utf-8-*-
import requests
from scrapy.selector import Selector
import MySQLdb

conn=MySQLdb.connect(host="127.0.0.1",user="root",passwd="123456",db="article",charset="utf8")
cursor=conn.cursor()
def craw_ips():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

    for i in range(1568):
        re=requests.get("http://www.xicidaili.com/nn/{0}".format(i),headers=headers)

        selector=Selector(text=re.text)
        all_trs=selector.css("#ip_list tr")
        ip_list=[]
        for tr in all_trs[1:]:
            speed_str=tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed=float(speed_str.split("秒")[0])
            all_texts=tr.css("td::text").extract()
            ip=all_texts[0]
            port=all_texts[1]
            proxy_type=all_texts[5]

            ip_list.append((ip,port,proxy_type,speed))
        for ip_info in ip_list:
            cursor.execute(
                "insert  proxy_ip(ip,port,speed,proxy_type) VALUES ('{0}','{1}',{2},'HTTP')ON DUPLICATE KEY UPDATE port= values(port)".format(
                ip_info[0],ip_info[1],ip_info[3]

            )
            )
            conn.commit()
    print (re.text)

class GetIP(object):

    def delete_ip(self,ip):
        #删除无效IP
        delete_sql="delete from proxy_ip where ip={0}".format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def check_ip(self,ip,port):
        #检查IP是否合法
        http_url="http://www.baidu.com"
        proxy_url="http://{0}:{1}".format(ip,port)
        try:
            proxy_dict={
                "http":proxy_url
            }
            response=requests.get(http_url,proxies=proxy_dict)
            return True
        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code=response.status_code
            if code>=200 and code<300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False
    def get_random_ip(self):
        #获取一个IP
        select_sql="select ip,port from proxy_ip order by rand() LIMIT 1"
        cursor.execute(select_sql)
        for ip_info in cursor.fetchall():
            ip=ip_info[0]
            port=ip_info[1]
            check_re=self.check_ip(ip,port)
            if check_re:
                return "http://{0}:{1}".format(ip,port)
            else:
                return self.get_random_ip()
if __name__=="__main__":
    get_ip=GetIP()
    get_ip.get_random_ip()