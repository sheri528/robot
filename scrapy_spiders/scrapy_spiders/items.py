# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class GrabItem(scrapy.Field):
    sku_id = scrapy.Field()
    name = scrapy.Field()
    product_url = scrapy.Field()
    store_id = scrapy.Field()
