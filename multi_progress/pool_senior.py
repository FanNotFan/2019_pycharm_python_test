#!/usr/bin/env python
# encoding: utf-8
'''
@author: lennon
@license: (C) Copyright 2019-2020, Node Supply Chain Manager Corporation Limited.
@contact: v-lefan@expedia.com
@software: pycharm
@file: pool_senior.py
@time: 2019-10-10 15:44
@desc: 当返回值是True False 时
@ref: https://thief.one/2016/11/24/Multiprocessing%E5%AD%90%E8%BF%9B%E7%A8%8B%E8%BF%94%E5%9B%9E%E5%80%BC/
'''

'''
    说明：总共要执行50000个子进程（并发数量为10），当其中一个子进程返回True时，结束进程池。因为使用了apply_async为异步进程，因此在执行完for循环的添加子进程操作后（只是添加并没有执行完所有的子进程），可以直接执行while代码，实时判断子进程返回值是否有True，有的话结束所有进程。

    优点：不必等到所有子进程结束再结束程序，只要得到想要的结果就可以提前结束，节省资源。
    
    不足：当需要执行的子进程非常大时，不适用，因为for循环在添加子进程时，要花费很长的时间，虽然是异步，但是也需要等待for循环添加子进程操作结束才能执行while代码，因此会比较慢。
'''
from multiprocessing import Pool
from queue import Queue
import time


def test(p):
    time.sleep(0.001)
    if p == 10000:
        return True
    else:
        return False


if __name__ == "__main__":
    pool = Pool(processes=10)
    q = Queue()
    for i in range(50000):
        '''
        将子进程对象存入队列中。
        '''
        q.put(pool.apply_async(test, args=(i,)))  # 维持执行的进程总数为10，当一个进程执行完后添加新进程.
    '''
    因为这里使用的为pool.apply_async异步方法，因此子进程执行的过程中，父进程会执行while，获取返回值并校验。
    '''
    while 1:
        if q.get().get():
            pool.terminate()  # 结束进程池中的所有子进程。
            break

    pool.close()
    pool.join()
