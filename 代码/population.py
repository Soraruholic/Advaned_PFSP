import numpy as np
from utils.utils import utils
class Population (object):
    def __init__ (self, data, p = 50):
# 定义列表三种参数：工序个数、机器个数和种群容量
        self.n = len (data)
        self.m = len (data[0])
        self.p = p
        self.data = data
        self.chromes = list()
        self.makespans = list()
        self.idle_times = list()
# 初始化最有个体的参数
        self.best_makespan = 0
        self.best_chrome = list() 
# 从cython库接入计算时间跨度的方法
    def calculateMakespans (self):
        chromes = np.array (self.chromes, dtype = 'int32')
        self.makespans = utils.calculateMakespans (chromes, self.data, self.n, self.m, self.p)
        return np.array (self.makespans)
# 计算种群中最优个体的染色体序号
    def calculateBestCombination (self):
        self.makespans = self.calculateMakespans()
        self.best_index = np.argmin (self.makespans) 
        return self.best_index
# 根据最优序号输出相应的染色体编码
    def calculateBestChrome (self):
        self.best_index = self.calculateBestCombination()
        self.best_chrome = self.chromes[self.best_index]
        return np.array (self.best_chrome)
# 根据最有序号输出相应最优时间跨度
    def calculateBestMakespan (self):
        self.best_index = self.calculateBestCombination()
        self.best_makespan = self.makespans[self.best_index]
        return self.best_makespan