# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import scrapy
from scrapy_spiders.items import CategoryItem
from scrapy_spiders.comm.misc import check_response

class SammydressCategorySpider(scrapy.Spider):

    name = "sammydress_category"
    category_set = set()

    def __init__(self):
        pass

    def start_requests(self):
        start_url = "https://www.sammydress.com/sitemap/category-sitemap.xml"
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        for p in scrapy.Selector(text=response.body).xpath('//url'):
            p_num = p.xpath('priority/text()').extract_first()
            url = p.xpath('loc/text()').extract_first()
            if p_num == u'0.7' and url not in self.category_set:
                yield scrapy.Request(url, callback=self.parse_category)

    @check_response
    def parse_category(self, response):
        navlist = response.xpath('//div[@class="cateB-wrap depart-now-navlist"]/ul/li/ul/li')
        cate_wrap = response.xpath('//div[@id="js_cateWrap"]/div/span/a/strong/text()').extract()

        for n in navlist:
            if not n.xpath('ul').extract_first():
                continue
            else:
                for a in n.xpath('ul/li/p/a'):
                    category_names = cate_wrap[1:]
                    last_name = a.xpath('text()').extract_first()
                    category_names.append(last_name)
                    temp_name = ' > '.join(category_names)
                    temp_url = a.xpath('@href').extract_first()
                    if temp_url not in self.category_set:
                        self.category_set.add(temp_url)
                        item = CategoryItem()
                        item['category_name'] = temp_name
                        item['category_url'] = temp_url
                        item['refer'] = response.url
                        category_names = []
                        yield item
                else:
                    break




