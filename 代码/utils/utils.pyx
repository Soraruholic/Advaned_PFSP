import numpy as np
cimport cython
@cython.boundscheck (False)  # 禁用边界检查
@cython.wraparound (False)   # 关闭负数访问
cpdef acceleration(int[:] permutation, int[:, :] data, int inserted_job, int m, int use_tie_breaking):
#	该函数寻找插入一个工序的最佳位置, 以获得最小的跨度时间
#	参数列表:
#		permutation (nparray, shape = (n, ))    -- 当前的加工顺序, n即工序个数
#		data (nparray, shape = (n, m))          -- 给定的数据矩阵, 包含每道工序单独在每台机器上的加工时间, n为工序个数, m为机器数
#		inserted_job (int)                      -- 目前待插入的工序
#		m (int)                                 -- 机器的个数
#		use_tie_breaking (int)                  -- 是否采取tie_breaking机制, 只可取1(True), 或0(False)
	cdef int e[802][62]
	cdef int q[802][62]
	cdef int f[802][62]
	cdef int makespan[802]
	cdef int n = len (permutation)
	cdef int lowest_makespan, best_position
	cdef int i, j, r, s, tmp
	r = n + 1
	for i in range (1, n + 2):
		if i < n + 1:
			e[i][0] = 0
			r = r - 1
			q[r][m + 1] = 0
		f[i][0] = 0
		s = m + 1
		for j in range (1, m + 1):
			if i == 1:
				e[0][j] = 0
				q[n + 1][m + 1 - j] = 0
			if i < n + 1:
				s = s - 1
				if e[i][j - 1] > e[i - 1][j]:
					e[i][j] = e[i][j - 1] + data[permutation[i - 1] - 1, j - 1]
				else:
					e[i][j] = e[i - 1][j] + data[permutation[i - 1] - 1, j - 1]

				if q[r][s + 1] > q[r + 1][s]:
					q[r][s] = q[r][s + 1] + data[permutation[r - 1] - 1, s - 1]
				else:
					q[r][s] = q[r + 1][s] + data[permutation[r - 1] - 1, s - 1]
			if f[i][j - 1] > e[i - 1][j]:
				f[i][j] = f[i][j - 1] + data[inserted_job - 1, j - 1]
			else:
				f[i][j] = e[i - 1][j] + data[inserted_job - 1, j - 1]
	lowest_makespan = 0
	best_position = 0
	for i in range (1, n + 2):
		makespan[i] = 0
		for j in range (1, m + 1):
			tmp = f[i][j] +	q[i][j]
			if tmp > makespan[i]:
				makespan[i] = tmp
		if makespan[i] < lowest_makespan or lowest_makespan == 0:
			lowest_makespan = makespan[i]
			best_position = i
	if use_tie_breaking > 0:
		best_position = tie_breaking(data, e, f, makespan, inserted_job, best_position, n, m)

	return best_position, lowest_makespan
@cython.boundscheck (False)  # 禁用边界检查
@cython.wraparound (False)   # 关闭负数访问
cdef tie_breaking(int[:,:] data, int[:,:] e, int[:,:] f, int[:] makespan, int inserted_job, int best_position, int n, int m):
#	该函数处理多个相同时间跨度的选择问题
#	参数列表:
#		data (nparray, shape = (n, m))               -- 给定的数据矩阵, 包含每道工序单独在每台机器上的加工时间, n为工序个数, m为机器数
#		e (static array, shape = (802, 62))          -- 每道工序在每台机器上的完成时间
#		f (static array, shape = (802, 62))          -- Taillard算法(NEH)中用来计算插入代价的辅助数组
#		makespan (static array, shape = (802, ))     -- 每个插入位置所对应的时间跨度
#		inserted_job (int)                           -- 目前待插入的工序
#		best_position                                -- 朴素NEH算法给出的最佳插入位置
#		n (int)                                      -- 工序的个数
#		m (int)                                      -- 机器的个数
	cdef int lowest_makespan = makespan[best_position]
	cdef int num_ties = 0
	cdef int itbp = 2000000
	cdef int it, tie, i, j
	cdef int fl[802][62]
	for i in range(1, n + 2):
		if makespan[i] == lowest_makespan:
			it = 0
			num_ties += 1
			if i == n:
				for j in range(1, m + 1):
					it += f[n][j] - e[n - 1][j] - data[inserted_job - 1,j - 1]
			else:
				fl[i][1] = f[i][1] + data[i - 1][0]
				for j in range(2, m + 1):
					it += f[i][j] - e[i][j] + data[i - 1,j - 1] - data[inserted_job - 1,j - 1]
					if fl[i][j - 1] - f[i][j] > 0:
						it += fl[i][j - 1] - f[i][j]
					if fl[i][j - 1] > f[i][j]:
						fl[i][j] = fl[i][j - 1] + data[i - 1,j - 1]
					else:
						fl[i][j] = fl[i][j] + data[i - 1,j - 1]
			if it < itbp:
				best_position = i
				itbp = it

	return best_position
@cython.boundscheck (False)  # 禁用边界检查
@cython.wraparound (False)   # 关闭负数访问
cpdef calculateCompletionTimes (int[:] permutation, int[:, :] data, int m, int return_type):
#	该函数计算每道工序在每个机器上花费的时间
#	参数列表:
#		permutation (nparray, shape = (n, ))    -- 当前的加工顺序, n即工序个数
#		data (nparray, shape = (n, m))          -- 给定的数据矩阵, 包含每道工序单独在每台机器上的加工时间, n为工序个数, m为机器数
#		m (int)                                 -- 机器的个数
#		return_type (array/int)                 -- 返回类型 
#										            如果为1，则返回每道工序各自的完成时间的数组										            如果为0，则直接返回最后一道工序在最后一台机器上完成的时间(整数)
#	返回列表:
#		completion_times: (nparray, shape = (n + 1, m + 1))   -- 每道工序在每台机器上的完成时间
#												或者 最后一道工序在最后一台机器上的完成时间
#
	cdef int n = len (permutation)
	cdef int[:, ::1] completion_times = np.zeros ((n + 1, m + 1), dtype = 'int32')
	cdef int i, j 
	for i in range (1, n + 1):
		for j in range (1, m + 1):
			if completion_times[i - 1, j] > completion_times[i, j - 1]:
				completion_times[i, j] = completion_times[i - 1, j] + data[permutation[i - 1] - 1, j - 1]
			else:
				completion_times[i, j] = completion_times[i, j - 1] + data[permutation[i - 1] - 1, j - 1]
	if return_type == 1:
		return completion_times
	else:
		return completion_times[n, m]
@cython.boundscheck (False)  # 禁用边界检查
@cython.wraparound (False)   # 关闭负数访问
cpdef calculateIdleTimes (int[:] permutation, int[:, :] data, int m):
#	该函数计算每台机器的空闲时间
#	参数列表:
#		permutation (nparray, shape = (n, ))   -- 当前的加工顺序, n即工序个数
#		data (nparray, shape = (n, m))         -- 给定的数据矩阵，包含每道工序单独在每台机器上的加工时间, n为工序个数, m为机器数
#		m (int)                                -- 机器的个数
	cdef int n = len (permutation)
	cdef int i, j;
	cdef int[:] idle_times = np.zeros ((n), dtype = 'int32')
	cdef int[:, ::1] completion_times = calculateCompletionTimes (permutation, data, m, 1)
	for i in range (0, n):
		idle_times[permutation[i] - 1] = 0
		for j in range (0, m):
			idle_times[permutation[i] - 1] = completion_times[i + 1, j + 1] - completion_times[i, j + 1] - data[permutation[i] - 1, j]
	return idle_times
@cython.boundscheck (False)  # 禁用边界检查
@cython.wraparound (False)   # 关闭负数访问
cpdef calculateMakespans (int[:, :] chromes, int[:, :] data, int n, int m, int p):
	cdef int i
	cdef int[:] makespans = np.zeros ((p), dtype = 'int32')
	for i in range (p):
		makespans[i] = calculateCompletionTimes (chromes[i, :], data, m, 0)
	return makespans