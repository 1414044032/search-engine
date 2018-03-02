#-*- coding : utf-8-*-
import hashlib

def get_md5(url):
    if isinstance(url,unicode):
        url=url.encode("utf-8")
    m=hashlib.md5()
    m.update(url)
    return m.hexdigest()

