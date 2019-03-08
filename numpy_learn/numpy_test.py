from numpy import *
from knn import kNN_test as knnt


# 模拟数据
def creatDataset():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


# 将文本记录转换为numpy 的解析程序,将文件数据转换成矩阵
def file2matrix(filename):
    fr = open(filename)
    array_o_lines = fr.readlines()
    number_of_lines = len(array_o_lines)
    return_mat = zeros((number_of_lines, 3))
    class_label_vector = []
    index = 0
    for line in array_o_lines:
        # 去除回车
        line = line.strip()
        # 使用spilt分割成一个数组
        list_from_line = line.split('\t')
        return_mat[index, :] = list_from_line[0:3]
        class_label_vector.append(int(list_from_line[-1]))
        index += 1
    return return_mat, class_label_vector


# 将图片转为向量
def img2vector(filename):
    returnVect = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32*i+j] = int(lineStr[j])
    return returnVect


if __name__ == '__main__':
    # group, lables = creatDataset()
    # print(group)
    # print(lables)

    dating_data_mat, dating_labels = file2matrix(
        "/Users/fan/Develop/Own_Workspace/Workspace_Python/PycharmProjects/2019_pycharm_python_test/resource/datingTestSet2.txt")
    # print(dating_data_mat)
    # print(dating_labels)

    norm_mat, ranges, min_vals = knnt.auto_norm(dating_data_mat)
    print(norm_mat)
    print(ranges)
    print(min_vals)

