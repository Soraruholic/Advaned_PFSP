import math
import random
import numpy as np
from datetime import datetime, timedelta
from solver import Solver
from population import Population
import localSearch
from GeneticAlgorithm import GeneticAlgorithm
from Climb import Climb
from SimulatedAnnealing import SimulatedAnnealing
from chromes import initializeChromes, selectChromes, crossChromes, muteChromes
import loadData
import NEH
import selection
import chromes
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
# 定义出入数据的函数，由于测试样例格式特殊，单独定义
def loadingData() :
    path = "../flowshop-test-10-student"
    f = open (path + ".txt", "r")
# 读入实例中样例的总个数
# 初始化读入列表
    instances = list()
    instance = list()
    for i in range (11):
        instance.clear()
# 跳过无用行
        f.readline()
        f.readline()
# 读取工序个数与机器个数
        n, m = [int (item) for item in f.readline().split()]
# 开始迭代读取样例
        for j in range (n):
            line = [int (item) for item in f.readline().split()]
            line = line[1::2]
            instance.append (line.copy())
# 将样例转化为int32数据类型
        instances.append (np.array (instance.copy(), dtype = 'int32'))    
    return instances
# 定义爬山法的解决器
def HillClimbing ():
    print ("下面进行爬山法求解PFSP问题:")
# 加载数据
    instances = loadingData ()
# 初始化最优解列表
    best_makespans = list()
    best_permutations = list()
# 遍历所有样例求解
    for index, instance in enumerate(instances):
        ig = Climb(instance)
        ig.tie_breaking = True
        ig.max_loop = 20000
        ig.eval(20000)
        best_makespans.append (ig.best_solver.makespan)
        best_permutations.append (ig.best_solver.permutation)
        print("Instance " + str(index) + " 最优时间跨度为:", ig.best_solver.makespan)
        print("\t相应的一个最优排列为:", ig.best_solver.permutation)
    return best_makespans, best_permutations
def simulatedAnnealing ():
    print ("下面进行模拟退火法求解PFSP问题:")
# 加载数据
    instances = loadingData ()
# 初始化最优解列表
    best_makespans = list()
    best_permutations = list()
# 遍历所有样例求解
    for index, instance in enumerate(instances):
        ig = SimulatedAnnealing(instance)
# 打开邻域搜索
        ig.local_search = True
        ig.max_loop = 20000
        ig.eval(10000)
        best_makespans.append (ig.best_solver.makespan)
        best_permutations.append (ig.best_solver.permutation)
        print("Instance " + str(index) + " 最优时间跨度为:", ig.best_solver.makespan)
        print("\t相应的一个最优排列为:", ig.best_solver.permutation)
    return best_makespans, best_permutations
# 定义写文件函数
def writeResults (best_makespans, best_permutations, method):
# 打开上级目录中的results文件
    path = '../results.txt'
    with open(path, mode='a', encoding='utf-8') as f:
# 写入使用的具体方法
        f.write ('Method : ' + method)
        f.write ('\n')
# 写入每个样例对应的最优时间跨度
        for index, best_makespan in enumerate (best_makespans):
            f.write("Instance " + str(index) + " 最优时间跨度为:" + str(best_makespan))
            f.write ('\n')
            f.write("\t相应的一个最优排列为:" + str(best_permutations[index]))
            f.write ('\n')
if __name__ == "__main__":
# 使用爬山法
	best_makespans, best_permutations = HillClimbing ()
	writeResults (best_makespans, best_permutations, "Hill Climbing")
# 使用模拟退火法
	best_makespans, best_permutations = simulatedAnnealing ()
	writeResults (best_makespans, best_permutations, "Simulated Annealing")