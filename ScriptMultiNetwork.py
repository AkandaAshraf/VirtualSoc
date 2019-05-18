import sys
from MultipleNetworksSimulation import Simulate, SalibPreprocessGetParamsForSobol
import os
sys.setrecursionlimit(100000000)



if __name__ == '__main__':

    folder = 'H:/cpu_Networksim_test_multiprocess4/' # path where the folder will be created with all the generated networks
    os.makedirs(folder) # make dir if not created already


    params = SalibPreprocessGetParamsForSobol(numberOfSamples=3, # number of samples. To generate sample parameters SALib's sobol
                                              # method is used (https://salib.readthedocs.io/en/latest/) N * (D + 2) , where D is the number of parameters and N = numberOfSamples
                                              folderPathToSaveParamsAndProblem=folder, # the path where the params will be generated and the graph will also be generated there
                                              labelSplit=[100, 200, 300], #
                                              features= 15,
                                              npDistFunc=['np.random.randint(18, high=80)',
                                                          'np.random.binomial(2, 0.5)'],# the distribution function
                                  # from where the features will be generated. Usually it is a numpy random number generator
                                  #function. However, the size parameter should not be filled while passing
                                  # the function as a string.
                                  #  If the number of features equals to the number of
                                  # passed distribution functions then each of them will be used with the corresponding
                                  # feature. Otherwise a features will be generated based on a randomly selected passed function.
                                  # A feature for all the nodes for a single network will be generated from a single function.
                                              bounds=[[0.1,1.0], [0.1, 10], [1, 80],[0.7, 0.9], [0.3, 0.6],[0.1, 0.2]] )
    if __name__ == '__main__':
         Simulate(processes=6, # number of cpu process that should be used
                  params=params, # params generated by SalibPreprocessGetParamsForSobol function. Or a user defined
                  # list of parameters as a pandas dataframe as the following row and col format:

                  #explorationProbabilityV,popularityPreferenceIntensityV,connectionPercentageWithMatchedNodesV,mutualPreferenceIntensityV2,mutualPreferenceIntensityV3,mutualPreferenceIntensityV4,index,labelSplit,features,npDistFuncs,path
                  # 0.14130859375000002,1.05712890625,41.9658203125,0.8353515625,0.38408203124999996,0.19072265625,1.0,"[100, 200, 300]",15,"['np.random.randint(18, high=80)', 'np.random.binomial(2, 0.5)']",H:/cpu_Networksim_test_multiprocess3/
                  # 0.29775390625,9.00419921875,41.9658203125,0.8353515625,0.38408203124999996,0.19072265625,2.0,"[100, 200, 300]",15,"['np.random.randint(18, high=80)', 'np.random.binomial(2, 0.5)']",H:/cpu_Networksim_test_multiprocess3/
                  evalParam='graph.socialise()' # after the graph is created and socialise once, if mutation or further socialise is needed
                  # the instruction should be passed as a string. The string will be evaluated for each of the networks.
                  # for example the follwoing will result in a mutation before socialising:
                  #     'G.mutateDNA(mutationIntensity=0.0001, mutatePreference=True, mutatePreferenceProbability=True) # wheather sDNA should be mutated
                  #     G.socialise()'


                  ##
                  )

