#-*- coding : utf-8-*-
import hashlib
import re
def get_md5(url):
    if isinstance(url,str):
        url=url.encode("utf-8")
    m=hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(text):
        match = re.match(".*?(\d+).*?", text)
        if match:
            nums = match.group(1)
        else:
            nums = 0
        return nums

def extract_num2(text):
        list=text.split(',')
        return int("".join(list))