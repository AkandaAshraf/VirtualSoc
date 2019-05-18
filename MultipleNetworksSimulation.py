import os
import Transfer as tp

from Networks import *
from SALib.sample import saltelli

import numpy as np

import multiprocessing
import pickle as pk
import pandas as pd


def iter_rows(params, useGPU, numberofProcesses, createInGPUMem,evalParam):
    for row in params.iterrows():
        index, row = row
        yield [row.tolist(), [useGPU], [numberofProcesses], [createInGPUMem], [evalParam]]
def Simulate(params,processes,useGPU=False, numberofProcesses=None, createInGPUMem=False,evalParam='graph.socialise()'):
    # params = [params]
    with multiprocessing.Pool(processes=processes) as pool:
            for i in pool.imap_unordered(simulateNetworksThreaded, iter_rows(params,useGPU, numberofProcesses, createInGPUMem,evalParam)):
                pass
    print('Finished')

def SalibPreprocessGetParamsForSobol(numberOfSamples,folderPathToSaveParamsAndProblem,labelSplit, npDistFunc, bounds, features):
    #https://salib.readthedocs.io/en/latest/basics.html
    problem = {
        'num_vars': 6,
        'names': ['explorationProbabilityV', 'popularityPreferenceIntensityV', 'connectionPercentageWithMatchedNodesV', 'mutualPreferenceIntensityV2', 'mutualPreferenceIntensityV3', 'mutualPreferenceIntensityV4'],
        'bounds':bounds
    }
    pk.dump(problem,open( folderPathToSaveParamsAndProblem+'/problemPickle.obj', 'wb' ) )
    param_values = saltelli.sample(problem, numberOfSamples)
    l = len(param_values)
    indices = np.arange(0, l)
    indices = indices.reshape(l,1)
    newParam_values = np.concatenate((param_values, indices), axis=1)
    newParam_valuesDF=pd.DataFrame(newParam_values)
    newParam_valuesDF.columns = ['explorationProbabilityV', 'popularityPreferenceIntensityV', 'connectionPercentageWithMatchedNodesV', 'mutualPreferenceIntensityV2', 'mutualPreferenceIntensityV3', 'mutualPreferenceIntensityV4','index']
    newParam_valuesDF.insert(loc=7,column='labelSplit',value=[labelSplit]*l)
    newParam_valuesDF.insert(loc=8,column='features', value=[features]*l)

    newParam_valuesDF.insert(loc=9,column='npDistFuncs', value=[npDistFunc]*l)
    newParam_valuesDF.insert(loc=10,column='path', value=[folderPathToSaveParamsAndProblem]*l)

    newParam_valuesDF.to_csv(folderPathToSaveParamsAndProblem+'params.csv')
    #
    # np.savetxt(folderPathToSaveParamsAndProblem+'/params', param_values, fmt='%.18e', delimiter=' ',
    #            newline='\n', header='', footer='', comments='# ', encoding=None)
    return newParam_valuesDF



def simulateNetworksThreaded(param_value):
        param_value = sum(param_value, [])

        explorationProbability = param_value[0]
        popularityPreferenceIntensity = param_value[1]
        connectionPercentageWithMatchedNodes = param_value[2]
        mutualPreferenceIntensity = [param_value[3], param_value[4], param_value[5]]
        labelSplit = param_value[7]
        features = param_value[8]

        npDistFuncs = param_value[9]
        folderPath = param_value[10]
        useGPU =  param_value[11]
        numberofProcesses= param_value[12]
        createInGPUMem = param_value[13]
        evalParam = param_value[14]


        i = param_value[6]
        os.mkdir(folderPath + '/' + str(i))

        graph = RandomSocialGraphAdvanced(labelSplit=labelSplit,
                                               connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                               explorationProbability=explorationProbability,
                                               addTraidtionalFeatures=False, additionalFeatureLen=features,
                                               npDistFunc=npDistFuncs,
                                               popularityPreferenceIntensity=popularityPreferenceIntensity,
                                               mutualPreferenceIntensity=mutualPreferenceIntensity,useGPU=useGPU,numberofProcesses=numberofProcesses,createInGPUMem=createInGPUMem)
        eval(evalParam)

        # graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300],
        #                                        connectionPercentageWithMatchedNodes=param_value[2],
        #                                        explorationProbability=param_value[0],
        #                                        addTraidtionalFeatures=False, additionalFeatureLen=3,
        #                                        npDistFunc=['np.random.randint(18, high=80)',
        #                                                    'np.random.binomial(2, 0.5)'],
        #                                        popularityPreferenceIntensity=param_value[1],
        #                                        mutualPreferenceIntensity=[param_value[3],param_value[4],param_value[5]])
        tp.WriteToFile(graph).easySaveEverything(
            folderPath +str(i)+ '/')
        i +=1

