from Node import *
from DNA import *
from Socialiser import *
from PetriDish import *
from Networks import *
import numpy as np
import networkx as nx
from Transfer import *
from HighLevel import*
from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami
import numpy as np
from HighLevelForSALib import *


import sys
from multiprocessing import Pool
sys.setrecursionlimit(1000000)
import threading
from threading import Thread
#
G2 = RandomSocialGraphAdvanced(labelSplit=[100,200,300],connectionPercentageWithMatchedNodes=30,explorationProbability=0.3,addTraidtionalFeatures=False,additionalFeatureLen=5, npDistFunc=['np.random.randint(18, high=80)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=1,mutualPreferenceIntensity=[3,2,1])

adj2 = G2.A()

G2.mutateDNA(mutationIntensity=0.8)
G2.mutateDNAandSocialise(mutationIntensity=0.5)
G2.socialise()

adj2 = G2.A()

# G2.writeFileA('D://testAdjFile.txt')

# G2.adjPower([2])
# WriteToFile(G2).easySaveEverything('D:\\VirtualSocTest2\\test1\\')
# WriteToFile(G2).easySaveEverything('D:\\VirtualSocTest2\\test2\\')

# np.random.beta()
# test = ['np.random.beta(5,1)','binomial(10,0.5)']

#
#


# # popularityPreferenceIntensityV = np.arange(1, 10, 1)
# # popularityPreferenceIntensityV=popularityPreferenceIntensityV.tolist()
# if __name__ == '__main__':
#     # pool = Pool(processes=20)
#     # pool.map_async(simulateNetworksEasy2('D:\\newVirtualSim1\\'))
#     # pool.map_async(simulateNetworksEasy3('D:\\newVirtualSim2\\'))
#
#     t1 = Thread(target=simulateNetworksEasy2('D:\\newVirtualSim1\\'))
#     t2 = Thread(target=simulateNetworksEasy3('D:\\newVirtualSim2\\'))
#     t1.start()
#     t2.start()
# simulateNetworksEasy2('D:\\VirtualSocEP\\')
# simulateNetworksEasyExplorationProbabilityTest('D:\\VirtualSocEP\\')
# simulateNetworksEasyConnectionPercentageWithMatchedNodesTest('D:\\VirtualSocPCMN\\')
# simulateNetworksEasypopularityPreferenceIntensityTest1('D:\\VirtualSocPP1\\')
# simulateNetworksEasypopularityPreferenceIntensityTest2('D:\\VirtualSocPP2\\')
# simulateNetworksEasymutualPreferenceIntensityTest1('D:\\VirtualSocMP1\\')
# simulateNetworksEasymutualPreferenceIntensityTest2('D:\\VirtualSocMP2\\')
# t = 0.0123
# print(str(" %6.5f " %t))



# problem = {
#     'num_vars': 6,
#     'names': ['explorationProbabilityV', 'popularityPreferenceIntensityV', 'connectionPercentageWithMatchedNodesV', 'mutualPreferenceIntensityV2', 'mutualPreferenceIntensityV3', 'mutualPreferenceIntensityV4'],
#     'bounds': [[0.0,1.0],
#                [0.1, 10],
#                [1, 80],
#                [0.7, 0.9],
#                [0.3, 0.6],
#                [0.1, 0.2]]
# }
#
# param_values = saltelli.sample(problem, 1)
#
#
# simulateNetworks(param_values=param_values,folderPath='D:\\sensitivityAnalaysisVirtualSoc\\')
