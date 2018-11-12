from SALib.sample import saltelli
from SALib.sample import fast_sampler
from SALib.sample import latin
from SALib.sample import morris
from SALib.sample import ff




from SALib.analyze import sobol
from SALib.analyze import rbd_fast
from SALib.analyze import fast
from SALib.analyze import delta


from SALib.test_functions import Ishigami
import numpy as np
from HighLevelForSALib import *
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool
import pandas as pd
import multiprocessing
import pickle as pk
import pandas as pd
from contextlib import redirect_stdout






import sys
from multiprocessing import Pool


def SalibPreprocessGetParamsForSobol(numberOfSamples,folderPathToSaveParamsAndProblem):
    #https://salib.readthedocs.io/en/latest/basics.html
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
    pk.dump(problem,open( folderPathToSaveParamsAndProblem+'\problemPickle.obj', 'wb' ) )
    param_values = saltelli.sample(problem, numberOfSamples)
    l = len(param_values)
    indices = np.arange(0, l)
    indices = indices.reshape(l,1)
    newParam_values = np.concatenate((param_values, indices), axis=1)

    np.savetxt(folderPathToSaveParamsAndProblem+'\\params', param_values, fmt='%.18e', delimiter=' ',
               newline='\n', header='', footer='', comments='# ', encoding=None)
    return newParam_values

def SalibPreprocessGetParamsForFAST(numberOfSamples, folderPathToSaveParamsAndProblem):
        # https://salib.readthedocs.io/en/latest/basics.html
        problem = {
            'num_vars': 6,
            'names': ['explorationProbabilityV', 'popularityPreferenceIntensityV',
                      'connectionPercentageWithMatchedNodesV', 'mutualPreferenceIntensityV2',
                      'mutualPreferenceIntensityV3', 'mutualPreferenceIntensityV4'],
            'bounds': [[0.0, 1.0],
                       [0.1, 10],
                       [1, 80],
                       [0.7, 0.9],
                       [0.3, 0.6],
                       [0.1, 0.2]]
        }
        pk.dump(problem, open(folderPathToSaveParamsAndProblem + '\problemPickle.obj', 'wb'))
        param_values=fast_sampler.sample(problem, numberOfSamples, M=4)
        l = len(param_values)
        indices = np.arange(0, l)
        indices = indices.reshape(l, 1)
        newParam_values = np.concatenate((param_values, indices), axis=1)

        np.savetxt(folderPathToSaveParamsAndProblem + '\\params', param_values, fmt='%.18e', delimiter=' ',
                   newline='\n', header='', footer='', comments='# ', encoding=None)
        return newParam_values

def SalibPreprocessGetParamsForRBDFASTandDelta(numberOfSamples, folderPathToSaveParamsAndProblem):
        # https://salib.readthedocs.io/en/latest/basics.html
        problem = {
            'num_vars': 6,
            'names': ['explorationProbabilityV', 'popularityPreferenceIntensityV',
                      'connectionPercentageWithMatchedNodesV', 'mutualPreferenceIntensityV2',
                      'mutualPreferenceIntensityV3', 'mutualPreferenceIntensityV4'],
            'bounds': [[0.0, 1.0],
                       [0.1, 10],
                       [1, 80],
                       [0.7, 0.9],
                       [0.3, 0.6],
                       [0.1, 0.2]]
        }
        pk.dump(problem, open(folderPathToSaveParamsAndProblem + '\problemPickle.obj', 'wb'))
        param_values=latin.sample(problem, numberOfSamples)
        l = len(param_values)
        indices = np.arange(0, l)
        indices = indices.reshape(l, 1)
        newParam_values = np.concatenate((param_values, indices), axis=1)

        np.savetxt(folderPathToSaveParamsAndProblem + '\\params', param_values, fmt='%.18e', delimiter=' ',
                   newline='\n', header='', footer='', comments='# ', encoding=None)
        return newParam_values

def SalibPreprocessGetParamsForFF(folderPathToSaveParamsAndProblem):
        # https://salib.readthedocs.io/en/latest/basics.html
        problem = {
            'num_vars': 6,
            'names': ['explorationProbabilityV', 'popularityPreferenceIntensityV',
                      'connectionPercentageWithMatchedNodesV', 'mutualPreferenceIntensityV2',
                      'mutualPreferenceIntensityV3', 'mutualPreferenceIntensityV4'],
            'bounds': [[0.0, 1.0],
                       [0.1, 10],
                       [1, 80],
                       [0.7, 0.9],
                       [0.3, 0.6],
                       [0.1, 0.2]]
        }
        pk.dump(problem, open(folderPathToSaveParamsAndProblem + '\problemPickle.obj', 'wb'))
        param_values=ff.sample(problem)
        l = len(param_values)
        indices = np.arange(0, l)
        indices = indices.reshape(l, 1)
        newParam_values = np.concatenate((param_values, indices), axis=1)

        np.savetxt(folderPathToSaveParamsAndProblem + '\\params', param_values, fmt='%.18e', delimiter=' ',
                   newline='\n', header='', footer='', comments='# ', encoding=None)
        return newParam_values
    # param_values1 = np.asmatrix(param_values)

def SalibPreprocessGetParamsForMorris(numberOfSamples, folderPathToSaveParamsAndProblem):
        # https://salib.readthedocs.io/en/latest/basics.html
        problem = {
            'num_vars': 6,
            'names': ['explorationProbabilityV', 'popularityPreferenceIntensityV',
                      'connectionPercentageWithMatchedNodesV', 'mutualPreferenceIntensityV2',
                      'mutualPreferenceIntensityV3', 'mutualPreferenceIntensityV4'],
            'bounds': [[0.0, 1.0],
                       [0.1, 10],
                       [1, 80],
                       [0.7, 0.9],
                       [0.3, 0.6],
                       [0.1, 0.2]]
        }
        pk.dump(problem, open(folderPathToSaveParamsAndProblem + '\problemPickle.obj', 'wb'))
        param_values=morris.sample(problem=problem, N=numberOfSamples,grid_jump=4)
        l = len(param_values)
        indices = np.arange(0, l)
        indices = indices.reshape(l, 1)
        newParam_values = np.concatenate((param_values, indices), axis=1)

        np.savetxt(folderPathToSaveParamsAndProblem + '\\params', param_values, fmt='%.18e', delimiter=' ',
                   newline='\n', header='', footer='', comments='# ', encoding=None)
        return newParam_values
    # param_values1 = np.asmatrix(param_values)
def getCleanStats(folderPath):
    stats = pd.read_csv(folderPath+'\\allStats.csv', sep=',', header='infer')
    statsUnique = stats.drop_duplicates(list(stats)[1:])
    statsUniqueSorted = statsUnique.sort_values(list(stats)[0])
    return statsUniqueSorted

def getSi(statsUniqueSorted,problemFolderPath):
    Si = {}
    problem = pk.load(open(problemFolderPath+'\\problemPickle.obj', 'rb'))
    # param_values = pd.read_csv(problemFolderPath+'\params', sep=',', header=None)
    with open(problemFolderPath+'//SoboltestOutput.txt', 'w') as f:
        with redirect_stdout(f):
            print('\n sensitivity analysis from total: '+str(len(statsUniqueSorted)) +' samples, details: https://salib.readthedocs.io/en/latest/api.html#sobol-sensitivity-analysis \n\n\n')

            for i in range(2,len(list(statsUniqueSorted))-1):
                Y = statsUniqueSorted[list(statsUniqueSorted)[i]]
                print('\n\n..... Sensitivity for: '+list(statsUniqueSorted)[i]+'...........\n\n')
                Si[list(statsUniqueSorted)[i]]=sobol.analyze(problem, np.asarray(Y), print_to_console=True)
    pk.dump(Si,open( problemFolderPath+'\\Sobol.obj', 'wb' ))


    return Si

def getSiFAST(statsUniqueSorted,problemFolderPath):
    Si = {}
    problem = pk.load(open(problemFolderPath+'\\problemPickle.obj', 'rb'))
    # param_values = pd.read_csv(problemFolderPath+'\params', sep=',', header=None)
    with open(problemFolderPath+'//FASTtestOutput.txt', 'w') as f:
        with redirect_stdout(f):
            print('\n sensitivity analysis from total: '+str(len(statsUniqueSorted)) +' samples, details: https://salib.readthedocs.io/en/latest/api.html#sobol-sensitivity-analysis \n\n\n')

            for i in range(2,len(list(statsUniqueSorted))-1):
                Y = statsUniqueSorted[list(statsUniqueSorted)[i]]
                print('\n\n..... Sensitivity for: '+list(statsUniqueSorted)[i]+'...........\n\n')
                Si[list(statsUniqueSorted)[i]]=fast.analyze(problem, np.asarray(Y), print_to_console=True)
    pk.dump(Si,open( problemFolderPath+'\\FAST.obj', 'wb' ))

    return Si


def getSiRBDFAST(statsUniqueSorted,problemFolderPath):
    Si = {}
    problem = pk.load(open(problemFolderPath+'\\problemPickle.obj', 'rb'))
    X = pd.read_csv(problemFolderPath+'\\params', sep=' ', header=None)
    X = np.asarray(X)

    # param_values = pd.read_csv(problemFolderPath+'\params', sep=',', header=None)
    with open(problemFolderPath+'//RBDFASTtestOutput.txt', 'w') as f:
        with redirect_stdout(f):
            print('\n sensitivity analysis from total: '+str(len(statsUniqueSorted)) +' samples, details: https://salib.readthedocs.io/en/latest/api.html#sobol-sensitivity-analysis \n\n\n')

            for i in range(2,len(list(statsUniqueSorted))-1):
                Y = statsUniqueSorted[list(statsUniqueSorted)[i]]
                print('\n\n..... Sensitivity for: '+list(statsUniqueSorted)[i]+'...........\n\n')
                Si[list(statsUniqueSorted)[i]]=rbd_fast.analyze(problem=problem, Y=np.asarray(Y),X=X, print_to_console=True)
    pk.dump(Si,open( problemFolderPath+'\\SiRDBFAST.obj', 'wb' ))

    return Si


def getSiDelta(statsUniqueSorted,problemFolderPath):
    Si = {}
    problem = pk.load(open(problemFolderPath+'\\problemPickle.obj', 'rb'))
    X = pd.read_csv(problemFolderPath+'\\params', sep=' ', header=None)
    X = np.asmatrix(X)

    # param_values = pd.read_csv(problemFolderPath+'\params', sep=',', header=None)
    with open(problemFolderPath+'//DeltaTestOutput.txt', 'w') as f:
        with redirect_stdout(f):
            print('\n sensitivity analysis from total: '+str(len(statsUniqueSorted)) +' samples, details: https://salib.readthedocs.io/en/latest/api.html#sobol-sensitivity-analysis \n\n\n')

            for i in range(2,len(list(statsUniqueSorted))-1):
                Y = statsUniqueSorted[list(statsUniqueSorted)[i]]
                print('\n\n..... Sensitivity for: '+list(statsUniqueSorted)[i]+'...........\n\n')
                Si[list(statsUniqueSorted)[i]]=delta.analyze(problem=problem, Y=np.asarray(Y),X=X, print_to_console=True)
    pk.dump(Si,open( problemFolderPath+'\\SiDelta.obj', 'wb' ))

    return Si
# def saveSi(folderPath):

