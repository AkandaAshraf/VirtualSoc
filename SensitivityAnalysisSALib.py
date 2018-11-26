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
# import matplotlib.plot as plt


#
import sys
sys.setrecursionlimit(1000000)

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

    # # from here call the simulation methods
    # newParam_values=SalibPreprocessGetParamsForSobol()
    # pool = multiprocessing.Pool(processes=7)
    # #
    # pool.map(simulateNetworksThreaded, newParam_values)
    # #
    # print("Number of cpu : ", multiprocessing.cpu_count())


   # problemFolderPath = 'D:\\sensitivityAnalaysisVirtualSoc\\'
   # statsUniqueSorted = getCleanStats('D:\\sensitivityAnalaysisVirtualSoc\\')
   # Si = getSi(statsUniqueSorted,'D:\\sensitivityAnalaysisVirtualSoc\\')

  # param_valuesFast = SalibPreprocessGetParamsForFAST(1000,'D:\\sensitivityAnalaysisVirtualSocFAST\\')
  # param_valuesRBDFast = SalibPreprocessGetParamsForRBDFASTandDelta(1000, 'D:\\sensitivityAnalaysisVirtualSocRBDFAST\\')
#   param_valuesFF = SalibPreprocessGetParamsForFF('D:\\sensitivityAnalaysisVirtualFF\\')
#
# # simulateNetworksThreaded(param_values,folderPath='D:\\sensitivityAnalaysisVirtualSocFAST')
#
#   pool = multiprocessing.Pool(processes=7)
#
#   # pool.map(simulateNetworksThreadedFAST, param_valuesFast)
#
#   # pool.map(simulateNetworksThreadedRBDFAST, param_valuesRBDFast)
#
#   pool.map(simulateNetworksThreadedFF, param_valuesFF)
#     statsUniqueSorted = getCleanStats('D:\\sensitivityAnalaysisVirtualSoc\\')
#     Si = getSi(statsUniqueSorted, 'D:\\sensitivityAnalaysisVirtualSoc\\')
#     Si = getSi(statsUniqueSorted, 'D:\\sensitivityAnalaysisVirtualSoc\\')

    # statsUniqueSorted = getCleanStats('D:\\sensitivityAnalaysisVirtualSocRBDFAST\\')
    # Si = getSiDelta(statsUniqueSorted, 'D:\\sensitivityAnalaysisVirtualSocRBDFAST\\')
    #
    #

    Si = pk.load(open('D:\\sensitivityAnalaysisVirtualSoc\\Sobol.obj', 'rb'))
    problem = pk.load(open('D:\\sensitivityAnalaysisVirtualSoc\\problemPickle.obj', 'rb'))

    Header = []
    Header.append('method')
    Header.append('property')
    Header.append('param')
    Header.append('S1')

    # class ResultDict(dict):
    #     '''Dictionary holding analysis results.
    #
    #     Conversion methods (e.g. to Pandas DataFrames) to be attached as necessary
    #     by each implementing method
    #     '''
    #     def __init__(self, *args, **kwargs):
    #         super(ResultDict, self).__init__(*args, **kwargs)
    #
    #     def to_df(self):
    #         '''Convert dict structure into Pandas DataFrame.'''
    #         return pd.DataFrame({k: v for k, v in self.items() if k is not 'names'},
    #                             index=self['names'])
    # for key,value in Si.items():
    #     NetProperties.append(key)
    # NetProperties.append('S1')

    df = pd.DataFrame(columns=Header)

    # ResultDict.to_df(Si)
    # pd.DataFrame({k: v for k, v in Si.items() if k is not 'names'},
    #                             index=Si['names'])

    for key, value in Si.items():
        i = 0
        for v in value['S1']:
            df.append(pd.DataFrame([('Sobol', key, problem['names'][i], v)], columns=Header))
            i += 1



