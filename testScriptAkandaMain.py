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
from UtilSAlib import *





import sys
from multiprocessing import Pool
sys.setrecursionlimit(1000000)
#
#
# folderPath = 'D:\\sensitivityAnalaysisVirtualSoc\\'
# modelOutputFolder = 'D:\\testFolder\\'
# # modelTypes = ['linear_model.LinearRegression()','linear_model.Ridge()','linear_model.LassoLarsIC(criterion=\'bic\')','linear_model.LassoLarsIC(criterion=\'aic\')',
# #               'linear_model.ElasticNet(alpha=1.0, l1_ratio=0.5, fit_intercept=True, normalize=False, copy_X=True, max_iter=1000, tol=0.0001, warm_start=False, random_state=None, selection=\'cyclic\')',
# #               'linear_model.Lars(fit_intercept=True, verbose=False, normalize=True, precompute=\'auto\', n_nonzero_coefs=500, eps=2.220446049250313e-16, copy_X=True, fit_path=True, positive=False)',
# #               'linear_model.LassoLars(alpha=.1)',
# #               'linear_model.BayesianRidge()',
# #               'Pipeline([(\'poly\', PolynomialFeatures(degree=3)),(\'linear\', LinearRegression(fit_intercept=False))])',
# #               'kernel_ridge.KernelRidge(alpha=1.0)',
# #               'svm.SVR()',
# #               'linear_model.SGDRegressor(max_iter=1000)',
# #               'KNeighborsRegressor.KNeighborsRegressor(n_neighbors=3)',
# #               'gaussian_process.GaussianProcessRegressor(kernel=sklearn.gaussian_process.kernels.DotProduct() + sklearn.gaussian_process.kernels.WhiteKernel(), random_state=0)',
# #               'tree.DecisionTreeRegressor()',
# #               'neural_network.MLPClassifier(alpha=0.01, random_state=1)']
#
# modelTypes = ['gaussian_process.GaussianProcessRegressor(kernel=gaussian_process.kernels.DotProduct() + gaussian_process.kernels.WhiteKernel(), random_state=0)',
#               'tree.DecisionTreeRegressor()',
#               'neural_network.MLPClassifier(alpha=0.01, random_state=1)']
#
#
# SocLearner.trainModelsIndividual(folderPath, modelOutputFolder, modelTypes)



import threading
from threading import Thread
# #
#
# sys.setrecursionlimit(1000000)
#
# G = RandomSocialGraphAdvanced(labelSplit=[100,200,300],connectionPercentageWithMatchedNodes=30,explorationProbability=0.3,addTraidtionalFeatures=False,additionalFeatureLen=5, npDistFunc=['np.random.randint(18, high=80)','np.random.binomial(2, 0.5)'],popularityPreferenceIntensity=1,mutualPreferenceIntensity=[3,2,1])
#
# adj2 = G.A()
#
# G.mutateDNA(mutationIntensity=0.8)
# G.mutateDNAandSocialise(mutationIntensity=0.5)
# G.socialise()
#
# adj2 = G.A()
#
# G.writeFileA('D://testAdjFile.txt')
#
# WriteToFile(G).easySaveEverything('D:\\VirtualSocTest2\\test1\\')


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

if __name__ == '__main__':

    # from here call the simulation methods
    # newParam_values=SalibPreprocessGetParamsForSobol(1000,folderPathToSaveParamsAndProblem='/home/akanda/virtualSoc/big/')
    # pool = multiprocessing.Pool(processes=11)
    # #
    # pool.map(simulateNetworksThreaded, newParam_values)
    # newParam_values = SalibPreprocessGetParamsForSobol(10000,folderPathToSaveParamsAndProblem='/home/akanda/virtualSoc/giant/')
    newParam_values = getExistingParams(folderPathParm='/home/akanda/virtualSoc/giant/', folderPathGenerated=None)
    pool = multiprocessing.Pool(processes=11)
    #
    pool.map(simulateNetworksThreadedGiant, newParam_values)
    #