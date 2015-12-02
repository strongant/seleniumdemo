# -*- coding: UTF-8 -*-
import datetime
import urllib2

from selenium.webdriver.common.keys import Keys

from selenium import webdriver

import sys

start = datetime.datetime.now()
reload(sys)
sys.setdefaultencoding('utf-8')
driver = webdriver.PhantomJS(executable_path='/usr/bin/phantomjs',
                             service_log_path='./fetch.log')  # 这要可能需要制定phatomjs可执行文件的位置
# driver.implicitly_wait(10)  # seconds
driver.get("http://www.fieldschina.com/")

# print driver.current_url
# print driver.page_sourced
# print driver.find_element_by_id('result').text.split('\n')[0].split('来自：')[1]
print driver.page_source
driver.quit
end = datetime.datetime.now()
print 'take:', (end - start).seconds
