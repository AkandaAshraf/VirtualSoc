from Node import *
from DNA import *
from Socialiser import *
from PetriDish import *
from Networks import *
import numpy as np
import networkx as nx
from Transfer import *
from HighLevel import*
import sys
sys.setrecursionlimit(1000000)

#
# G2 = RandomSocialGraphAdvanced(labelSplit=[100,300,600],connectionPercentageWithMatchedNodes=30,explorationProbability=0.3,addTraidtionalFeatures=False,additionalFeatureLen=5, npDistFunc=['np.random.randint(18, high=80)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=1,mutualPreferenceIntensity=[3,2,1])
#
# adj2 = G2.A()
# Gx = nx.from_scipy_sparse_matrix(adj2)
# G2.mutateDNA(mutationIntensity=0.8)
# G2.mutateDNAandSocialise(mutationIntensity=0.5)
# G2.socialise()
# adj2 = G2.A()
# test = ['np.random.beta(5,1)','binomial(10,0.5)']
# e = eval(test[0])
# np.linspace(0.1,1,10)
# a = 2+ 3
#
#


# popularityPreferenceIntensityV = np.arange(1, 10, 1)
# popularityPreferenceIntensityV=popularityPreferenceIntensityV.tolist()

simulateNetworksEasy('D:\\SimVirtualSoc\\')
