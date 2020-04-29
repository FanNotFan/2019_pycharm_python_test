#!/usr/bin/env python
# encoding: utf-8
'''
@author: lennon
@license: (C) Copyright 2019-2020, Node Supply Chain Manager Corporation Limited.
@contact: v-lefan@expedia.com
@software: pycharm
@file: process_primary.py
@time: 2019-10-12 15:17
@desc:
'''

import multiprocessing
from multiprocessing import Manager, freeze_support


def worker(procnum, return_dict):
    '''worker function'''
    print(str(procnum) + ' represent!')
    return_dict[procnum] = procnum


if __name__ == '__main__':
    freeze_support()
    manager = Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range(5000000):
        p = multiprocessing.Process(target=worker, args=(i, return_dict))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()
    # 最后的结果是多个进程返回值的集合
    print(return_dict.values())
