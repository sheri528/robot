# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import json
import time
import urllib

import scrapy
from scrapy_spiders.items import GrabItem

class EbaySpider(scrapy.Spider):
    '''
        Go through ever sub sit in ebay, fetch data and sending via email.
        Args:
            -keyword- Search word. Using "hello word" instead for None
        Run:
        >>scrapy crawl ebay -a keyword=xxx
    '''
    name = "ebay"
    sku_ids = set()

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_spiders.pipelines.XmlExportPipeline': 100,
            'scrapy_spiders.pipelines.EbaySendingEmailPipeline': 999,
        },
    }

    def __init__(self, keyword=None, *args, **kwargs):
        if keyword:
            self.keyword = keyword
        else:
            self.keyword = 'hello world'

    def start_requests(self):
        url = "https://www.ebay.com/"
        request = scrapy.Request(url=url, callback=self.parse)
        yield request

    def parse(self, response):
        ''' send requests per sub-ebay-site '''
        ebay_sites = response.xpath('//div[@id="gf-f"]/ul/li/a/@href').extract()
        for url in ebay_sites:
            request = scrapy.Request(url=url, callback=self.parse_site_index)
            yield request

    def parse_site_index(self, response):
        ''' search keywords '''

        # form url
        form_url = response.xpath('//form[@id="gh-f"]/@action|//form/@action').extract_first()
        # hidden parameter
        inputs = response.xpath('//input')
        name_value = {}
        for i in inputs:
            name = i.xpath('@name').extract_first()
            value = i.xpath('@value').extract_first()
            if name and value:
                name_value[name] = value
        # k_name is parameter for search bar
        k_name = response.xpath('//input[@id="gh-ac"]/@name').extract_first()
        if name_value and k_name and form_url:
            name_value[k_name] = self.keyword
            url = ''.join([form_url, "?", urllib.urlencode(name_value)])
            request = scrapy.Request(url=url, callback=self.parse_keyword_list)
            yield request

    def parse_keyword_list(self, response):
        item_list = response.xpath('//ul[@id="ListViewInner"]/li')
        Num_per_page = len(item_list)
        try:
            page = response.meta['page']
        except :
            page = 1

        for i, p in enumerate(item_list):
            item = GrabItem()
            # item['position'] = i + 1
            # item['page'] = page
            # item['category_index'] = (page - 1)*Num_per_page + i + 1
            item['sku_id'] = p.xpath('@id').extract_first()
            if item['sku_id'] and item['sku_id'].strip() not in self.sku_ids:
                self.sku_ids.add(item['sku_id'].strip())
            else:
                continue
            item['name'] = p.xpath('h3/a/text()').extract_first().strip()
            item['product_url'] = p.xpath('h3/a/@href').extract_first().strip()
            if item['product_url']:
                request = scrapy.Request(url=item['product_url'],
                                         meta={'item': item},
                                         callback=self.parse_detail)
                yield request
        # request for next page
        if page == 1:
            total_num = response.xpath('//span[@class="rcnt"]/text()').re_first('[0-9,]{1,}')
            total_num = int(re.sub(',', '', total_num)) if total_num else 1
            total_page = total_num/Num_per_page + 1 if total_num%Num_per_page else total_num/Num_per_page
            while page < total_page:
                page += 1
                url = ''.join([response.url, "&_pgn={}".format(page)])
                request = scrapy.Request(url=url,
                                         meta={'page': page},
                                         callback=self.parse_keyword_list)
                yield request

    def parse_detail(self, response):
        item = response.meta['item']

        store_id = response.xpath('//span[@class="mbg-nw"]/text()').extract_first()
        if store_id:
            item['store_id'] = store_id.strip()
        else:
            self.logger.info('no store id: {}'.format(item['product_url']))
        try:
            name = response.xpath('//title/text()').extract_first()
            item['name'] = name.split('|')[0] if name else ''
        except Exception as e:
            self.logger.error("name Error : {e}, url : {url}".format(e=e, url=item['product_url']))
        yield item
