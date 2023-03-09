import math
import random
import numpy as np
from datetime import datetime, timedelta
from solver import Solver
import localSearch
from localSearch import localSearchPop
import loadData
import NEH
import selection
from population import Population
from chromes import initializeChromes, selectChromes, crossChromes, muteChromes
class GeneticAlgorithm (object):
    def __init__ (self, data, tie_breaking = False, local_optimum = True, local_search = False, 
                  select_method = 'tournament', tournament_size = 5, initialize_method = 'random', 
                  mute_method = 'mixed', cross_rate = 0.6, mute_rate = 0.8, p = 50, max_generation = 500,
                  relax_rate = 1.2):
        self.p = p
        self.n = len (data)
        self.m = len (data[0])
        self.max_generation = max_generation
        self.current_pop = Population (data, self.p)
        self.new_pop = Population (data, self.p)
        self.best_pop = Population (data, self.p)
        self.tie_breaking = tie_breaking
        self.local_optimum = local_optimum
        self.local_search = local_search
        self.select_method = select_method
        self.initialize_method = initialize_method
        self.mute_method = mute_method
        self.cross_rate = cross_rate
        self.mute_rate = mute_rate
        self.tournament_size = tournament_size
        self.relax_rate = relax_rate
# 定义运算函数 
    def eval (self, runtime):
# 初始化迭代次数计数器
        self.iterations = 0
# 计算最大计算时限
        time_limit = datetime.now() + timedelta (milliseconds = runtime)
# 初始化种群的染色体编码
        self.current_pop.chromes = initializeChromes (self.n, self.p, initialize_method = self.initialize_method)
# 若开启邻域搜索则进行邻域搜索
        if self.local_search == True:
            localSearchPop (self.current_pop, self.local_optimum, self.tie_breaking)
# 初始化最优种群
        self.current_pop.calculateMakespans()
        self.best_pop.best_chrome = self.current_pop.calculateBestChrome()
        self.best_pop.best_makespan = self.current_pop.calculateBestMakespan()
        self.best_pop.chromes = self.current_pop.chromes.copy()
        for generation in range (self.max_generation):
# 若时间超出限制，则强行中断
            if datetime.now() >= time_limit:
                break
# 初始化新种群
            self.new_pop.chromes = self.current_pop.chromes.copy()
            self.new_pop.calculateMakespans()
# 计算种群的适应度
            makespan = np.max (np.array (self.new_pop.makespans)) * self.relax_rate - np.array (self.new_pop.makespans)
# 进行复制操作
            selectChromes (self.new_pop.chromes, makespan, tournament_size = self.tournament_size, select_method = self.select_method)
# 进行交叉操作
            crossChromes (self.new_pop.chromes, self.cross_rate)
# 进行变异操作
            muteChromes (self.new_pop.chromes, self.mute_rate, self.mute_method)
# 若开启邻域搜索则进行邻域搜索
            if self.local_search == True:
                localSearchPop (self.new_pop, self.local_optimum, self.tie_breaking)
            self.new_pop.calculateMakespans()
            self.new_pop.best_makespan = self.new_pop.calculateBestMakespan()
            self.new_pop.best_chrome = self.new_pop.calculateBestChrome()
            if self.new_pop.best_makespan < self.current_pop.best_makespan:
                self.current_pop.chromes = self.new_pop.chromes
                self.current_pop.best_makespan = self.new_pop.best_makespan
                self.current_pop.best_chrome = self.new_pop.best_chrome
                if self.current_pop.best_makespan < self.best_pop.best_makespan:
                    self.best_pop.chromes = self.current_pop.chromes
                    self.best_pop.best_makespan = self.current_pop.best_makespan
                    self.best_pop.best_chrome = self.current_pop.best_chrome
            self.iterations += 1
        