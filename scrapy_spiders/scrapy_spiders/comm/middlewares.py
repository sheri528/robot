# -*- coding: utf-8 -*-
import logging
import re

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
        if not re.search('192\.168\.\d{1,3}\.\d{1,3}', request.url):
            try:
                proxy_response = requests.get(api_proxy)
            except Exception as e:
                logger.error("proxy Error: {}".format(e))
            else:
                if proxy_response.status_code == 200:
                    proxy = proxy_response.text
                    request.meta['proxy'] = ''.join(['http://', proxy])
                    logger.info("proxy. Success: {0}, {1}".format(request.url, request.meta['proxy']))

                else:
                    logger.info("proxy is not OK. Error: {0}".format(proxy_response.text))

                if hasattr(spider, 'proxy_count'):
                    spider.proxy_count[proxy_response.status_code] = \
                        spider.proxy_count.get(proxy_response.status_code, 0) + 1

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
