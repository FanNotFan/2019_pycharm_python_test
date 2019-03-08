
'''
    append() 方法  执行完后a的第四个元素也是数组
    结果：
        resultA : %s [1, 2, 3, [4, 5, 6, 7]]
'''
def append_method():
    a = [1, 2, 3]
    b = [4, 5, 6, 7]

    a.append(b)
    print("resultA : %s", a)


'''
    原生extend 方法： 执行完后是一个包含全部的元素列表
    结果：
        resultB : %s [1, 2, 3, 4, 5, 6, 7]
'''
def extend_method():
    c = [1, 2, 3]
    d = [4, 5, 6, 7]
    c.extend(d)
    print("resultB : %s", c)

