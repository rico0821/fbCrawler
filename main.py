# -*- coding: utf-8 -*-

from crawler import Crawler
from logger import Log


# CONFIG
fb_version = '2.12'
app_id = 'APP_ID'
app_secret = 'APP_SECRET'
token = 'access_token=' + app_id + '|' + app_secret
target = 'bbcnews'

if __name__ == '__main__':
    
    Log.init()
    crawler = Crawler(token, fb_version)
    crawler.setTarget(target)
    crawler.setTimeInterval(1)
    crawler.init()

    