#-- coding: utf-8 --
import matplotlib.pyplot as plt
from numpy_learn import numpy_test as npt
from numpy import *

def matplotlib_learn_001():
    plt.plot([1, 2, 3], [4, 2, 5])
    plt.show()


def matplotlib_learn_002():
    plt.plot([1, 2, 4, 4], 'r')
    plt.ylabel('some numbers')  # 为y轴加注释
    plt.show()


def matplotlib_learn_003():
    dating_data_mat, dating_labels = npt.file2matrix(
        "/Users/fan/Develop/Own_Workspace/Workspace_Python/PycharmProjects/2019_pycharm_python_test/resource/datingTestSet2.txt")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # 设置整个表格的标题
    ax.set_title('矩阵图')
    # 设置横坐标标题
    ax.set_xlabel(u'玩视屏游戏所消耗时间百分比')
    # 设置纵坐标标题
    ax.set_ylabel(u'每周消费的冰激凌公升数')
    # ax.scatter(dating_data_mat[:, 1], dating_data_mat[:, 2])
    ax.scatter(dating_data_mat[:, 1], dating_data_mat[:, 2],
               15.0 * array(dating_labels), 15.0 * array(dating_labels))
    plt.show()


if __name__ == '__main__':
    # matplotlib_learn_001()
    # matplotlib_learn_002()
    matplotlib_learn_003()