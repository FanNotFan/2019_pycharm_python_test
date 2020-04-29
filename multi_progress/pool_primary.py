#!/usr/bin/env python
# encoding: utf-8
'''
@author: lennon
@license: (C) Copyright 2019-2020, Node Supply Chain Manager Corporation Limited.
@contact: v-lefan@expedia.com
@software: pycharm
@file: pool.py
@time: 2019-10-10 10:49
@desc:
@ref: https://jingsam.github.io/2015/12/31/multiprocessing.html
'''

from multiprocessing import Manager, Pool, freeze_support, cpu_count


def worker(procnum, return_dict):
    '''worker function'''
    print(str(procnum) + ' represent!')
    return_dict[procnum] = procnum


if __name__ == "__main__":
    # Windows 平台要加上这句，避免 RuntimeError
    freeze_support()
    manager = Manager()
    return_dict = manager.dict()
    cpus = cpu_count()
    # Pool默认大小是CPU的核数，我们也可以通过在Pool中传入processes参数即可自定义需要的核数量
    pool = Pool(processes=10)
    result = []
    for i in range(500000):
        '''
        for循环执行流程：
        （1）添加子进程到pool，并将这个对象（子进程）添加到result这个列表中。（此时子进程并没有运行）
        （2）执行子进程（同时执行10个）
        '''
        result.append(pool.apply_async(worker, args=(i, return_dict)))  # 维持执行的进程总数为10，当一个进程执行完后添加新进程.

    '''
        最后我们使用一下语句回收进程池
    '''
    pool.close()
    pool.join()
    '''
    获取返回值的过程最好放在进程池回收之后进行，避免阻塞后面的语句
    遍历result列表，取出子进程对象，访问get()方法，获取返回值。（此时所有子进程已执行完毕）
    '''
    print(return_dict.values())
    # for i in result:
    #     print(i.get())
