#-*- coding : utf-8-*-
from selenium import webdriver
from scrapy.selector import Selector
import time
brower=webdriver.Chrome(executable_path="F:/chromedriver.exe")
chrome_opt=webdriver.ChromeOptions()
prefs={"profile.managed_default_content_setting.images":2}
chrome_opt.add_experimental_option("prefs",prefs)

brower.get("https://prcportal.pccw.com/web/guest/home")
print(brower.page_source)
time.sleep(1)
print("kaishi")

print (brower.find_element_by_xpath("//input[@name='_58_login']").text)
    #.send_keys("liu-qi.wang@pccw.com")
#brower.find_element_by_css_selector("input[name='_58_password']").send_keys("wW0776867106")
#brower.find_element_by_css_selector("#denglu input").click()
t_selector=Selector(text=brower.page_source)
brower.quit()