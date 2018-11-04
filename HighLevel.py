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

def simulateNetworksEasy(folderPath):
    explorationProbabilityV = np.linspace(0.1,0.5,3)
    connectionPercentageWithMatchedNodesV = np.arange(5,30,3)



    # popularityPreferenceIntensityV = np.arange(1,10,1)
    # popularityPreferenceIntensityV = popularityPreferenceIntensityV.tolist()

    for explorationProbability in explorationProbabilityV:
        for connectionPercentageWithMatchedNodes in connectionPercentageWithMatchedNodesV:
            for popularityPreferenceIntensity in range(1, 5):
                    os.mkdir(folderPath + '\\' +'EP'+ str(explorationProbability)+ 'CPN'+str(connectionPercentageWithMatchedNodes)+'PPV'+ str(popularityPreferenceIntensity))

                    graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[500, 1000, 1500], connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                          explorationProbability=explorationProbability, addTraidtionalFeatures=True, additionalFeatureLen=2,
                                          npDistFunc=['np.random.randint(18, high=80)', 'np.random.binomial(2, 0.5)'],
                                          popularityPreferenceIntensity=popularityPreferenceIntensity, mutualPreferenceIntensity=[3, 2, 1])
                    graphTemp1.mutateDNAandSocialise(mutationIntensity=0.3)
                    graphTemp1.mutateDNAandSocialise(mutationIntensity=0.5)
                    graphTemp1.mutateDNAandSocialise(mutationIntensity=0.7)

                    graphTemp1.socialise()
                    tp.WriteToFile(graphTemp1).easySaveEverything(folderPath + '\\' +'EP'+ str(explorationProbability)+ 'CPN'+str(connectionPercentageWithMatchedNodes)+'PPV'+ str(popularityPreferenceIntensity)+'\\')

                    # graphTemp2 = ntk.RandomSocialGraphAdvanced(labelSplit=[500, 1000, 1500],
                    #                                            connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                    #                                            explorationProbability=0.3, addTraidtionalFeatures=False,
                    #                                            additionalFeatureLen=5,
                    #                                            npDistFunc=['np.random.randint(18, high=80)',
                    #                                                        'np.random.binomial(2, 0.5)'],
                    #                                            popularityPreferenceIntensity=1,
                    #                                            mutualPreferenceIntensity=[0.9, 0.6, 0.3])


def simulateNetworksEasy2(folderPath):
    explorationProbabilityV = np.linspace(0.01,0.1,2)
    popularityPreferenceIntensityV = np.linspace(0.5,1.5,2)

    connectionPercentageWithMatchedNodesV = np.linspace(0.5,2,2)
    mutualPreferenceIntensityV = []
    len2 = np.random.uniform(low=0.7, high=1.0, size=3)
    len3 = np.random.uniform(low=0.3, high=0.7, size=3)
    len4 =  np.random.uniform(low=0.0, high=0.3, size=3)

    for i in range(0, 3):
        mutualPreferenceIntensityV.append([len2[i], len3[i], len4[i]])



    # popularityPreferenceIntensityV = np.arange(1,10,1)
    # popularityPreferenceIntensityV = popularityPreferenceIntensityV.tolist()

    for explorationProbability in explorationProbabilityV:
        for connectionPercentageWithMatchedNodes in connectionPercentageWithMatchedNodesV:
            for popularityPreferenceIntensity in popularityPreferenceIntensityV:
                for mutualPreferenceIntensity in mutualPreferenceIntensityV:
                        os.mkdir(folderPath + '\\' +'EP'+ str(explorationProbability)+ 'CPN'+str(connectionPercentageWithMatchedNodes)+'PP'+ str(popularityPreferenceIntensity)+'mpi'+str(mutualPreferenceIntensity[0])+str(mutualPreferenceIntensity[1])+str(mutualPreferenceIntensity[2]))

                        graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[500, 1000, 1500], connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                              explorationProbability=explorationProbability, addTraidtionalFeatures=False, additionalFeatureLen=3,
                                              npDistFunc=['np.random.randint(18, high=80)', 'np.random.binomial(2, 0.5)'],
                                              popularityPreferenceIntensity=popularityPreferenceIntensity, mutualPreferenceIntensity=mutualPreferenceIntensity)
                        graphTemp1.mutateDNAandSocialise(mutationIntensity=0.3)
                        graphTemp1.socialise()
                        graphTemp1.mutateDNAandSocialise(mutationIntensity=0.7)
                        graphTemp1.socialise()
                        tp.WriteToFile(graphTemp1).easySaveEverything(folderPath + '\\'+'EP'+ str(explorationProbability)+ 'CPN'+str(connectionPercentageWithMatchedNodes)+'PP'+ str(popularityPreferenceIntensity)+'mpi'+str(mutualPreferenceIntensity[0])+str(mutualPreferenceIntensity[1])+str(mutualPreferenceIntensity[2])+'\\')

                        # graphTemp2 = ntk.RandomSocialGraphAdvanced(labelSplit=[500, 1000, 1500],
                        #                                            connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                        #                                            explorationProbability=0.3, addTraidtionalFeatures=False,
                        #                                            additionalFeatureLen=5,
                        #                                            npDistFunc=['np.random.randint(18, high=80)',
                        #                                                        'np.random.binomial(2, 0.5)'],
                        #                                            popularityPreferenceIntensity=1,
                        #                                            mutualPreferenceIntensity=[0.9, 0.6, 0.3])


def simulateNetworksEasyTest(folderPath):
    explorationProbabilityV = np.linspace(0.01,0.1,1)
    popularityPreferenceIntensityV = np.linspace(0.5,1.5,1)

    connectionPercentageWithMatchedNodesV = np.linspace(0.5,2,1)
    mutualPreferenceIntensityV = []
    len2 = np.random.uniform(low=0.7, high=1.0, size=1)
    len3 = np.random.uniform(low=0.3, high=0.7, size=1)
    len4 =  np.random.uniform(low=0.0, high=0.3, size=1)

    for i in range(0, 1):
        mutualPreferenceIntensityV.append([len2[i], len3[i], len4[i]])



    # popularityPreferenceIntensityV = np.arange(1,10,1)
    # popularityPreferenceIntensityV = popularityPreferenceIntensityV.tolist()

    for explorationProbability in explorationProbabilityV:
        for connectionPercentageWithMatchedNodes in connectionPercentageWithMatchedNodesV:
            for popularityPreferenceIntensity in popularityPreferenceIntensityV:
                for mutualPreferenceIntensity in mutualPreferenceIntensityV:
                        os.mkdir(folderPath + '\\' +'EP'+ str(explorationProbability)+ 'CPN'+str(connectionPercentageWithMatchedNodes)+'PP'+ str(popularityPreferenceIntensity)+'mpi'+str(mutualPreferenceIntensity[0])+str(mutualPreferenceIntensity[1])+str(mutualPreferenceIntensity[2]))

                        graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[10, 20, 30], connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                              explorationProbability=explorationProbability, addTraidtionalFeatures=False, additionalFeatureLen=3,
                                              npDistFunc=['np.random.randint(18, high=80)', 'np.random.binomial(2, 0.5)'],
                                              popularityPreferenceIntensity=popularityPreferenceIntensity, mutualPreferenceIntensity=mutualPreferenceIntensity)
                        graphTemp1.mutateDNAandSocialise(mutationIntensity=0.3)
                        graphTemp1.socialise()
                        graphTemp1.mutateDNAandSocialise(mutationIntensity=0.7)
                        graphTemp1.socialise()
                        tp.WriteToFile(graphTemp1).easySaveEverything(folderPath + '\\'+'EP'+ str(explorationProbability)+ 'CPN'+str(connectionPercentageWithMatchedNodes)+'PP'+ str(popularityPreferenceIntensity)+'mpi'+str(mutualPreferenceIntensity[0])+str(mutualPreferenceIntensity[1])+str(mutualPreferenceIntensity[2])+'\\')

                        # graphTemp2 = ntk.RandomSocialGraphAdvanced(labelSplit=[500, 1000, 1500],
                        #                                            connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                        #                                            explorationProbability=0.3, addTraidtionalFeatures=False,
                        #                                            additionalFeatureLen=5,
                        #                                            npDistFunc=['np.random.randint(18, high=80)',
                        #                                                        'np.random.binomial(2, 0.5)'],
                        #                                            popularityPreferenceIntensity=1,
                        #                                            mutualPreferenceIntensity=[0.9, 0.6, 0.3])

