from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami
import numpy as np
from HighLevelForSALib import *
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool
import pandas as pd
import multiprocessing




import sys
from multiprocessing import Pool
sys.setrecursionlimit(1000000)
problem = {
    'num_vars': 6,
    'names': ['explorationProbabilityV', 'popularityPreferenceIntensityV', 'connectionPercentageWithMatchedNodesV', 'mutualPreferenceIntensityV2', 'mutualPreferenceIntensityV3', 'mutualPreferenceIntensityV4'],
    'bounds': [[0.0,1.0],
               [0.1, 10],
               [1, 80],
               [0.7, 0.9],
               [0.3, 0.6],
               [0.1, 0.2]]
}

param_values = saltelli.sample(problem, 1000)
param_values.shape
l = len(param_values)
indices  = np.arange(0,l)
indices = indices.reshape(l,1)
# param_values1 = np.asmatrix(param_values)

newParam_values = np.concatenate((param_values, indices), axis=1)

# for p in newParam_values:
#      print(p[0])
if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=7)
    pool.map(simulateNetworksThreaded, newParam_values)

    print("Number of cpu : ", multiprocessing.cpu_count())

#
# def worker(num):
#     """thread worker function"""
#     print('Worker:', num)
#
#
# if __name__ == '__main__':
#     jobs = []
#     for newParam_value in newParam_values:
#         p = multiprocessing.Process(target=simulateNetworksThreaded, args=(i,))
#         jobs.append(p)
#         p.start()

# simulateNetworks(param_values=param_values,folderPath='D:\\sensitivityAnalaysisVirtualSoc\\')

    np.savetxt('D:\\sensitivityAnalaysisVirtualSoc\\params', np.asarray(param_values), fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ', encoding=None)