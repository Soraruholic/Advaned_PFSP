import math
import random
import numpy as np
from datetime import datetime, timedelta
from solver import Solver
import localSearch
import loadData
import NEH
import selection
# 定义模拟退火方法类
class SimulatedAnnealing (object):
# 初始化定义类内成员
    def __init__ (self, data, NEH_order = 'SD', local_optimum = True, tie_breaking = False, 
                  temperature_init = 0.4, annealing_rate = 0.99, iteration_per_epoch = 1000,
                  local_search = True, max_loop = 10000):
        self.current_solver = Solver (data)
        self.new_solver = Solver (data)
        self.best_solver = Solver (data)
        self.tie_breaking = tie_breaking
        self.NEH_order = NEH_order
        self.local_optimum = local_optimum
        self.local_search = local_search
        self.temperature_init = temperature_init
        self.annealing_rate = annealing_rate
        self.iteration_per_epoch = iteration_per_epoch
        self.max_loop = max_loop
    def eval (self, runtime):
# 初始化迭代次数
        self.iterations = 0
# 计算运行时间上限
        time_limit = datetime.now() + timedelta (milliseconds = runtime)
        temperature = self.calculateInitialTemperature()
# 使用NEH进行初始化
        NEH.NEH(self.current_solver, self.tie_breaking, self.NEH_order)
        localSearch.localSearch(self.current_solver, self.local_optimum, self.tie_breaking)
# 初始化最优解
        self.best_solver.permutation = self.current_solver.permutation.copy()
        self.best_solver.makespan = self.current_solver.makespan
# 迭代求解问题
        for iteration in range (self.max_loop):
# 如果运行时间超出上限，则结束循环
            if datetime.now() >= time_limit:
                break
# 随机抽取两下标
            i = random.randint (0, len (self.current_solver.permutation) - 1)
            j = random.randint (0, len (self.current_solver.permutation) - 1)
            while i == j:
                j = random.randint (0, len (self.current_solver.permutation) - 1)
# 初始化新解
            self.new_solver.permutation = self.current_solver.permutation.copy()
# 交换两下表对应的元素
            tmp = self.new_solver.permutation[i];
            self.new_solver.permutation[i] = self.new_solver.permutation[j];
            self.new_solver.permutation[j] = tmp;
# 如果开启邻域搜索，则进行邻域搜索
            if self.local_search == True:
                localSearch.localSearch(self.new_solver, self.local_optimum, self.tie_breaking)
            self.new_solver.makespan = self.new_solver.calculateMakespan()
# 若新解更优，则更新当前解
            if self.new_solver.makespan < self.current_solver.makespan:
                self.current_solver.permutation = self.new_solver.permutation.copy()
                self.current_solver.makespan = self.new_solver.makespan
# 更新最优解
                if self.current_solver.makespan < self.best_solver.makespan:
                    self.best_solver.makespan = self.current_solver.makespan
                    self.best_solver.permutation = self.current_solver.permutation.copy()
            else:
                diff = self.new_solver.makespan - self.current_solver.makespan
                acceptance_probabilty = math.exp(- diff / temperature)
                if random.random() <= acceptance_probabilty:
                    self.current_solver.permutation = self.new_solver.permutation.copy()
                    self.current_solver.makespan = self.new_solver.makespan
            self.iterations += 1
            if self.iterations % self.iteration_per_epoch == 0:
                temperature *= self.annealing_rate
# 定义初始化温度函数
    def calculateInitialTemperature (self):
        temperature = 0
        for i in range(self.current_solver.n):
            temperature += np.sum(self.current_solver.data[i])
        div = self.current_solver.n * self.current_solver.m * 10
        return self.temperature_init * (temperature / div)         