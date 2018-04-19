# -*- coding: utf-8 -*-
import logging

import requests
import random

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
            logger.info("proxy. Success: {0}".format(request.url))
        except Exception as e:
            logger.info("no proxy. Error: {0}".format(e))
        return None
