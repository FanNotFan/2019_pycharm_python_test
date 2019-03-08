import numpy as np


# Numpy基本操作
def np_base_operate():
    a = np.array([[1, 2], [3, 4], [5, 6]])

    print(a)

    # 维度,输出: 2
    print(a.ndim)

    # 行数和列数  (3, 2)
    print(a.shape)

    # 元素个数 6
    print(a.size)


## Numpy的数组(Array)
def np_array_operate():
    a = np.array([1, 2, 3])  # 创建一维数组
    print(type(a))           # 输出 "<class 'numpy.ndarray'>"
    print(a[0], a[1], a[2])  # 输出 "1 2 3"
    a[0] = 8                 # 修改数组某元素的值
    print(a[0])              # 输出 "8"

    # 其他创建数组的方法
    b = np.zeros((2, 2))
    print(b)                # 输出 "[[ 0.  0.]
                            #       [ 0.  0.]]"
    c = np.ones((1, 2))
    print(c)                # 输出 "[[ 1.  1.]"

    d = np.eye(2)           # 创建单位矩阵
    print(d)                # 输出 "[[ 1.  0.]
                            #       [ 0.  1.]]"

    e = np.random.random((2, 2)) # 随机值
    print(e)


# Numpy的数组(Array)
# 创建numpy数组
def np_array_operate_2():
    a = np.array([1, 2, 3])  # 创建一维数组
    print(type(a))           # 输出 "<class 'numpy.ndarray'>"
    print(a[0], a[1], a[2])  # 输出 "1 2 3"
    a[0] = 8                 # 修改数组某元素的值
    print(a[0])              # 输出 "8"

    # 其他创建数组的方法
    b = np.zeros((2, 2))
    print(b)                # 输出 "[[ 0.  0.]
                            #       [ 0.  0.]]"
    c = np.ones((1, 2))
    print(c)                # 输出 "[[ 1.  1.]"

    d = np.eye(2)           # 创建单位矩阵
    print(d)                # 输出 "[[ 1.  0.]
                            #       [ 0.  1.]]"
    e = np.random.random((2, 2)) # 随机值
    print(e)                # 输出 "[[0.29027784 0.01445969]
                            #       [0.76571518 0.75046783]]"


# 数组索引
def np_array_operate_3():
    # 切片：和Python列表类似，numpy数组也可以使用切片语法。
    # 由于数组可能是多维的，因此必须为数组的每个维指定切片。

    # 创建一个二维数组(矩阵更容易理解)，shape为 (3，2)
    # [1,7]
    # [3,4]
    # [5,6]
    a = np.array([[1, 7], [3, 4], [5, 6]])

    # 下面操作相当于取 a[1, 1]
    print(a)
    b = a[:1, 1:2]
    print(b)        # 输出"[[7]]"

    # 可以同时使用整型和切片语法来访问数组。这样做会产生比原数组低阶的新数组。
    row_r1 = a[1, :]
    row_r2 = a[1:2, :]
    print(row_r1, row_r1.shape)  # Prints "[3 4] (2,)"
    print(row_r2, row_r2.shape)  # Prints "[[3 4]] (1, 2)"

    # 使用切片语法访问数组时，得到的总是原数组的一个子集
    # 整型数组访问允许我们利用其它数组的数据构建一个新的数组
    a1 = np.array([[1, 2], [3, 4], [5, 6]])

    print(a1[[0, 1, 2], [0, 1, 0]])  # Prints "[1 4 5]"
    # 等价于以下操作
    print(np.array([a1[0, 0], a1[1, 1], a1[2, 0]]))

    # 布尔型数组访问：布尔型数组访问可以让你选择数组中任意元素
    # 这种访问方式用于选取数组中满足某些条件的元素
    a2 = np.array([[1, 2], [3, 4], [5, 6]])
    b2 = (a > 2)
    print(b2)
    print(a2[b2])  # 输出 "[3 4 5 6]"
    # 等价于
    print(a[a > 2])  # 输出 "[3 4 5 6]"


# numpy 数据类型
def np_datatype_opreate():
    x1 = np.array([1, 2])                   # numpy选择类型
    print(x1.dtype)                         # 输出"int32"

    x2 = np.array([1.0, 2.0])               # numpy选择类型
    print(x2.dtype)                         # 输出"float64"

    x3 = np.array([1, 2], dtype=np.int64)   # 指定类型
    print(x3.dtype)                         # 输出"int64"


# numpy 数组计算
def np_array_calculate():
    x = np.array([[1, 2], [3, 4]], dtype=np.float64)
    y = np.array([[5, 6], [7, 8]], dtype=np.float64)

    # 按元素相加，产生的还是同样shape的数组
    # 输出 "[[ 6.  8.]
    #       [10. 12.]]"
    print(x + y)
    print(np.add(x, y))

    # 按元素相减
    # 输出 "[[ 6.  8.]
    #       [10. 12.]]"
    print(x - y)
    print(np.subtract(x, y))

    # 按元素相乘
    # 输出 "[[ 5. 12.]
    #       [21. 32.]]"
    print(x * y)
    print(np.multiply(x, y))

    # 按元素相除
    # 输出 "[[0.2        0.33333333]
    #        [0.42857143 0.5       ]]"
    print(x / y)
    print(np.divide(x, y))

    # 开平方
    # 输出 "[[1.         1.41421356]
    #        [1.73205081 2.        ]]"
    print(np.sqrt(x))

    # numpy矩阵乘法
    x = np.array([[1, 2], [3, 4]])
    y = np.array([[5, 6], [7, 8]])

    v = np.array([9, 10])
    w = np.array([11, 12])

    # 向量的内积，输出：219
    print(v.dot(w))
    print(np.dot(v, w))

    # 向量/矩阵乘积
    # 输出 "[29 67]"
    print(x.dot(v))
    print(np.dot(x, v))

    # 矩阵/矩阵乘积
    # 输出 "[[19 22]
    #       [43 50]]"
    print(x.dot(y))
    print(np.dot(x, y))

    # 求和函数sum
    x = np.array([[1, 2], [3, 4]])
    print(np.sum(x))  # 所有元素相加，输出"10"
    print(np.sum(x, axis=0))  # 按列相加，输出"[4 6]"
    print(np.sum(x, axis=1))  # 按行相加，输出"[3 7]"

    # 转置操作
    x = np.array([[1, 2], [3, 4]])
    print(x)    # 输出   "[[1 2]
                #        [3 4]]"
    print(x.T)  # 输出   "[[1 3]
                #        [2 4]]"


# 广播机制(Broadcasting)
def np_broadcasting():
    # 把一个向量加到矩阵的每一行，可以这样做
    x = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    v = np.array([1, 0, 1])
    y = np.empty_like(x)  # 创建一个空矩阵，shape和x一致

    for i in range(3):
        y[i, :] = x[i, :] + v
    print(y)

    #  输出
    # [[ 2  2  4]
    # [ 5  5  7]
    # [ 8  8 10]]

    # 当x矩阵非常大，利用循环来计算就会变得很慢很慢
    # 换一种思路
    vv = np.tile(v, (3, 1))  # 将v复制三次堆叠在一起
    print(vv)  # 输出    "[[1 0 1]
    #          [1 0 1]
    #          [1 0 1]"

    y = x + vv  # 按元素相加
    print(y)

    # Numpy广播机制让我们不用创建vv，就能直接运算
    y = x + v  # 使用广播将v添加到x的每一行
    print(y)


# 广播机制例子
# 1.计算向量的外积
def np_broadcasting_2():
    # 广播机制例子
    # 1.计算向量的外积

    v = np.array([1, 2, 3])  # v 的shape (3,) 一行三列
    w = np.array([4, 5])  # w 的shape (2,)
    #  首先将v转化成(3, 1) 3行1列, 然后广播
    print(np.reshape(v, (3, 1)))
    #  输出的shape为(3, 2)
    # [[ 4  5]
    #  [ 8 10]
    #  [12 15]]
    print(np.reshape(v, (3, 1)) * w)
    # 2.向矩阵的每一行添加一个向量
    x = np.array([[1, 2, 3], [4, 5, 6]])
    # x的shape为（2,3），v的shape为（3，），因此它们广播得到（2,3）
    #  输出:
    # [[2 4 6]
    #  [5 7 9]]
    print(x + v)

    # 3.向矩阵的每一列添加一个向量
    # x 的shape (2, 3) and w的shape (2,).
    # 　转置x的shape（3,2），针对w广播以产生形状的结果（3,2）
    # 输出:
    # [[ 5  6  7]
    #  [ 9 10 11]]
    print((x.T + w).T)

    # 4.另一个解决方案是将w重塑shape为（2,1）
    # 然后可以直接对x广播它以产生相同的效果
    # 输出
    print(x + np.reshape(w, (2, 1)))

    # 5.用常数乘以矩阵
    # 输出:
    # [[ 2  4  6]
    #  [ 8 10 12]]
    print(x * 2)

if __name__ == '__main__':
    # np_array_operate_2()
    # np_array_operate_3()
    # np_broadcasting()
    np_broadcasting_2()