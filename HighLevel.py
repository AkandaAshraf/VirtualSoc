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
##testtttt
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
    len2 = np.random.uniform(low=0.7, high=1.0, size=2)
    len3 = np.random.uniform(low=0.3, high=0.7, size=2)
    len4 =  np.random.uniform(low=0.0, high=0.3, size=2)

    for i in range(0, 2):
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








def simulateNetworksEasy3(folderPath):
    explorationProbabilityV = np.linspace(0.1,1,10)
    popularityPreferenceIntensityV = np.linspace(1,10,10)

    connectionPercentageWithMatchedNodesV = np.linspace(1,20,10)
    mutualPreferenceIntensityV = []
    len2 = np.random.uniform(low=3, high=5, size=10)
    len3 = np.random.uniform(low=1, high=3, size=10)
    len4 =  np.random.uniform(low=0.01, high=1, size=10)

    for i in range(0, 10):
        mutualPreferenceIntensityV.append([len2[i], len3[i], len4[i]])



    # popularityPreferenceIntensityV = np.arange(1,10,1)
    # popularityPreferenceIntensityV = popularityPreferenceIntensityV.tolist()

    for explorationProbability in explorationProbabilityV:
        for connectionPercentageWithMatchedNodes in connectionPercentageWithMatchedNodesV:
            for popularityPreferenceIntensity in popularityPreferenceIntensityV:
                for mutualPreferenceIntensity in mutualPreferenceIntensityV:
                        os.mkdir(folderPath + '\\' +'EP'+ str(explorationProbability)+ 'CPN'+str(connectionPercentageWithMatchedNodes)+'PP'+ str(popularityPreferenceIntensity)+'mpi'+str(mutualPreferenceIntensity[0])+str(mutualPreferenceIntensity[1])+str(mutualPreferenceIntensity[2]))

                        graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300], connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
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




def simulateNetworksEasyExplorationProbabilityTest(folderPath):
    explorationProbabilityV = np.linspace(0.01,1,300)
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
                        os.mkdir(folderPath + '\\' +'EP'+ str("%6.5f" % explorationProbability)+ 'CPN'+str("%6.3f" % connectionPercentageWithMatchedNodes)+'PP'+ str("%6.3f" % popularityPreferenceIntensity)+'mpi'+ str("%6.3f" % mutualPreferenceIntensity[0])+str("%6.3f" % mutualPreferenceIntensity[1])+str("%6.3f" % mutualPreferenceIntensity[2]))

                        graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300], connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                              explorationProbability=explorationProbability, addTraidtionalFeatures=False, additionalFeatureLen=3,
                                              npDistFunc=['np.random.randint(18, high=80)', 'np.random.binomial(2, 0.5)'],
                                              popularityPreferenceIntensity=popularityPreferenceIntensity, mutualPreferenceIntensity=mutualPreferenceIntensity)
                        graphTemp1.socialise()
                        graphTemp1.socialise()
                        tp.WriteToFile(graphTemp1).easySaveEverything(folderPath + '\\'+'EP'+ str("%6.5f" % explorationProbability)+ 'CPN'+str("%6.3f" % connectionPercentageWithMatchedNodes)+'PP'+ str("%6.3f" % popularityPreferenceIntensity)+'mpi'+str("%6.3f" % mutualPreferenceIntensity[0])+str("%6.3f" % mutualPreferenceIntensity[1])+str("%6.3f" % mutualPreferenceIntensity[2])+'\\')

                        # graphTemp2 = ntk.RandomSocialGraphAdvanced(labelSplit=[500, 1000, 1500],
                        #                                            connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                        #                                            explorationProbability=0.3, addTraidtionalFeatures=False,
                        #                                            additionalFeatureLen=5,
                        #                                            npDistFunc=['np.random.randint(18, high=80)',
                        #                                                        'np.random.binomial(2, 0.5)'],
                        #                                            popularityPreferenceIntensity=1,
                        #                                            mutualPreferenceIntensity=[0.9, 0.6, 0.3])



def simulateNetworksEasyConnectionPercentageWithMatchedNodesTest(folderPath):
    explorationProbabilityV = [0.5]
    popularityPreferenceIntensityV = np.linspace(0.5,1.5,1)

    connectionPercentageWithMatchedNodesV = np.linspace(1,30,300)
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
                        os.mkdir(folderPath + '\\' +'EP'+ str("%6.5f" % explorationProbability)+ 'CPN'+str("%6.3f"%connectionPercentageWithMatchedNodes)+'PP'+ str("%6.3f"%popularityPreferenceIntensity)+'mpi'+ str("%6.3f" % mutualPreferenceIntensity[0])+str("%6.3f" % mutualPreferenceIntensity[1])+str("%6.3f"%mutualPreferenceIntensity[2]))

                        graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300], connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                              explorationProbability=explorationProbability, addTraidtionalFeatures=False, additionalFeatureLen=3,
                                              npDistFunc=['np.random.randint(18, high=80)', 'np.random.binomial(2, 0.5)'],
                                              popularityPreferenceIntensity=popularityPreferenceIntensity, mutualPreferenceIntensity=mutualPreferenceIntensity)
                        graphTemp1.socialise()
                        graphTemp1.socialise()
                        tp.WriteToFile(graphTemp1).easySaveEverything(folderPath + '\\'+'EP'+ str("%6.5f"%explorationProbability)+ 'CPN'+str("%6.3f"%connectionPercentageWithMatchedNodes)+'PP'+ str("%6.3f" % popularityPreferenceIntensity)+'mpi'+str("%6.3f" % mutualPreferenceIntensity[0])+str("%6.3f"%mutualPreferenceIntensity[1])+str("%6.3f"%mutualPreferenceIntensity[2])+'\\')

                        # graphTemp2 = ntk.RandomSocialGraphAdvanced(labelSplit=[500, 1000, 1500],
                        #                                            connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                        #                                            explorationProbability=0.3, addTraidtionalFeatures=False,
                        #                                            additionalFeatureLen=5,
                        #                                            npDistFunc=['np.random.randint(18, high=80)',
                        #                                                        'np.random.binomial(2, 0.5)'],
                        #                                            popularityPreferenceIntensity=1,
                        #                                            mutualPreferenceIntensity=[0.9, 0.6, 0.3])



def simulateNetworksEasypopularityPreferenceIntensityTest1(folderPath):
    explorationProbabilityV = [0.5]
    popularityPreferenceIntensityV = np.linspace(0.1,1,300)

    connectionPercentageWithMatchedNodesV = [10.00]
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
                        os.mkdir(folderPath + '\\' +'EP'+ str("%6.5f" % explorationProbability)+ 'CPN'+str("%6.3f" % connectionPercentageWithMatchedNodes)+'PP'+ str("%6.3f" % popularityPreferenceIntensity)+'mpi'+ str("%6.3f" % mutualPreferenceIntensity[0])+str("%6.3f" % mutualPreferenceIntensity[1])+str("%6.3f" % mutualPreferenceIntensity[2]))

                        graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300], connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                              explorationProbability=explorationProbability, addTraidtionalFeatures=False, additionalFeatureLen=3,
                                              npDistFunc=['np.random.randint(18, high=80)', 'np.random.binomial(2, 0.5)'],
                                              popularityPreferenceIntensity=popularityPreferenceIntensity, mutualPreferenceIntensity=mutualPreferenceIntensity)
                        graphTemp1.socialise()
                        graphTemp1.socialise()
                        tp.WriteToFile(graphTemp1).easySaveEverything(folderPath + '\\'+'EP'+ str("%6.5f" % explorationProbability)+ 'CPN'+str("%6.3f" % connectionPercentageWithMatchedNodes)+'PP'+ str("%6.3f" % popularityPreferenceIntensity)+'mpi'+str("%6.3f" % mutualPreferenceIntensity[0])+str("%6.3f" % mutualPreferenceIntensity[1])+str("%6.3f" % mutualPreferenceIntensity[2])+'\\')

                        # graphTemp2 = ntk.RandomSocialGraphAdvanced(labelSplit=[500, 1000, 1500],
                        #                                            connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                        #                                            explorationProbability=0.3, addTraidtionalFeatures=False,
                        #                                            additionalFeatureLen=5,
                        #                                            npDistFunc=['np.random.randint(18, high=80)',
                        #                                                        'np.random.binomial(2, 0.5)'],
                        #                                            popularityPreferenceIntensity=1,
                        #                                            mutualPreferenceIntensity=[0.9, 0.6, 0.3])


def simulateNetworksEasypopularityPreferenceIntensityTest2(folderPath):
    explorationProbabilityV = [0.5]
    popularityPreferenceIntensityV = np.linspace(1,30,300)

    connectionPercentageWithMatchedNodesV = [10.00]
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
                        os.mkdir(folderPath + '\\' +'EP'+ str("%6.5f" % explorationProbability)+ 'CPN'+str("%6.3f" % connectionPercentageWithMatchedNodes)+'PP'+ str("%6.3f" % popularityPreferenceIntensity)+'mpi'+ str("%6.3f" % mutualPreferenceIntensity[0])+str("%6.3f" % mutualPreferenceIntensity[1])+str("%6.3f" % mutualPreferenceIntensity[2]))

                        graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300], connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                              explorationProbability=explorationProbability, addTraidtionalFeatures=False, additionalFeatureLen=3,
                                              npDistFunc=['np.random.randint(18, high=80)', 'np.random.binomial(2, 0.5)'],
                                              popularityPreferenceIntensity=popularityPreferenceIntensity, mutualPreferenceIntensity=mutualPreferenceIntensity)
                        graphTemp1.socialise()
                        graphTemp1.socialise()
                        tp.WriteToFile(graphTemp1).easySaveEverything(folderPath + '\\'+'EP'+ str("%6.5f" % explorationProbability)+ 'CPN'+str("%6.3f" % connectionPercentageWithMatchedNodes)+'PP'+ str("%6.3f" % popularityPreferenceIntensity)+'mpi'+str("%6.3f" % mutualPreferenceIntensity[0])+str("%6.3f" % mutualPreferenceIntensity[1])+str("%6.3f" % mutualPreferenceIntensity[2])+'\\')

                        # graphTemp2 = ntk.RandomSocialGraphAdvanced(labelSplit=[500, 1000, 1500],
                        #                                            connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                        #                                            explorationProbability=0.3, addTraidtionalFeatures=False,
                        #                                            additionalFeatureLen=5,
                        #                                            npDistFunc=['np.random.randint(18, high=80)',
                        #                                                        'np.random.binomial(2, 0.5)'],
                        #                                            popularityPreferenceIntensity=1,
                        #                                            mutualPreferenceIntensity=[0.9, 0.6, 0.3])

def simulateNetworksEasymutualPreferenceIntensityTest1(folderPath):
    explorationProbabilityV = [0.5]
    popularityPreferenceIntensityV = [1]

    connectionPercentageWithMatchedNodesV = [10.00]
    mutualPreferenceIntensityV = []
    len2 = np.random.uniform(low=0.7, high=1.0, size=300)
    len3 = np.random.uniform(low=0.3, high=0.7, size=300)
    len4 =  np.random.uniform(low=0.0, high=0.3, size=300)

    for i in range(0, 300):
        mutualPreferenceIntensityV.append([len2[i], len3[i], len4[i]])



    # popularityPreferenceIntensityV = np.arange(1,10,1)
    # popularityPreferenceIntensityV = popularityPreferenceIntensityV.tolist()

    for explorationProbability in explorationProbabilityV:
        for connectionPercentageWithMatchedNodes in connectionPercentageWithMatchedNodesV:
            for popularityPreferenceIntensity in popularityPreferenceIntensityV:
                for mutualPreferenceIntensity in mutualPreferenceIntensityV:
                        os.mkdir(folderPath + '\\' +'EP'+ str("%6.5f" % explorationProbability)+ 'CPN'+str("%6.3f" % connectionPercentageWithMatchedNodes)+'PP'+ str("%6.3f" % popularityPreferenceIntensity)+'mpi'+ str("%6.3f" % mutualPreferenceIntensity[0])+str("%6.3f" % mutualPreferenceIntensity[1])+str("%6.3f" % mutualPreferenceIntensity[2]))

                        graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300], connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                              explorationProbability=explorationProbability, addTraidtionalFeatures=False, additionalFeatureLen=3,
                                              npDistFunc=['np.random.randint(18, high=80)', 'np.random.binomial(2, 0.5)'],
                                              popularityPreferenceIntensity=popularityPreferenceIntensity, mutualPreferenceIntensity=mutualPreferenceIntensity)
                        graphTemp1.socialise()
                        graphTemp1.socialise()
                        tp.WriteToFile(graphTemp1).easySaveEverything(folderPath + '\\'+'EP'+ str("%6.5f" % explorationProbability)+ 'CPN'+str("%6.3f" % connectionPercentageWithMatchedNodes)+'PP'+ str("%6.3f" % popularityPreferenceIntensity)+'mpi'+str("%6.3f" % mutualPreferenceIntensity[0])+str("%6.3f" % mutualPreferenceIntensity[1])+str("%6.3f" % mutualPreferenceIntensity[2])+'\\')



def simulateNetworksEasymutualPreferenceIntensityTest2(folderPath):
    explorationProbabilityV = [0.5]
    popularityPreferenceIntensityV = [1]

    connectionPercentageWithMatchedNodesV = [10.00]
    mutualPreferenceIntensityV = []
    len2 = np.random.uniform(low=20, high=30, size=300)
    len3 = np.random.uniform(low=10, high=20, size=300)
    len4 =  np.random.uniform(low=1, high=10, size=300)

    for i in range(0, 300):
        mutualPreferenceIntensityV.append([len2[i], len3[i], len4[i]])



    # popularityPreferenceIntensityV = np.arange(1,10,1)
    # popularityPreferenceIntensityV = popularityPreferenceIntensityV.tolist()

    for explorationProbability in explorationProbabilityV:
        for connectionPercentageWithMatchedNodes in connectionPercentageWithMatchedNodesV:
            for popularityPreferenceIntensity in popularityPreferenceIntensityV:
                for mutualPreferenceIntensity in mutualPreferenceIntensityV:
                        os.mkdir(folderPath + '\\' +'EP'+ str("%6.5f" % explorationProbability)+ 'CPN'+str("%6.3f" % connectionPercentageWithMatchedNodes)+'PP'+ str("%6.3f" % popularityPreferenceIntensity)+'mpi'+ str("%6.3f" % mutualPreferenceIntensity[0])+str("%6.3f" % mutualPreferenceIntensity[1])+str("%6.3f" % mutualPreferenceIntensity[2]))

                        graphTemp1 = RandomSocialGraphAdvanced(labelSplit=[100, 200, 300], connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                              explorationProbability=explorationProbability, addTraidtionalFeatures=False, additionalFeatureLen=3,
                                              npDistFunc=['np.random.randint(18, high=80)', 'np.random.binomial(2, 0.5)'],
                                              popularityPreferenceIntensity=popularityPreferenceIntensity, mutualPreferenceIntensity=mutualPreferenceIntensity)
                        graphTemp1.socialise()
                        graphTemp1.socialise()
                        tp.WriteToFile(graphTemp1).easySaveEverything(folderPath + '\\'+'EP'+ str("%6.5f" % explorationProbability)+ 'CPN'+str("%6.3f" % connectionPercentageWithMatchedNodes)+'PP'+ str("%6.3f" % popularityPreferenceIntensity)+'mpi'+str("%6.3f" % mutualPreferenceIntensity[0])+str("%6.3f" % mutualPreferenceIntensity[1])+str("%6.3f" % mutualPreferenceIntensity[2])+'\\')

                        # graphTemp2 = ntk.RandomSocialGraphAdvanced(labelSplit=[500, 1000, 1500],
                        #                                            connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                        #                                            explorationProbability=0.3, addTraidtionalFeatures=False,
                        #                                            additionalFeatureLen=5,
                        #                                            npDistFunc=['np.random.randint(18, high=80)',
                        #                                                        'np.random.binomial(2, 0.5)'],
                        #                                            popularityPreferenceIntensity=1,
                        #                                            mutualPreferenceIntensity=[0.9, 0.6, 0.3])

