import Networks as ntk
import numpy as np
import os
import Transfer as tp

def simulateNetworksEasy(folderPath):
    explorationProbabilityV = np.linspace(0.1,1,10)
    connectionPercentageWithMatchedNodesV = np.arange(5,95,10)
    popularityPreferenceIntensityV = np.arange(1,10,1)

    for explorationProbability in explorationProbabilityV:
        for connectionPercentageWithMatchedNodes in connectionPercentageWithMatchedNodesV:
            for popularityPreferenceIntensityV in popularityPreferenceIntensityV:
                os.mkdir(folderPath + '\\' +'EP'+ str(explorationProbability)+ 'CPN'+str(connectionPercentageWithMatchedNodes)+'PPV'+ str(popularityPreferenceIntensityV))

                graphTemp1 = ntk.RandomSocialGraphAdvanced(labelSplit=[500, 1000, 1500], connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                                      explorationProbability=0.3, addTraidtionalFeatures=False, additionalFeatureLen=5,
                                      npDistFunc=['np.random.randint(18, high=80)', 'np.random.binomial(2, 0.5)'],
                                      popularityPreferenceIntensity=1, mutualPreferenceIntensity=[3, 2, 1])
                graphTemp1.mutateDNA(mutationIntensity=0.8)
                graphTemp1.mutateDNAandSocialise(mutationIntensity=0.5)
                graphTemp1.socialise()
                tp.WriteToFile(graphTemp1).easySaveEverything(folderPath + '\\' +'EP'+ str(explorationProbability)+ 'CPN'+str(connectionPercentageWithMatchedNodes)+'PPV'+ str(popularityPreferenceIntensityV)+'\\')

                # graphTemp2 = ntk.RandomSocialGraphAdvanced(labelSplit=[500, 1000, 1500],
                #                                            connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,
                #                                            explorationProbability=0.3, addTraidtionalFeatures=False,
                #                                            additionalFeatureLen=5,
                #                                            npDistFunc=['np.random.randint(18, high=80)',
                #                                                        'np.random.binomial(2, 0.5)'],
                #                                            popularityPreferenceIntensity=1,
                #                                            mutualPreferenceIntensity=[0.9, 0.6, 0.3])

