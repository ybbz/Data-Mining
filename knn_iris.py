import numpy as np
import scipy.spatial.distance as ssd

"""
本文将3个类别150条Iris数据，每个类别选取10条作为测试数据集，剩余数据为训练数据集；
这样，训练集（iris_train）120条数据，测试集（iris_test）30条数据。
"""

# 读取数据集文件并处理
def read_file(file):
    # 读取数据并初步处理(,)
    with open(file) as f:
        data_rows = np.loadtxt(f, delimiter=',', dtype='float', skiprows=0, usecols=None, unpack=False)
    data_property = []  # 属性
    data_category = []  # 分类
    # 分离读取数据的属性和分类
    for row in data_rows:
        data_property.append(row[:-1])
        data_category.append(int(row[-1]))
    return np.array(data_property), np.array(data_category)


# K最近邻(kNN，k-NearestNeighbor)分类算法
def knn(k, proper_train, proper_test, cate_train):
    cate_predict = []  # 初始化数组,保存kNN算法计算的分类结果
    # 遍历测试数据集,并计算其中每条数据与训练数据集中数据的距离
    for di in proper_test:
        distances = []
        for ij, dj in enumerate(proper_train):  # enumerate函数用于遍历序列中的元素以及它们的下标
            distances.append((ssd.euclidean(di, dj), ij))  # euclidean函数计算di和dj的欧氏距离
        # 距离排序,并根据k值做取舍
        k_nn = sorted(distances)[:k]
        # 根据训练集的分类值来为测试集分类
        cate_collect = []  # k个最近邻居的分类
        for distance, i_train in k_nn:
            cate_collect.append(cate_train[i_train])
        # np.argmax,np.bincount计算(非负整数)数组中每个值的出现次数,返回次数最大的那个值
        cate_predict.append(np.argmax(np.bincount(cate_collect)))
    return cate_predict


# 对测试数据集分类结果的评价
def evaluate(result):
    # np.zeros返回一个给定形状和数据类型的新数组(值为零)
    eval_result = np.zeros((2,), dtype=np.int)
    for x in result:
        if x == 0:  # 分类正确
            eval_result[0] += 1
        else:  # 分类错误
            eval_result[1] += 1
    return eval_result


# iris训练集:property_train(属性),category_train(类别)
property_train, category_train = read_file('/Users/ybbz/Desktop/iris/iris_train.txt')

# iris测试集:property_test(属性),category_test(类别)
property_test, category_test = read_file('/Users/ybbz/Desktop/iris/iris_test.txt')

# 选取几种不同的k值进行比较测试
K = [1, 3, 7, 11]

print("kNN算法分类结果(Iris数据集):\n")
print("k    | 正确分类数/错误分类数")

for k in K:
    category_predict = knn(k, property_train, property_test, category_train)
    evaluate_result = evaluate(category_predict - category_test)
    print(k, "   | ", evaluate_result[0], "/", evaluate_result[1])

