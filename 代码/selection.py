import numpy as np
import random
# 轮盘赌选择算法
def rouletteWheelSelection (fitness, n):
    total_fit = np.sum (fitness)
    permutation = []
# 循环随机转动轮盘抽出最优者
    for i in range (n):
        rand = random.random() * total_fit
# 计算累计概率
        for k in range (len (fitness)):
            rand -= fitness[k]
# 挑出最优者
            if rand <= 0:
                permutation.append (k + 1)
                break
        else:
            permutation.append (len (fitness) - 1)
    return permutation
# 锦标赛选择算法 (采样无放回)
def tournamentSelection (fitness, tournament_size, n):
    population = [x + 1 for x in range (len(fitness))]
    permutation = []
# 循环计算锦标赛胜者
    for dummy in range (n):
        aspirants = random.sample (population, tournament_size)
        best = -1
# 在参赛选手中选取最优者
        for asp in aspirants:
            if fitness[asp - 1] > best:
                best = fitness[asp - 1]
                winner = asp
# 处理平凡的情形
        if best == 0:
            winner = random.choice (aspirants)
        permutation.append (winner)
        population.remove (winner)
    return permutation
def stochasticUniversalSampling(fitness, n):
    distance = np.sum (fitness) / n
    start = random.uniform(0, distance)
    points = [start + i * distance for i in range (n)]
    permutation = []
# 遍历选取最优者
    for point in points:
        i = 0
        total_fitness = fitness[i]
        while total_fitness < point:
            i += 1
            total_fitness += fitness[i]
        permutation.append (i + 1)
    return permutation