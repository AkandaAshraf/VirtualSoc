#/home/akanda/virtualSoc/Sobol
from UtilSAlib import *
from HighLevelForSALib import simulateNetworksThreadedNew
import multiprocessing
import pickle as pk
import pandas as pd

newParam_values = SalibPreprocessGetParamsForSobol(numberOfSamples=100,folderPathToSaveParamsAndProblem='/home/akanda/SobolDynamic/')

if __name__ == '__main__':

    pool = multiprocessing.Pool(processes=11)
    #
    pool.map(simulateNetworksThreadedNew, newParam_values)
    #
    print("Number of cpu : ", multiprocessing.cpu_count())



newParam_values = SalibPreprocessGetParamsForSobol(numberOfSamples=100,
                                                       folderPathToSaveParamsAndProblem='/home/akanda/SobolSmall/')

if __name__ == '__main__':
        pool = multiprocessing.Pool(processes=11)
        #
        pool.map(simulateNetworksThreadedNew, newParam_values)
        #
        print("Number of cpu : ", multiprocessing.cpu_count())

    #
    # problemFolderPath = 'home/akanda/virtualSoc/Sobol'
    # statsUniqueSorted = getCleanStats('home/akanda/virtualSoc/Sobol/')
    # Si = getSi(statsUniqueSorted,'home/akanda/virtualSoc/Sobol')
