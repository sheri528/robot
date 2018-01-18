# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

import requests
import scrapy
from selenium import webdriver

driver = webdriver.PhantomJS()
# maybe get sku_id, page_url from database
page_urls = ["http://www.shein.com/Frayed-Trim-Asymmetric-Zip-Tweed-Jacket-p-409971-cat-1776.html", ]
sku_ids = [409971, ]


url = "http://sheinsz.ltwebstatic.com/js/category.js?v=shein_661"
js_cnt = requests.get(url).text

for sid, purl in zip(sku_ids, page_urls):
    driver.get(purl)
    driver.execute_script(js_cnt, "update_product_price({})".format(sid))
    response_body = driver.page_source
    selenium_response = scrapy.http.TextResponse(url=purl, encoding='utf-8', body=response_body, request=purl)
    if selenium_response:
        price = selenium_response.xpath('//div[@id="special_price_u"]/@price').re_first('[0-9]{1,}\.*[0-9]*')
        if not price:
            price = selenium_response.xpath('//div[@id="shop_price_u"]/@price').re_first('[0-9]{1,}\.*[0-9]*')
    # maybe compare with price saved in database
    print(price)

driver.quit()