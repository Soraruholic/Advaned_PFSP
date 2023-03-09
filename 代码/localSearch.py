import random
from solver import Solver
import numpy as np
# 定义邻域搜索函数
def localSearch(solver, local_optimum = True, tie_breaking = False):
    current_makespan = 0
    need_improve = True
    MAXLOOP = 1000000
    for dummy in range (MAXLOOP):
# 若不需要再进一步搜索，则直接退出循环
        if need_improve == False:
            break
        current_jobs = solver.permutation.copy()
        random.shuffle (current_jobs)
        for job in current_jobs:
            solver.permutation.remove (job)
# 三目运算符判断当前状态的时间跨度有无被计算过
            current_makespan = current_makespan if current_makespan != 0 else solver.calculateMakespan()
# 调用NEH中的插入规则
            solver.insertIntoBestPosition (job, tie_breaking)
            if solver.makespan < current_makespan:
                need_improve = True
                current_makespan = solver.makespan
            else:
                need_improve = False
# 若禁止多重邻域搜索，则退出循环
        if local_optimum == False:
            break
    return    
# 定义种群邻域搜索函数 
def localSearchPop (population, local_optimum = True, tie_breaking = False):
    p = population.p
    for index in range (p):
        solver = Solver (population.data)
        solver.permutation = list(population.chromes[index].copy())
        localSearch(solver, local_optimum, tie_breaking)
        population.chromes[index] = solver.permutation.copy()