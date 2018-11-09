from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami
import numpy as np
from HighLevelForSALib import *
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool
import pandas as pd
import multiprocessing
import pickle as pk
import pandas as pd
from UtilSAlib import *



#
# import sys
# from multiprocessing import Pool
# sys.setrecursionlimit(1000000)
#
# def SalibPreprocessGetParamsForSobol(numberOfSamples,folderPathToSaveParamsAndProblem):
#     #https://salib.readthedocs.io/en/latest/basics.html
#     problem = {
#         'num_vars': 6,
#         'names': ['explorationProbabilityV', 'popularityPreferenceIntensityV', 'connectionPercentageWithMatchedNodesV', 'mutualPreferenceIntensityV2', 'mutualPreferenceIntensityV3', 'mutualPreferenceIntensityV4'],
#         'bounds': [[0.0,1.0],
#                    [0.1, 10],
#                    [1, 80],
#                    [0.7, 0.9],
#                    [0.3, 0.6],
#                    [0.1, 0.2]]
#     }
#     pk.dump(problem,open( folderPathToSaveParamsAndProblem+'\problemPickle.obj', 'wb' ) )
#     param_values = saltelli.sample(problem, numberOfSamples)
#     l = len(param_values)
#     indices = np.arange(0, l)
#     indices = indices.reshape(l,1)
#     newParam_values = np.concatenate((param_values, indices), axis=1)
#
#     np.savetxt(folderPathToSaveParamsAndProblem+'\\params', param_values, fmt='%.18e', delimiter=' ',
#                newline='\n', header='', footer='', comments='# ', encoding=None)
#     return newParam_values

    # param_values1 = np.asmatrix(param_values)


# for p in newParam_values:
#      print(p[0])
if __name__ == '__main__':

    #from here call the simulation methods
    # newParam_values=SalibPreprocessGetParamsForSobol()
    # pool = multiprocessing.Pool(processes=7)
    #
    # pool.map(simulateNetworksThreaded, newParam_values)
    #
    # print("Number of cpu : ", multiprocessing.cpu_count())

   #test here ....
   # problem = pk.load(open('D:\\sensitivityAnalaysisVirtualSoc\\problemPickle.obj','rb'))
   # param_values  =pd.read_csv('D:\\sensitivityAnalaysisVirtualSoc\\params', sep=',',header=None)
   # #
   # # stats  =pd.read_csv('D:\\sensitivityAnalaysisVirtualSoc\\allStats.csv', sep=',',header='infer')
   # # statsUnique = stats.drop_duplicates(list(stats)[1:])
   # # statsUniqueSorted  = statsUnique.sort_values(list(stats)[0])
   # #
   # #
   #
   problemFolderPath = 'D:\\sensitivityAnalaysisVirtualSoc\\'
   statsUniqueSorted = getCleanStats('D:\\sensitivityAnalaysisVirtualSoc\\')
   Si = getSi(statsUniqueSorted,'D:\\sensitivityAnalaysisVirtualSoc\\')
   Si['GlobalClusteringCoefficent']
   # Y = statsUniqueSorted[list(statsUniqueSorted)[3]]
   # Si = sobol.analyze(problem, np.asarray(Y), print_to_console=True)
