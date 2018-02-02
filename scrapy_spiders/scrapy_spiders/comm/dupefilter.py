# -*-coding:utf-8-*-
import random
import time

from scrapy.dupefilters import RFPDupeFilter

class DupefilterMiddleware(RFPDupeFilter):
    """
        Use time stamp + random to prevent fragment(#) url filtered.
    """

    def request_fingerprint(request, nn):
        a = random.uniform(0, 50000000)
        t = time.time()
        return ''.join([str(a), str(t)])
