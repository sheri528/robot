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

class CategoryItem(scrapy.Field):
    category_name = scrapy.Field()
    category_url = scrapy.Field()
    refer = scrapy.Field()

class GrabPriceItem(GrabItem):
    price = scrapy.Field()
    price_unit = scrapy.Field()