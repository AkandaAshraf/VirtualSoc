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
import  SocLearner


import sys
from multiprocessing import Pool
sys.setrecursionlimit(100000000)

#
# folderPath = 'D:\\sensitivityAnalaysisVirtualSoc\\'
# modelOutputFolder = 'D:\\outputTest\\'
# modelTypes = ['linear_model.LinearRegression()','linear_model.Ridge()','linear_model.LassoLarsIC(criterion=\'bic\')','linear_model.LassoLarsIC(criterion=\'aic\')',
#               'linear_model.ElasticNet(alpha=1.0, l1_ratio=0.5, fit_intercept=True, normalize=False, copy_X=True, max_iter=1000, tol=0.0001, warm_start=False, random_state=None, selection=\'cyclic\')',
#               'linear_model.Lars(fit_intercept=True, verbose=False, normalize=True, precompute=\'auto\', n_nonzero_coefs=500, eps=2.220446049250313e-16, copy_X=True, fit_path=True, positive=False)',
#               'linear_model.LassoLars(alpha=.1)',
#               'linear_model.BayesianRidge()',
#               'Pipeline([(\'poly\', PolynomialFeatures(degree=3)),(\'linear\', LinearRegression(fit_intercept=False))])',
#               'kernel_ridge.KernelRidge(alpha=1.0)',
#               'svm.SVR()',
#               'linear_model.SGDRegressor(max_iter=1000)',
#               'KNeighborsRegressor.KNeighborsRegressor(n_neighbors=3)',
#               'gaussian_process.GaussianProcessRegressor(kernel=sklearn.gaussian_process.kernels.DotProduct() + sklearn.gaussian_process.kernels.WhiteKernel(), random_state=0)',
#               'tree.DecisionTreeRegressor()',
#               'neural_network.MLPClassifier(alpha=0.01, random_state=1)']

# modelTypes = [ 'neighbors.KNeighborsRegressor(n_neighbors=3)',
#               'gaussian_process.GaussianProcessRegressor(kernel=gaussian_process.kernels.DotProduct() + gaussian_process.kernels.WhiteKernel(), random_state=0)',
#               'tree.DecisionTreeRegressor()',
#               'neural_network.MLPClassifier(alpha=0.01, random_state=1)']
#
#
# SocLearner.trainModelsIndividual(folderPath, modelOutputFolder, modelTypes)]]


#
# import threading
# from threading import Thread
# # #
# G2 = RandomSocialGraphAdvanced(labelSplit=[20,40,60],connectionPercentageWithMatchedNodes=30,connectionPercentageWithMatchedNodesWithRandomness=0.5,explorationProbability=0.3,addTraidtionalFeatures=True,additionalFeatureLen=2, npDistFunc=['np.random.randint(10, high=20)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=1,mutualPreferenceIntensity=[3,2,1],genFeaturesFromSameDistforAllLabel=False)
#
#
# G2.mutateDNA(mutationIntensity=0.9,mutatePreference=True)
# G2.mutateDNAandSocialise(mutationIntensity=0.9)
# G2.socialise()
#
#
# # G2.writeFileA('D:\\testVirtualSoc\\testAdjFile.txt')
# #
# WriteToFile(G2).easySaveEverything('D:\\VirtualSocGCN\soc1')


# # #
# G2 = RandomSocialGraphAdvanced(labelSplit=[500,1000,1500],connectionPercentageWithMatchedNodes=30,connectionPercentageWithMatchedNodesWithRandomness=0.5,explorationProbability=0.3,addTraidtionalFeatures=True,additionalFeatureLen=2, npDistFunc=['np.random.randint(10, high=20)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=1,mutualPreferenceIntensity=[3,2,1],genFeaturesFromSameDistforAllLabel=False,keepHistory=False)
#
#
# # G2.mutateDNA(mutationIntensity=0.9,mutatePreference=True)
# # G2.mutateDNAandSocialise(mutationIntensity=0.9)
# # G2.socialise()
# #
#
# # G2.writeFileA('D:\\testVirtualSoc\\testAdjFile.txt')
# #
# WriteToFile(G2).easySaveEverything('D:\\VirtualSocGCN\\ShufledDNATest2\\')
#
#
# G2 = RandomSocialGraphAdvanced(labelSplit=[5,10,15],connectionPercentageWithMatchedNodes=30,connectionPercentageWithMatchedNodesWithRandomness=0.5,explorationProbability=0.3,addTraidtionalFeatures=True,additionalFeatureLen=2, npDistFunc=['np.random.randint(10, high=20)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=1,mutualPreferenceIntensity=[3,2,1],genFeaturesFromSameDistforAllLabel=False,keepHistory=False)
#
# WriteToFile(G2).easySaveEverything('D:\\VirtualSocGCN\\ShuffledDNATestSmall\\')

#################################
# G2 = RandomSocialGraphAdvanced(labelSplit=[10000,20000,30000],connectionPercentageWithMatchedNodes=30,connectionPercentageWithMatchedNodesWithRandomness=0.5,explorationProbability=0.3,addTraidtionalFeatures=True,additionalFeatureLen=2, npDistFunc=['np.random.randint(10, high=20)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=1,mutualPreferenceIntensity=[3,2,1],genFeaturesFromSameDistforAllLabel=False,keepHistory=False)
#
# WriteToFile(G2).easySaveEverything('D:\\VirtualSocGCN\\ShufledDNATestGiant1\\')
#
# G2 = RandomSocialGraphAdvanced(labelSplit=[10000,20000,30000],connectionPercentageWithMatchedNodes=30,connectionPercentageWithMatchedNodesWithRandomness=0.5,explorationProbability=0.3,addTraidtionalFeatures=True,additionalFeatureLen=2, npDistFunc=['np.random.randint(10, high=20)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=12,mutualPreferenceIntensity=[0.9,0.6,0.3],genFeaturesFromSameDistforAllLabel=False,keepHistory=False)
#
# WriteToFile(G2).easySaveEverything('D:\\VirtualSocGCN\\ShufledDNATestGiant2\\')
#
# dir = 'D:\\VirtualSocGCN\\'
# os.makedirs(dir+'ShuffledDNAFeatureBased1')
# G2 = RandomSocialGraphAdvanced(labelSplit=[2000,4000,6000],connectionPercentageWithMatchedNodes=30,connectionPercentageWithMatchedNodesWithRandomness=0.5,explorationProbability=0.3,addTraidtionalFeatures=True,additionalFeatureLen=2, npDistFunc=['np.random.randint(10, high=20)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=0.3,mutualPreferenceIntensity=[0.3,0.3,0.3],genFeaturesFromSameDistforAllLabel=False,keepHistory=False)
#
# WriteToFile(G2).easySaveEverything('D:\\VirtualSocGCN\\ShuffledDNAFeatureBased1\\')
#
# dir = 'D:\\VirtualSocGCN\\'
# os.makedirs(dir+'ShuffledDNAFeatureBased2')
# G2 = RandomSocialGraphAdvanced(labelSplit=[2000,4000,6000],connectionPercentageWithMatchedNodes=15,connectionPercentageWithMatchedNodesWithRandomness=0.7,explorationProbability=0.7,addTraidtionalFeatures=True,additionalFeatureLen=2, npDistFunc=['np.random.randint(10, high=20)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=0.3,mutualPreferenceIntensity=[0.3,0.3,0.3],genFeaturesFromSameDistforAllLabel=False,keepHistory=False)
#
# WriteToFile(G2).easySaveEverything('D:\\VirtualSocGCN\\ShuffledDNAFeatureBased2\\')



# os.makedirs('D:\\VirtualSocGCN\\ShuffledDNAFeatureBased4')
# G2 = RandomSocialGraphAdvanced(labelSplit=[500,1000,1500,2000,2500],connectionPercentageWithMatchedNodes=50,connectionPercentageWithMatchedNodesWithRandomness=0.3,explorationProbability=0.7,addTraidtionalFeatures=True,additionalFeatureLen=20, npDistFunc=['np.random.randint(10, high=20)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=0.1,mutualPreferenceIntensity=[0.1,0.1,0.1],genFeaturesFromSameDistforAllLabel=False,keepHistory=False)
#
# WriteToFile(G2).easySaveEverything('D:\\VirtualSocGCN\\ShuffledDNAFeatureBased4\\')

# file = 'D:\\VirtualSocGCN\\OptimisedNewNew\\'
# os.makedirs(file)
# G2 = RandomSocialGraphAdvanced(labelSplit=[1000,2000,3000],connectionPercentageWithMatchedNodes=15,connectionPercentageWithMatchedNodesWithRandomness=0.7,explorationProbability=0.7,addTraidtionalFeatures=False,additionalFeatureLen=100, npDistFunc=['np.random.randint(10, high=20)'],popularityPreferenceIntensity=0.1,mutualPreferenceIntensity=[0.9,0.1,0.1],genFeaturesFromSameDistforAllLabel=False,keepHistory=False,useGPU = True)
#
# WriteToFile(G2).easySaveEverything(file)
# file = 'D:\\VirtualSocGCN\\OptimisedNewNew2\\'
# os.makedirs(file)
# G2 = RandomSocialGraphAdvanced(labelSplit=[1000,2000,3000],connectionPercentageWithMatchedNodes=15,connectionPercentageWithMatchedNodesWithRandomness=0.7,explorationProbability=0.7,addTraidtionalFeatures=False,additionalFeatureLen=500, npDistFunc=['np.random.randint(10, high=20)'],popularityPreferenceIntensity=0.1,mutualPreferenceIntensity=[0.9,0.1,0.1],genFeaturesFromSameDistforAllLabel=False,keepHistory=False,useGPU = True)
#
# WriteToFile(G2).easySaveEverything(file)
if __name__ == '__main__':

    file = 'D:\\VirtualSocGCN\\OptimisedNewNewMultiProcess\\'
    G2 = RandomSocialGraphAdvanced(labelSplit=[20,40,50],connectionPercentageWithMatchedNodes=15,connectionPercentageWithMatchedNodesWithRandomness=0.7,explorationProbability=0.7,addTraidtionalFeatures=False,additionalFeatureLen=2000, npDistFunc=['np.random.randint(10, high=20)'],popularityPreferenceIntensity=0.1,mutualPreferenceIntensity=[0.9,0.1,0.1],genFeaturesFromSameDistforAllLabel=False,keepHistory=False,useGPU = True,numberofProcesses=7)

    WriteToFile(G2).easySaveEverything(file)
#
# file = 'D:\\VirtualSocGCN\\test\\'
# os.makedirs(file)
# G2 = RandomSocialGraphAdvanced(labelSplit=[250,500],connectionPercentageWithMatchedNodes=10,connectionPercentageWithMatchedNodesWithRandomness=0.5,explorationProbability=0.1,addTraidtionalFeatures=True,additionalFeatureLen=3, npDistFunc=['np.random.randint(10, high=1500)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=2,mutualPreferenceIntensity=[3,2,1],genFeaturesFromSameDistforAllLabel=False,keepHistory=False)
# WriteToFile(G2).easySaveEverything(file)
#
# file = 'D:\\VirtualSocGCN\\test11\\'
# # os.makedirs(file)
# G2 = RandomSocialGraphAdvanced(labelSplit=[5,10,15],dna='auto',connectionPercentageWithMatchedNodes=95,connectionPercentageWithMatchedNodesWithRandomness=0.15,explorationProbability=0.5,addTraidtionalFeatures=True,additionalFeatureLen=50, npDistFunc=['np.random.randint(10, high=20)','np.random.randint(1, high=10)'],popularityPreferenceIntensity=0.5,mutualPreferenceIntensity=[3,2,1],genFeaturesFromSameDistforAllLabel=False,keepHistory=False)
# G2.socialise()
#
# WriteToFile(G2).easySaveEverything(file)
# file = 'D:\\VirtualSocGCN\\test15\\'
# os.makedirs(file)
# G2 = RandomSocialGraphAdvanced(labelSplit=[1000,2000,3000],dna='auto',connectionPercentageWithMatchedNodes=50,connectionPercentageWithMatchedNodesWithRandomness=0.15,explorationProbability=0.5,addTraidtionalFeatures=True,additionalFeatureLen=1500, npDistFunc=['np.random.randint(1, high=300)','np.random.randint(1, high=10)'],popularityPreferenceIntensity=0.5,mutualPreferenceIntensity=[0.9,0.6,0.3],genFeaturesFromSameDistforAllLabel=False,keepHistory=False)
# G2.socialise()
# WriteToFile(G2).easySaveEverything(file)
# file = 'D:\\VirtualSocGCN\\test13\\'
# os.makedirs(file)
# G2 = RandomSocialGraphAdvanced(labelSplit=[2000,4000,6000],dna='autoWeightless',connectionPercentageWithMatchedNodes=95,connectionPercentageWithMatchedNodesWithRandomness=0.15,explorationProbability=0.5,addTraidtionalFeatures=True,additionalFeatureLen=1500, npDistFunc=['np.random.randint(1, high=300)','np.random.randint(1, high=10)'],popularityPreferenceIntensity=2,mutualPreferenceIntensity=[3,2,1],genFeaturesFromSameDistforAllLabel=False,keepHistory=False)
#
#
# WriteToFile(G2).easySaveEverything(file)



# file = 'D:\\VirtualSocGCN\\ShuffledDNAFeatureBased9\\'
# os.makedirs(file)
# G2 = RandomSocialGraphAdvanced(labelSplit=[500,1000,1500,2000,3000],connectionPercentageWithMatchedNodes=1,connectionPercentageWithMatchedNodesWithRandomness=0.3,explorationProbability=0.5,addTraidtionalFeatures=True,additionalFeatureLen=100, npDistFunc=['np.random.randint(10, high=1500)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=0.5,mutualPreferenceIntensity=[0.9,0.3,0.1],genFeaturesFromSameDistforAllLabel=False,keepHistory=False)
# G2.socialise()
# G2.socialise()
# G2.socialise()
# G2.socialise()
# G2.socialise()
# G2.socialise()
# G2.socialise()
# G2.socialise()
# WriteToFile(G2).easySaveEverything(file)
# file = 'D:\\VirtualSocGCN\\ShuffledDNAFeatureBased10\\'
# os.makedirs(file)
# G2 = RandomSocialGraphAdvanced(labelSplit=[500,1000,1500,2000,3000,4000,5000],connectionPercentageWithMatchedNodes=1,connectionPercentageWithMatchedNodesWithRandomness=0.3,explorationProbability=0.5,addTraidtionalFeatures=True,additionalFeatureLen=100, npDistFunc=['np.random.randint(10, high=1500)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=0.5,mutualPreferenceIntensity=[0.9,0.3,0.1],genFeaturesFromSameDistforAllLabel=False,keepHistory=False)
# G2.socialise()
# G2.socialise()
# G2.socialise()
# G2.socialise()
# G2.socialise()
# G2.socialise()
# G2.socialise()
# G2.socialise()
# WriteToFile(G2).easySaveEverything(file)
# file = 'D:\\VirtualSocGCN\\ShuffledDNAFeatureBased11\\'
# os.makedirs(file)
# G2 = RandomSocialGraphAdvanced(labelSplit=[500,1000,1500,2000,3000,4000,5000],connectionPercentageWithMatchedNodes=90,connectionPercentageWithMatchedNodesWithRandomness=0.3,explorationProbability=0.1,addTraidtionalFeatures=True,additionalFeatureLen=100, npDistFunc=['np.random.randint(10, high=1500)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=0.5,mutualPreferenceIntensity=[0.9,0.3,0.1],genFeaturesFromSameDistforAllLabel=False,keepHistory=False)
# G2.socialise()
# G2.socialise()
#
# WriteToFile(G2).easySaveEverything(file)

###########################################


#
# G2 = RandomSocialGraphAdvanced(labelSplit=[500,1000,1500],connectionPercentageWithMatchedNodes=30,connectionPercentageWithMatchedNodesWithRandomness=0.5,explorationProbability=0.3,addTraidtionalFeatures=True,additionalFeatureLen=2, npDistFunc=['np.random.randint(10, high=20)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=1,mutualPreferenceIntensity=[3,2,1],genFeaturesFromSameDistforAllLabel=False,keepHistory=False)
#
#
# G2.mutateDNA(mutationIntensity=0.9,mutatePreference=True)
# G2.mutateDNAandSocialise(mutationIntensity=0.9)
# G2.socialise()
# #
#
# # G2.writeFileA('D:\\testVirtualSoc\\testAdjFile.txt')
# #
# WriteToFile(G2).easySaveEverything('D:\\VirtualSocGCN\\soc4\\')
# #
#
#
#
# #
# G2 = RandomSocialGraphAdvanced(labelSplit=[500,1000,1500],connectionPercentageWithMatchedNodes=30,connectionPercentageWithMatchedNodesWithRandomness=0.5,explorationProbability=0.3,addTraidtionalFeatures=True,additionalFeatureLen=2, npDistFunc=['np.random.randint(10, high=20)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=1,mutualPreferenceIntensity=[3,2,1],genFeaturesFromSameDistforAllLabel=False)
#
#
# G2.mutateDNA(mutationIntensity=0.9,mutatePreference=True)
# G2.mutateDNAandSocialise(mutationIntensity=0.9)
# G2.socialise()
#
#
# # G2.writeFileA('D:\\testVirtualSoc\\testAdjFile.txt')
# #
# WriteToFile(G2).easySaveEverything('D:\\VirtualSocGCN\soc2')
# # np.random.beta()
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
# print(str(" %6.5f " %t



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
