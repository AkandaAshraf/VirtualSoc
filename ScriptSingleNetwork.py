from Transfer import WriteToFile
from Networks import RandomSocialGraphAdvanced
import os
import sys
sys.setrecursionlimit(100000000)  # this is needed for a large network
# if keep history is true and   WriteToFile(G).easySaveEverything(folder)
# is needed. This is due to python's deep copy problems. One way to avoid this is to write to file
# after each of the evolution and setting keepHistory = False

if __name__ == '__main__':

    folder = 'D:/cpu_virtualsoc_single2/'  # just a folder name to write the networks

    os.makedirs(folder)    # create the folder

    G = RandomSocialGraphAdvanced(labelSplit=[10, 20, 30, 40], # 1st 10 with the same sDNA-1, 2nd 20 with the same sDNA-2 (each 10 with
                                  # same sDNA)

                                  connectionPercentageWithMatchedNodes=5, # the top fraction of the nodes to be connected, see paper
                                  connectionPercentageWithMatchedNodesWithRandomness=1, # this param is not implemented
                                  explorationProbability=0.3, # exploration probablity, see paper
                                  addTraidtionalFeatures=False, # weather to add traditional age, gender, location features
                                  additionalFeatureLen=1000, # feature len. If the addTraidtionalFeatures is true then 1003 features for each
                                  # nodes
                                  npDistFunc=['np.random.randint(3, high=500)','np.random.randint(3, high=500)'], # the distribution function
                                  # from where the features will be generated. Usually it is a numpy random number generator
                                  #function. However, the size parameter should not be filled while passing
                                  # the function as a string.
                                  #  If the number of features equals to the number of
                                  # passed distribution functions then each of them will be used with the corresponding
                                  # feature. Otherwise a features will be generated based on a randomly selected passed function.
                                  # A feature for all the nodes for a single network will be generated from a single function.

                                  popularityPreferenceIntensity=0.5, # preferential attachment parameter
                                  mutualPreferenceIntensity=[0.9, 0.3, 0.1], # the path length preference parameter
                                  genFeaturesFromSameDistforAllLabel=False, # Wheter or not to generate features from the same dist.
                                  # for all labels. Otherwise different labels will have a different dist. for the selected feature dist.
                                  #numpy function
                                  keepHistory=True, # whether or past history for each evaliation is kept.  If
                                  #   WriteToFile(G).easySaveEverything(folder) is used then this should be set to true.
                                  # However, for a large network the recursion limit needs to be set high for this to be used.
                                  # This is for Python's complicated deep copy procedure. A easy way to solve this is to
                                  #use the WriteToFile after each evolution of the network and settin this as param as False.
                                  useGPU=False, # whether GPU should be used. Only valid for the GPU version
                                  numberofProcesses=None, # The number of processed should be used. Set it to None
                                  # if that is not desired.
                                  createInGPUMem=False, # whether the features and sDNAs should be created
                                  #in GPU memory. This is faster as the transition from system memory to
                                  # video memory is not required if useGPU is set to True. Only
                                  # valid for the the GPU version
                                  socialiseOnCreation=True # if  a socialisation is performed right after instantiate the network.
                                  # if False, the socialise agolrithm can be called later using the socialise function.
                                  # see paper for more information.
                                  )
    G.socialise() # a socialise method to socialise the graph. The exp explorationProbability=None, connectionPercentageWithMatchedNodes=None
    # can also be reassigned here again. If not assigned then it will use the same value for these two parameters when
    # the network was first created.

    G.mutateDNA(mutationIntensity=0.0001, mutatePreference=True, mutatePreferenceProbability=True) # wheather sDNA should be mutated
    G.socialise()

    G.mutateDNA(mutationIntensity=0.01, mutatePreference=True, mutatePreferenceProbability=True)
    G.socialise()

    WriteToFile(G).easySaveEverything(folder) # save everything to a folder


