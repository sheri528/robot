# -*- coding: utf-8 -*-
import os
import logging
from concurrent.futures import ThreadPoolExecutor
from scrapy import cmdline
from subprocess import call

logger = logging.getLogger(__name__)

def func(url):
    try:
        '''
            1.os.system 调用系统内部命令。与os.exec的区别是 os.exec会接管进程的控制权. os.system会隐式调用shell

             system(...)
                system(command) -> exit_status

                Execute the command (a string) in a subshell.

            2.subprocess模块的call()/check_all()可以替代os.system.

                对于call函数，将会直接调用命令生成子进程，并且等待子进程结束，然后返回子进程的返回值
                check_call函数来说，和call函数的主要区别在于如果返回值不为0，则触发CallProcessError异常

            3.cmdline.execute() 必须以主线程运行
        '''
        r = call("scrapy crawl spider_name -a url={0} --logfile _20180518.log -L DEBUG".format(url))
    except Exception as e:
        import traceback
        traceback.print_exc()

def main(filename):
    '''
        max_workers=4
        url.csv:
        http://url.com
    '''
    with ThreadPoolExecutor(max_workers=4) as executor:
        for line in open(filename, 'r'):
            url = line.split(',')[0].strip()
            r = executor.submit(func, url)


if __name__ == '__main__':
    main('url.csv')


