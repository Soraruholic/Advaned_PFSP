import math
import random
import numpy as np
from datetime import datetime, timedelta
from solver import Solver
import localSearch
import loadData
import NEH
import selection
# 迭代算法类设计
class IteratedGreedy (object):
    def __init__ (self, data, temperature_init = 0.4, num_removed_jobs = 4, NEH_order = 'SD', tie_breaking = False, 
                  local_optimum = True, local_search = False, selection_algorithm = 'random', tournament_size = 5,
                  max_loop = 50000):
# 声明类成员
        self.current_solver = Solver (data)
        self.new_solver = Solver (data)
        self.best_solver = Solver (data)
        self.temperature_init = temperature_init
        self.num_removed_jobs = num_removed_jobs
        self.NEH_order = NEH_order
        self.tie_breaking = tie_breaking
        self.local_optimum = local_optimum
        self.local_search = local_search
        self.selection_algorithm = selection_algorithm
        self.tournament_size = tournament_size
        self.max_loop = max_loop
    def eval (self, runtime):
        self.iterations = 0
# 初始化温度
        temperature = self.calculateTemperature()
# 定义最长运行时间
        time_limit = datetime.now() + timedelta (milliseconds = runtime)
# 使用NEH进行初始化
        NEH.NEH(self.current_solver, self.tie_breaking, self.NEH_order)
# 进行邻域搜索
        localSearch.localSearch(self.current_solver, self.local_optimum, self.tie_breaking)
# 初始化最优解
        self.best_solver.permutation = self.current_solver.permutation.copy()
        self.best_solver.makespan = self.current_solver.makespan
        for iteration in range (self.max_loop):
# 根据运行时间判断是否需要退出循环
            if datetime.now() >= time_limit:
                break
# 随机选择k道工序移走
            removed_jobs = self.selectJobsToRemove()
            self.new_solver.permutation = [x for x in self.current_solver.permutation if x not in removed_jobs]
# 若开启邻域搜索，则对剩余排列进行一次邻域搜索
            if self.local_search:
                localSearch.localSearch(self.new_solver, self.local_optimum, self.tie_breaking)
# 将抽走的工序一个个加回去，按照NEH规则插入
            for job in removed_jobs:
                self.new_solver.insertIntoBestPosition (job, self.tie_breaking)
            localSearch.localSearch(self.current_solver, self.local_optimum, self.tie_breaking)
# 如果新解优于当前解，则直接更新当前解
            if self.new_solver.makespan < self.current_solver.makespan:
                self.current_solver.permutation = self.new_solver.permutation.copy()
                self.current_solver.makespan = self.new_solver.makespan
                if self.current_solver.makespan < self.best_solver.makespan:
                    self.best_solver.makespan = self.current_solver.makespan
                    self.best_solver.permutation = self.current_solver.permutation.copy()
# 如不然，则根据Mtrepolis规则决定是否更新当前解
            else:
                diff = self.new_solver.makespan - self.current_solver.makespan
# 使用Mtrepolis规则计算舍弃概率
                acceptance_probabilty = math.exp(- diff / temperature)
# 若命中，则更新当前解
                if random.random() <= acceptance_probabilty:
                    self.current_solver.permutation = self.new_solver.permutation.copy()
                    self.current_solver.makespan = self.new_solver.makespan
# 每次循环结束后，更新当前迭代次数
            self.iterations += 1
        
    def computationalTime (self, runtime_facts):
        num = self.current_solver.n * (self.current_solver.m / 2)
        return num * runtime_facts
# 初始化温度
    def calculateTemperature (self):
        temperature = 0
        for i in range(self.current_solver.n):
            temperature += np.sum(self.current_solver.data[i])
        div = self.current_solver.n * self.current_solver.m * 10
        return self.temperature_init * (temperature / div)
    
    def selectJobsToRemove (self):
# 若采用锦标赛法
        if self.selection_algorithm == 'tournament':
            self.current_solver.calculateIdleTimes()
            fitness = self.current_solver.idle_times
            fitness[self.current_solver.permutation[0] - 1] = 0
            selected_jobs = selection.tournamentSelection (fitness, self.tournament_size, self.num_removed_jobs)
# 采用轮盘赌
        elif self.selection_algorithm == 'roulette':
            self.current_solver.calculateIdleTimes()
            fitness = self.selectionFitness()
            fitness[self.current_solver.permutation[0] - 1] = 0
            selected_jobs = selection.rouletteWheelSelection (fitness, self.num_removed_jobs)
# 采用随即遍历
        elif self.selection_algorithm == 'stochastic_uni':
            self.current_solver.calculateIdleTimes()
            fitness = self.selectionFitness()
            fitness[self.current_solver.permutation[0] - 1] = 0
            selected_jobs = selection.stochasticUniversalSampling (fitness, self.num_removed_jobs)
# 采用纯随机法
        else:
            selected_jobs = random.sample(self.current_solver.permutation, self.num_removed_jobs)
        return selected_jobs
    
    def selectionFitness (self):
# 初始化适应度
        fitness = np.empty (self.current_solver.n)
# 计算适应度系数
        for i in range(self.current_solver.n):
            total_fit = np.sum (self.current_solver.data[i])
            fitness[i] = (total_fit + self.current_solver.idle_times[i]) / total_fit
        return fitness