# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from functools import wraps


def check_response(func):
    @wraps(func)
    def is_normal(*args, **kwargs):
        '''
            :args[0] self
            :args[1] response
            Could be used to check proxy. or do things like replace response body.
                args[1]._encoding = 'utf-8'
                args[1]._set_body(xxx)
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

def check_proxy(func):
    @wraps(func)
    def is_normal(*args, **kwargs):
        '''
            统计proxy响应状态。spider需要设置属性proxy_count为dict类型
            :args[0] self
            :args[1] response
        '''
        origin_func = func(*args, **kwargs)
        try:
            use_proxy = args[1].request.meta.get('proxy', None)
            response_status = args[1].status
            if use_proxy and response_status in [200, 600]:
                args[0].proxy_count[response_status] = args[0].proxy_count.get(response_status, 0) + 1
        except Exception as e:
            import traceback
            traceback.print_exc()
        return origin_func

    return is_normal


def timethis(func):
    '''
        Decorator that limits the execution period not less than 10s.
    '''

    _last_time = [0]

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        if _last_time[0] == 0 or start - _last_time[0] > 10:
            result = func(*args, **kwargs)
            _last_time[0] = start
            print("success. call {0}, time is {1}".format(func.__name__, _last_time[0]))
            return result
        else:
            print("limit call 10s, last call time is {0}".format(_last_time[0]))

    return wrapper

# @timethis
# def func(n):
#     for i in range(n):
#         pass
#
# func(400)
# func(2)
# time.sleep(10)
# func(30)
