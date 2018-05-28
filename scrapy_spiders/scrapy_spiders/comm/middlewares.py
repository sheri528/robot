# -*- coding: utf-8 -*-
import logging

import requests
import random
import scrapy
from scrapy.exceptions import CloseSpider

from agents import AGENTS
from scrapy_spiders.settings import api_proxy

logger = logging.getLogger(__name__)

class CustomUserAgentMiddleware(object):

    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent


class AddProxyMiddleware(object):

    def process_request(self, request, spider):
        try:
            request.meta['proxy'] = ''.join(['http://', requests.get(api_proxy).text])
            # request.meta['dont_filter'] = True
            logger.info("proxy. Success: proxy: {0}, request url: {1}".format(request.meta['proxy'], request.url))
        except Exception as e:
            logger.info("no proxy. Error: {0}".format(e))
        return None


class ItemLimitedMiddleware(object):
    '''
        抓取数量为spider.push_num
    '''
    def process_spider_output(self, response, result, spider):
        def _count_items(item):
            if isinstance(item, (scrapy.item.Item, scrapy.item.ItemMeta)) and not item.get('update', None) and hasattr(spider, 'push_num') and isinstance(getattr(spider, 'push_num'), int):
                if spider.push_num > 0:
                    spider.push_num -= 1
                    logger.info("====push_num : {}".format(spider.push_num))
                    return True
                elif spider.push_num == 0:
                    raise CloseSpider(reason="item exceed push_num")
                    # return False
            else:
                return True


        res_gen = (r for r in result or () if _count_items(r))
        return res_gen
