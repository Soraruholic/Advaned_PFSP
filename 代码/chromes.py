import random
import numpy as np
# 定义染色体初始化函数
def initializeChromes (n, p, initialize_method = 'random'):
# 采用随机初始化方法
    if initialize_method == 'random':
        permutation = np.arange (1, n + 1)
        chromes = list()
        for i in range (p):
            random.shuffle (permutation)
            chromes.append (permutation.copy())
    return chromes
# 定义复制操作函数
def selectChromes (chromes, fitness, tournament_size = 5, select_method = 'tournament'):
    p = len (chromes)
# 采用锦标赛选择法
    if select_method == 'tournament':
        population = [x + 1 for x in range (len(fitness))]
        permutation = []
        for dummy in range (p):
            aspirants = random.sample (population, tournament_size)
            best = -1
            for asp in aspirants:
                if fitness[asp - 1] > best:
                    best = fitness[asp - 1]
                    winner = asp
            if best == 0:
                winner = random.choice (aspirants)
            permutation.append (winner)
# 采用轮盘赌选择法
    elif select_method == 'roulette':
        total_fit = np.sum (fitness)
        permutation = []
        for i in range (p):
            rand = random.random() * total_fit
            for k in range (len (fitness)):
                rand -= fitness[k]
                if rand <= 0:
                    permutation.append (k + 1)
                    break
            else:
                permutation.append (len (fitness) - 1)
# 采用随即遍历选择法
    elif select_method == 'stochastic_uni':
        distance = np.sum (fitness) / p
        start = random.uniform(0, distance)
        points = [start + i * distance for i in range (p)]
        permutation = []
        for point in points:
            i = 0
            total_fitness = fitness[i]
            while total_fitness < point:
                i += 1
                total_fitness += fitness[i]
            permutation.append (i + 1)
    return [chromes[x - 1] for x in permutation]
# 定义交叉操作函数
def crossChromes (chromes, cross_rate):
    p = len (chromes)
    n = len (chromes[0])
    for i in range (0, p, 2):
# 随机数判断是否进行交叉操作
        if random.random() < cross_rate:
            j = (i + 1) % n
            dic1 = dict (zip (chromes[i], range (n)))
            dic2 = dict (zip (chromes[j], range (n)))
            spl = np.array(random.sample(range(0, n + 1), 2), dtype = 'int32')
            r = np.min (spl)
            s = np.max (spl)
            diff1 = list (set (chromes[i][r:s]) - set (chromes[j][r:s]))
            diff2 = list (set (chromes[j][r:s]) - set (chromes[i][r:s]))
# 对两端进行可行性修正
            for index, x in enumerate(diff2):
                chromes[i][dic1[x]] = diff1[index]
                chromes[j][dic2[diff1[index]]] = x
# 执行交换操作
            tmp = chromes[i][r:s].copy()
            chromes[i][r:s] = chromes[j][r:s].copy()
            chromes[j][r:s] = tmp.copy()
# return chromes 
# 定义变异操作函数
def muteChromes (chromes, mute_rate, mute_method):
    p = len (chromes)
    for i in range (p):
# 随机数判断是否需要变异
        if random.random() < mute_rate:  
# 采用交换法
            if mute_method == 'interchange':
                muteInterchange (chromes[i])
# 采用逆序法
            elif mute_method == 'reverse':
                muteReverse (chromes[i])
            elif mute_method == 'insertion':
                muteInsertion (chromes[i])
# 采用混合法
            elif mute_method == 'mixed':
# 随机判断方法混合的情况
                seq = random.randint (1, 7)
                if seq % 2 == 1:
                    muteInsertion (chromes[i])
                elif (seq / 2) % 2 == 1:
                    muteReverse (chromes[i])
                elif (seq / 4) % 2 == 1:
                     muteInterchange (chromes[i])
# elif mute_method == 'heuristic':  
# 定义交换函数
def muteInterchange (chrome):
    r, s = np.array(random.sample(range(0, len(chrome)), 2), dtype = 'int32')
    tmp = chrome[r]
    chrome[r] = chrome[s]
    chrome[s] = tmp
# 定义倒序函数
def muteReverse (chrome):
# 随机倒序片段的两个端点
    slp = np.array(random.sample(range(0, len(chrome) + 1), 2), dtype = 'int32')
    r = np.min (slp)
    s = np.max (slp)
# 如遇到端点，则必须经过特殊处理
    p = - len(chrome) - 1 + s if r == 0 else s - 1
    q = - len(chrome) - 1 if r == 0 else r - 1 
    chrome[r:s] = chrome[p:q:-1]  
# 定义插入函数
def muteInsertion (chrome):
# 随机选择插入点与被插入点
    slp = np.array(random.sample(range(0, len(chrome)), 2), dtype = 'int32')
    r = np.min (slp)
    s = np.max (slp)
# 执行插入操作
    tmp = chrome[r]
    chrome[r:(s - 1)] = chrome[(r + 1):s]
    chrome[s - 1] = tmp