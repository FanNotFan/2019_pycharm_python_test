from numpy import *
import operator
from numpy_learn import numpy_test as npt
from os import listdir


# k-近邻算法
def classify0(inx, dataset, labels, k):
    # shape函数是numpy.core.fromnumeric中的函数，它的功能是查看矩阵或者数组的维数
    dataset_size = dataset.shape[0]

    # numpy.tile(A,B)函数 重复A，B次
    diff_mat = tile(inx, (dataset_size, 1)) - dataset

    sq_diff_mat = diff_mat ** 2
    sq_distances = sq_diff_mat.sum(axis=1)
    distances = sq_distances ** 0.5
    sorted_dist_indiceies = distances.argsort()
    class_count = {}
    for i in range(k):
        vote_ilabel = labels[sorted_dist_indiceies[i]]
        class_count[vote_ilabel] = class_count.get(vote_ilabel, 0) + 1
    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]


# 归一化特征值：将取值范围处理为0到1或者-1到1之间
def auto_norm(data_set):
    # 从列中选取最小值，放入 min_vals
    min_vals = data_set.min(0)
    # 每列最大值放入 max_vals
    max_vals = data_set.max(0)
    ranges = max_vals - min_vals

    # shape 建立一个单位矩阵，zeros 其他全部归0
    norm_data_set = zeros(shape(data_set))

    # 求数组的行数
    m = data_set.shape[0]

    # tile(A,B) 重复A，B次
    norm_data_set = data_set - tile(min_vals, (m, 1))
    norm_data_set = norm_data_set/tile(ranges, (m, 1))
    return norm_data_set, ranges, min_vals


# 验证分类器
def datingClassTest():
    hoRatio = 0.10
    dating_data_mat, dating_labels = npt.file2matrix("/Users/fan/Develop/Own_Workspace/Workspace_Python/PycharmProjects/2019_pycharm_python_test/resource/datingTestSet2.txt")
    norm_mat, ranges, min_vals = auto_norm(dating_data_mat)
    m = norm_mat.shape[0]
    # hoRatio 是随机取取 10% 的数据
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(norm_mat[i, :], norm_mat[numTestVecs:m, :],
                                     dating_labels[numTestVecs:m], 3)
        print("came back: %d,real answer: %d" % (classifierResult, dating_labels[i]))
        if(classifierResult != dating_labels[i]): errorCount += 1.0
    print("error rate is: %f " % (errorCount/float(numTestVecs)))


def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('/Users/fan/Develop/Own_Workspace/Workspace_Python/PycharmProjects/2019_pycharm_python_test/resource/digits/trainingDigits')           #load the training set
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = npt.img2vector('/Users/fan/Develop/Own_Workspace/Workspace_Python/PycharmProjects/2019_pycharm_python_test/resource/digits/trainingDigits/%s' % fileNameStr)
    testFileList = listdir('/Users/fan/Develop/Own_Workspace/Workspace_Python/PycharmProjects/2019_pycharm_python_test/resource/digits/testDigits')        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = npt.img2vector('/Users/fan/Develop/Own_Workspace/Workspace_Python/PycharmProjects/2019_pycharm_python_test/resource/digits/testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr))
        if (classifierResult != classNumStr): errorCount += 1.0
    print("\nthe total number of errors is: %d" % errorCount)
    print("\nthe total error rate is: %f" % (errorCount/float(mTest)))


if __name__ == '__main__':
    # group, lables = npt.creatDataset()
    # result = classify0([0.8, 0.8], group, lables, 3)
    # print(result)
    # datingClassTest()
    handwritingClassTest()

