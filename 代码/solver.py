import numpy as np
from utils.utils import utils
class Solver (object):
#    类成员列表:
#        self.n (int)                                  -- 样例的工序个数
#        self.m (int)                                  -- 样例的机器数
#        self.makespan (int)                           -- 该Solver对象对应permuation的时间跨度
#        self.idle_time (int)                          -- 所有工序的总的空闲时间
#        self.idle_times (nparray, shape = (n/k, ))    -- 该Solver对象对应permuation的各个工序的等待时间
    def __init__ (self, data):
        self.n = len (data)
        self.m = len (data[0])
        self.makespan = 0
        self.idle_time = 0
        self.permutation = list()
        self.data = data
        self.idle_times = np.zeros ((self.n), dtype = 'int32') 
    def calculateCompletionTimes (self):
        permutation = np.array (self.permutation, dtype = 'int32')
        completion_times = utils.calculateCompletionTimes (permutation, self.data, self.m, 1)
        return np.array (completion_times)
    def calculateMakespan (self):
        permutation = np.array (self.permutation, dtype = 'int32')
        self.makespan = utils.calculateCompletionTimes (permutation, self.data, self.m, 0)
        return self.makespan
    def insertIntoBestPosition (self, inserted_job, tie_breaking = False):
        use_tie_breaking = 1 if tie_breaking == True else 0
        permutation = np.array (self.permutation, dtype = 'int32')
        best_position, self.makespan = utils.acceleration (permutation, self.data, inserted_job, self.m, use_tie_breaking)
        self.permutation.insert (best_position - 1, inserted_job)
        return self.makespan
    def calculateIdleTimes (self):
        permutation = np.array (self.permutation, dtype = 'int32')
        idle_times = utils.calculateIdleTimes (permutation, self.data, self.m)
        self.idle_time = np.array (idle_times)