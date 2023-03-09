#    NEH算法的实现, 注意这里使用了三种不同的初始化方法: 
#    SD : 按照每道工序单独在不同机器上消耗时间总和的倒序初始化
#    AD : 按照每道工序单独在不同机器上消耗时间的均值与标准差之和的倒序初始化
#    Random : 按照随机顺序
import random
import numpy as np
from solver import Solver
def NEH (solver, tie_breaking = False, order = 'SD'):
# 采取朴素逆序顺序
    if order == 'SD':
        jobs = sd_order (solver)
# 采取均值+方差顺序
    elif order == 'AD':
        jobs = ad_order (solver)
# 采取纯随机顺序
    else:
        jobs = [x for x in range (1, solver.n + 1)]
        random.shuffle (jobs)
    solver.permutation = jobs[:2]
    ms1 = solver.calculateMakespan()
    solver.permutation = jobs[1::-1]
    if ms1 < solver.calculateMakespan():
        solver.permutation = jobs[:2]
        solver.makespan = ms1
    for job in jobs[2:]:
        solver.insertIntoBestPosition (job, tie_breaking)    
def sd_order (solver):
    total_processing_times = dict()
    for i in range(1, solver.n + 1):
        total_processing_times[i] = np.sum(solver.data[i - 1])
    return sorted(total_processing_times, key = total_processing_times.get, reverse = True)
def ad_order (solver):
    average_plus_deviation = dict()
    for i in range(1, solver.n + 1):
        avg = np.mean(solver.data[i - 1])
        dev = np.std(solver.data[i - 1])
        average_plus_deviation[i] = avg + dev
    return sorted(average_plus_deviation, key = average_plus_deviation.get, reverse = True)
# 声明NEH算法类
class NawazEnscoreHam (object):
    def __init__ (self, data, order = 'SD', tie_breaking = False):
        self.solver = Solver (data)
        self.data = data
        self.order = order
        self.tie_breaking = tie_breaking
    def eval (self):
        NEH (self.solver, self.tie_breaking, self.order)