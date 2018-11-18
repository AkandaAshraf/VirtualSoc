import Networks as ntk
import numpy as np
import os
import Transfer as tp
from Node import *
from DNA import *
from Socialiser import *
from PetriDish import *
from Networks import *
import numpy as np


def simulateNetworks(param_values, folderPath):
    i = 0
    for param_value in param_values:
        explorationProbability = param_value[0]
        popularityPreferenceIntensity = param_value[1]
        connectionPercentageWithMatchedNodes = param_value[2]
        mutualPreferenceIntensity = [param_value[3], param_value[4], param_value[5]]
        os.mkdir(folderPath + '\\' + str(i))

        graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300],
                                               connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                               explorationProbability=explorationProbability,
                                               addTraidtionalFeatures=False, additionalFeatureLen=3,
                                               npDistFunc=['np.random.randint(18, high=80)',
                                                           'np.random.binomial(2, 0.5)'],
                                               popularityPreferenceIntensity=popularityPreferenceIntensity,
                                               mutualPreferenceIntensity=mutualPreferenceIntensity)

        # graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300],
        #                                        connectionPercentageWithMatchedNodes=param_value[2],
        #                                        explorationProbability=param_value[0],
        #                                        addTraidtionalFeatures=False, additionalFeatureLen=3,
        #                                        npDistFunc=['np.random.randint(18, high=80)',
        #                                                    'np.random.binomial(2, 0.5)'],
        #                                        popularityPreferenceIntensity=param_value[1],
        #                                        mutualPreferenceIntensity=[param_value[3],param_value[4],param_value[5]])
        tp.WriteToFile(graphTemp1).easySaveEverything(
            folderPath +str(i)+ '\\')
        i +=1




def simulateNetworksThreaded(param_value):
        folderPath = 'H:\\SobolBig\\'
        explorationProbability = param_value[0]
        popularityPreferenceIntensity = param_value[1]
        connectionPercentageWithMatchedNodes = param_value[2]
        mutualPreferenceIntensity = [param_value[3], param_value[4], param_value[5]]
        i = param_value[6]
        os.mkdir(folderPath + '\\' + str(i))

        graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[300, 600, 900],
                                               connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                               explorationProbability=explorationProbability,
                                               addTraidtionalFeatures=False, additionalFeatureLen=3,
                                               npDistFunc=['np.random.randint(18, high=80)',
                                                           'np.random.binomial(2, 0.5)'],
                                               popularityPreferenceIntensity=popularityPreferenceIntensity,
                                               mutualPreferenceIntensity=mutualPreferenceIntensity)

        # graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300],
        #                                        connectionPercentageWithMatchedNodes=param_value[2],
        #                                        explorationProbability=param_value[0],
        #                                        addTraidtionalFeatures=False, additionalFeatureLen=3,
        #                                        npDistFunc=['np.random.randint(18, high=80)',
        #                                                    'np.random.binomial(2, 0.5)'],
        #                                        popularityPreferenceIntensity=param_value[1],
        #                                        mutualPreferenceIntensity=[param_value[3],param_value[4],param_value[5]])
        tp.WriteToFile(graphTemp1).easySaveEverything(
            folderPath +str(i)+ '\\')
        i +=1




def simulateNetworksThreadedGiant(param_value):
        folderPath = 'H:\\SobolGiant\\'
        explorationProbability = param_value[0]
        popularityPreferenceIntensity = param_value[1]
        connectionPercentageWithMatchedNodes = param_value[2]
        mutualPreferenceIntensity = [param_value[3], param_value[4], param_value[5]]
        i = param_value[6]
        os.mkdir(folderPath + '\\' + str(i))

        graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[300, 600, 900],
                                               connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                               explorationProbability=explorationProbability,
                                               addTraidtionalFeatures=False, additionalFeatureLen=3,
                                               npDistFunc=['np.random.randint(18, high=80)',
                                                           'np.random.binomial(2, 0.5)'],
                                               popularityPreferenceIntensity=popularityPreferenceIntensity,
                                               mutualPreferenceIntensity=mutualPreferenceIntensity)

        # graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300],
        #                                        connectionPercentageWithMatchedNodes=param_value[2],
        #                                        explorationProbability=param_value[0],
        #                                        addTraidtionalFeatures=False, additionalFeatureLen=3,
        #                                        npDistFunc=['np.random.randint(18, high=80)',
        #                                                    'np.random.binomial(2, 0.5)'],
        #                                        popularityPreferenceIntensity=param_value[1],
        #                                        mutualPreferenceIntensity=[param_value[3],param_value[4],param_value[5]])
        tp.WriteToFile(graphTemp1).easySaveEverything(
            folderPath +str(i)+ '\\')
        i +=1


def simulateNetworksThreadedFAST(param_value):
        folderPath = 'D:\\sensitivityAnalaysisVirtualSocFAST\\'
        explorationProbability = param_value[0]
        popularityPreferenceIntensity = param_value[1]
        connectionPercentageWithMatchedNodes = param_value[2]
        mutualPreferenceIntensity = [param_value[3], param_value[4], param_value[5]]
        i = param_value[6]
        os.mkdir(folderPath + '\\' + str(i))

        graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300],
                                               connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                               explorationProbability=explorationProbability,
                                               addTraidtionalFeatures=False, additionalFeatureLen=3,
                                               npDistFunc=['np.random.randint(18, high=80)',
                                                           'np.random.binomial(2, 0.5)'],
                                               popularityPreferenceIntensity=popularityPreferenceIntensity,
                                               mutualPreferenceIntensity=mutualPreferenceIntensity)

        # graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300],
        #                                        connectionPercentageWithMatchedNodes=param_value[2],
        #                                        explorationProbability=param_value[0],
        #                                        addTraidtionalFeatures=False, additionalFeatureLen=3,
        #                                        npDistFunc=['np.random.randint(18, high=80)',
        #                                                    'np.random.binomial(2, 0.5)'],
        #                                        popularityPreferenceIntensity=param_value[1],
        #                                        mutualPreferenceIntensity=[param_value[3],param_value[4],param_value[5]])
        tp.WriteToFile(graphTemp1).easySaveEverything(
            folderPath +str(i)+ '\\')
        i +=1


def simulateNetworksThreadedRBDFAST(param_value):
    folderPath = 'D:\\sensitivityAnalaysisVirtualSocRBDFAST\\'
    explorationProbability = param_value[0]
    popularityPreferenceIntensity = param_value[1]
    connectionPercentageWithMatchedNodes = param_value[2]
    mutualPreferenceIntensity = [param_value[3], param_value[4], param_value[5]]
    i = param_value[6]
    os.mkdir(folderPath + '\\' + str(i))

    graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300],
                                           connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                           explorationProbability=explorationProbability,
                                           addTraidtionalFeatures=False, additionalFeatureLen=3,
                                           npDistFunc=['np.random.randint(18, high=80)',
                                                       'np.random.binomial(2, 0.5)'],
                                           popularityPreferenceIntensity=popularityPreferenceIntensity,
                                           mutualPreferenceIntensity=mutualPreferenceIntensity)

    # graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300],
    #                                        connectionPercentageWithMatchedNodes=param_value[2],
    #                                        explorationProbability=param_value[0],
    #                                        addTraidtionalFeatures=False, additionalFeatureLen=3,
    #                                        npDistFunc=['np.random.randint(18, high=80)',
    #                                                    'np.random.binomial(2, 0.5)'],
    #                                        popularityPreferenceIntensity=param_value[1],
    #                                        mutualPreferenceIntensity=[param_value[3],param_value[4],param_value[5]])
    tp.WriteToFile(graphTemp1).easySaveEverything(
        folderPath + str(i) + '\\')
    i += 1


def simulateNetworksThreadedRBDdelta(param_value):
    folderPath = 'D:\\sensitivityAnalaysisVirtualDelta\\'
    explorationProbability = param_value[0]
    popularityPreferenceIntensity = param_value[1]
    connectionPercentageWithMatchedNodes = param_value[2]
    mutualPreferenceIntensity = [param_value[3], param_value[4], param_value[5]]
    i = param_value[6]
    os.mkdir(folderPath + '\\' + str(i))

    graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300],
                                           connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                           explorationProbability=explorationProbability,
                                           addTraidtionalFeatures=False, additionalFeatureLen=3,
                                           npDistFunc=['np.random.randint(18, high=80)',
                                                       'np.random.binomial(2, 0.5)'],
                                           popularityPreferenceIntensity=popularityPreferenceIntensity,
                                           mutualPreferenceIntensity=mutualPreferenceIntensity)

    # graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300],
    #                                        connectionPercentageWithMatchedNodes=param_value[2],
    #                                        explorationProbability=param_value[0],
    #                                        addTraidtionalFeatures=False, additionalFeatureLen=3,
    #                                        npDistFunc=['np.random.randint(18, high=80)',
    #                                                    'np.random.binomial(2, 0.5)'],
    #                                        popularityPreferenceIntensity=param_value[1],
    #                                        mutualPreferenceIntensity=[param_value[3],param_value[4],param_value[5]])
    tp.WriteToFile(graphTemp1).easySaveEverything(
        folderPath + str(i) + '\\')
    i += 1



def simulateNetworksThreadedFF(param_value):
    folderPath = 'D:\\sensitivityAnalaysisVirtualFF\\'
    explorationProbability = param_value[0]
    popularityPreferenceIntensity = param_value[1]
    connectionPercentageWithMatchedNodes = param_value[2]
    mutualPreferenceIntensity = [param_value[3], param_value[4], param_value[5]]
    i = param_value[6]
    os.mkdir(folderPath + '\\' + str(i))

    graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300],
                                           connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                           explorationProbability=explorationProbability,
                                           addTraidtionalFeatures=False, additionalFeatureLen=3,
                                           npDistFunc=['np.random.randint(18, high=80)',
                                                       'np.random.binomial(2, 0.5)'],
                                           popularityPreferenceIntensity=popularityPreferenceIntensity,
                                           mutualPreferenceIntensity=mutualPreferenceIntensity)

    # graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300],
    #                                        connectionPercentageWithMatchedNodes=param_value[2],
    #                                        explorationProbability=param_value[0],
    #                                        addTraidtionalFeatures=False, additionalFeatureLen=3,
    #                                        npDistFunc=['np.random.randint(18, high=80)',
    #                                                    'np.random.binomial(2, 0.5)'],
    #                                        popularityPreferenceIntensity=param_value[1],
    #                                        mutualPreferenceIntensity=[param_value[3],param_value[4],param_value[5]])
    tp.WriteToFile(graphTemp1).easySaveEverything(
        folderPath + str(i) + '\\')
    i += 1





