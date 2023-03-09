# 爬山算法
import math
import random
import numpy as np
from datetime import datetime, timedelta
from solver import Solver
import localSearch
import loadData
import NEH
import selection
# 爬山算法方法类定义
class Climb (object):
# 定义类内成员
    def __init__ (self, data, NEH_order = 'SD', local_optimum = True, tie_breaking = False,
                  local_search = True, max_loop = 10000):
        self.current_solver = Solver (data)
        self.new_solver = Solver (data)
        self.best_solver = Solver (data)
        self.tie_breaking = tie_breaking
        self.NEH_order = NEH_order
        self.local_optimum = local_optimum
        self.local_search = local_search
        self.max_loop = max_loop
# 定义运算函数
    def eval (self, runtime):
# 初始化迭代次数
        self.iterations = 0
# 计算最大运行时间
        time_limit = datetime.now() + timedelta (milliseconds = runtime)
# 使用NEH进行初始化
        NEH.NEH(self.current_solver, self.tie_breaking, self.NEH_order)
        localSearch.localSearch(self.current_solver, self.local_optimum, self.tie_breaking)
# 初始化最优解
        self.best_solver.permutation = self.current_solver.permutation.copy()
        self.best_solver.makespan = self.current_solver.makespan
        for iteration in range (self.max_loop):
# 若运行时间国长，则结束迭代
            if datetime.now() >= time_limit:
                break
# 随机取下标并且交换
            i = random.randint (0, len (self.current_solver.permutation) - 1)
            j = random.randint (0, len (self.current_solver.permutation) - 1)
            while i == j:
                j = random.randint (0, len (self.current_solver.permutation) - 1)
            self.new_solver.permutation = self.current_solver.permutation.copy()
            tmp = self.new_solver.permutation[i];
            self.new_solver.permutation[i] = self.new_solver.permutation[j];
            self.new_solver.permutation[j] = tmp;
            if self.local_search == True:
                localSearch.localSearch(self.new_solver, self.local_optimum, self.tie_breaking)
            self.new_solver.makespan = self.new_solver.calculateMakespan()
# 更新最优解
            if self.new_solver.makespan < self.current_solver.makespan:
                self.current_solver.permutation = self.new_solver.permutation.copy()
                self.current_solver.makespan = self.new_solver.makespan
                if self.current_solver.makespan < self.best_solver.makespan:
                    self.best_solver.makespan = self.current_solver.makespan
                    self.best_solver.permutation = self.current_solver.permutation.copy()
            self.iterations += 1