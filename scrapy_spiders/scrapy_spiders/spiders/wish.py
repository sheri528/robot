# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import json

import scrapy
from scrapy_spiders.items import GrabPriceItem

class WishSpider(scrapy.Spider):

    '''
        Log in Wish before getting products info.
    '''

    name = "wish"

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'COOKIES_DEBUG': True,
        'COOKIES_ENABLED': True,
        'DOWNLOAD_DELAY': 0.25,
        'USER_AGENT': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36",
        'REDIRECT_ENABLED': True,
        'AJAXCRAWL_ENABLED': True,
        'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 100,
        'EXTENSIONS': {
            'scrapy.telnet.TelnetConsole': None
        },
        'ITEM_PIPELINES': {
        },
        'LOG_FILE': "wish.log"
    }

    def __init__(self, url=None, *args, **kwargs):
        super(WishSpider, self).__init__(*args, **kwargs)
        self.url = url
        assert self.url, self.logger.error("url is None")
        self.index_url = "https://www.wish.com"
        self.account = {'email': '@163.com', 'password': ''}
        self.login_url = r'https://www.wish.com/api/email-login'

    def start_requests(self):
        request = scrapy.Request(url=self.index_url, callback=self.after_index)
        yield request

    def after_index(self, response):
        '''get _xsrf'''

        for k, v in response.headers.items():
            if k == 'Set-Cookie' and re.search('_xsrf', str(v)):
                _xsrf = re.findall('_xsrf\=(.*?)\;', str(v))[0]
                post_data = {
                    "email": self.account['email'],
                    "password": self.account['password'],
                    "_buckets": '',
                    "_experiments": '',
                    "_xsrf": _xsrf,
                }
                yield scrapy.FormRequest(url=self.login_url, formdata=post_data, callback=self.after_login)
                break
        else:
            self.logger.error("wish can't find _xsrf. url : {}".format(self.url))

    def after_login(self, response):
        self.logger.info("wish login success, message : {}".format(response.body))
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        item = GrabPriceItem()
        item['product_url'] = self.url
        js = response.xpath('//script[@type="application/ld+json"]/text()').extract_first()
        item['price_unit'] = re.findall('(\w+)',re.findall("\"priceCurrency\"(.*)",js)[0])[0]
        item['price'] = re.findall('([0-9.]+)',re.findall("\"price\"(.*)",js)[0])[0]
        yield item
