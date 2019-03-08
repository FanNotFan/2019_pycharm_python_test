from KNearestNeighbors.knn import kNN_test as knt
from KNearestNeighbors.numpy_learn import numpy_test as npt
from numpy import *

# 根据学习数据，从看视屏电影、获得飞行里程数、吃冰激凌 定义是否喜欢一个人
def classifyPerson():
    resultList = ['not at all', 'in small does', 'in large does']
    percentTats = float(input("percentage of time spent playing video games?"))
    ffMiles = float(input("frequent flier miles earned per year?"))
    iceCream = float(input("liters of ice cream consumed per year"))

    return_mat, class_label_vector = npt.file2matrix(
        "/Users/fan/Develop/Own_Workspace/Workspace_Python/PycharmProjects/2019_pycharm_python_test/resource/datingTestSet2.txt")
    normMat, ranges, minVals = knt.auto_norm(return_mat)
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = knt.classify0((inArr-minVals)/ranges, normMat, class_label_vector, 3)
    print("you will probably like this person: ", resultList[classifierResult -1])


if __name__ == '__main__':
    classifyPerson()

