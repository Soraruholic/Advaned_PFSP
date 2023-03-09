import numpy as np
#        参数列表:
#                dname  (str)             -- 所需要读入实例数据的名称, 只能在'cars', 'rec', 'bit', 'et', 'heller',
#                                                            'vrf_small', 'vrf_large'中任选一个
#       返回列表:
#                instances (list)         -- 实例所包含的数据, 列表的每个元素都是nparray, 存储单个样例
#                upper_bounds (nparray)   -- 每个实例对应的标准结果的上界，为算法评价指标的主要相对参照因素
#                lower_bounds (nparray)   -- 每个实例对应的标准结果的下界，通过分支界限法蛮力计算而来，用来评价算法的绝对准确率
def dataLoading (dname):
        path = "../附件/instances/instance_"
        f = open (path + dname + ".txt", "r")
# 读入实例中样例的总个数
        line = f.readline()
        count = int(line)
        instances = list()
        instance = list()
        for i in range (count):
            instance.clear()
            n, m = [int (item) for item in f.readline().split()]
            for j in range (n):
                line = [int (item) for item in f.readline().split()]
                line = line[1::2]
                instance.append (line.copy())
            instances.append (np.array (instance.copy(), dtype = 'int32'))          
        upper_bounds = list()
        lower_bounds = list()
        f.readline()
        for i in range (count):
            upper_bounds.append (int (f.readline()))
        upper_bounds = np.array (upper_bounds, dtype = 'int32')
        f.readline()
        for i in range (count):
            lower_bounds.append (int (f.readline()))
        lower_bounds = np.array (lower_bounds, dtype = 'int32')
        return instances, upper_bounds, lower_bounds