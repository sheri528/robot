# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import wraps

def check_response(func):
    @wraps(func)
    def is_normal(*args, **kwargs):
        '''
            :args[0] self
            :args[1] response
        '''
        origin_func = func(*args, **kwargs)
        page_source = args[1].body
        try:
            if args[1].status == 200:
                args[0].logger.info("=====response 200")
            else:
                args[0].logger.info("====not OK. response: {code}, {url}".format(code=args[1].status, url=args[1].url))
        except Exception as e:
            import traceback
            traceback.print_exc()
        return origin_func

    return is_normal

