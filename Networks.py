from Node import *
from DNA import *
from Socialiser import *
import PetriDish
import collections
import numpy as np
from scipy.sparse import dok_matrix
import warnings
import collections
import copy


class Graph:

    def __init__(self, undirected=True, selfConncetions=False):
        self.nodeCount = 0
        self.edgeCount = 0
        self.adjMatDict = collections.defaultdict(lambda: None)
        self.E = self.adjMatDict
        self.undirected = undirected
        self.selfConncetions=selfConncetions

    def A(self, externalAdjDict = None, nodeCount=None):

        if externalAdjDict is None:
            adj = dok_matrix((self.nodeCount, self.nodeCount),dtype=np.int)
            for key1,key2 in self.adjMatDict:
                if self.adjMatDict[key1,key2] is not None:
                    adj[key1,key2] = 1
            return adj

        else:
            adj = dok_matrix((nodeCount, nodeCount),dtype=np.int)
            for key1,key2 in externalAdjDict:
                if externalAdjDict[key1, key2] is not None:
                    adj[key1,key2] = 1
            return adj

        # elif not undirected and dense:
        #     adj = dok_matrix((self.nodeCount, self.nodeCount), dtype=np.int)
        #     for key1, key2 in self.adjMatDict:
        #         if self.adjMatDict[key1,key2] is not None:
        #             adj[key1,key2] = 1
        #     return adj.todense()
        # elif undirected and not dense:
        #     adj = dok_matrix((self.nodeCount, self.nodeCount), dtype=np.int)
        #     for key1, key2 in self.adjMatDict:
        #         if self.adjMatDict[key1, key2] is not None:
        #             adj[key1, key2] = 1
        #     return  adj + adj.T.multiply(adj.T > adj) - adj.multiply(adj.T > adj)
        #
        # elif undirected and dense:
        #     adj = dok_matrix((self.nodeCount, self.nodeCount), dtype=np.int)
        #     for key1, key2 in self.adjMatDict:
        #         if self.adjMatDict[key1, key2] is not None:
        #             adj[key1, key2] = 1
        #     return  (adj + adj.T.multiply(adj.T > adj) - adj.multiply(adj.T > adj)).todense()



    def checkSameEntryAdj(self, node1, node2,warning = True):
        if self.adjMatDict[node1.ID, node2.ID] == 1 or self.adjMatDict[node1.ID, node2.ID] is not None:
            if warning:
                warnings.warn(
                    "multiple edge connection detected and ignored!",

                )
            return True
        else:
            return False

    def checkSelfConnection(self,node1, node2,warning=True):
        if node1 is node2:
            if warning:
                warnings.warn(
                    "self connection detected!",

                )
            return True
        else:
            return False


    def edge_list(self):
        pass


class RandomGraph(Graph):


    def __init__(self, n, p, type='gnp', undirected=True, selfConncetions=False):
        super(RandomGraph, self).__init__(undirected, selfConncetions)
        self.type =type
        self.p = p
        # Dish = PetriDish()
        self.N = PetriDish.createSimpleNodes(numberOfNodes=n, nodeType=Node, DNA=DNA('random'), Graph=self)
        __SocialiserObj = randomSocial(graph=self, p=p)
        __SocialiserObj.simpleRandomSocialiserSingleEdge(self.N)
        self.Ncount = len(self.N)

    def A(self, externalAdjDict = None, nodeCount=None):
        return super().A()


class RandomSocialGraph(Graph):

    def __init__(self, labelSplit, explorationProbability=0.9, connectionPercentageWithMatchedNodes=20 , n='auto', dna='auto', p=None, undirected=True, selfConncetions=False, keepHistory = True):
        super(RandomSocialGraph, self).__init__(undirected, selfConncetions)
        self.DNA = []
        self.p = explorationProbability
        self.percentageOfConnectionNodes = connectionPercentageWithMatchedNodes
        self.N = []
        self.keepHistory = keepHistory

        if self.keepHistory:
             self.evolutionHistory = []



        for i in range(0,len(labelSplit)):
            # we will gen using createSocialNodesThreeFeatures which has three features thus len =3
            self.DNA.append(DNA(dna, len=3))

            if i ==0:
                tempN = PetriDish.createSocialNodesThreeFeatures(numberOfNodes=labelSplit[i], nodeType=NodeSocial, DNA=self.DNA[-1],commonLabel=i, Graph=self)
                self.N = tempN
                self.DNA[-1]._assignedNodes(tempN)
            else:
                tempN = PetriDish.createSocialNodesThreeFeatures(numberOfNodes=labelSplit[i]-labelSplit[i-1], nodeType=NodeSocial,commonLabel=i, DNA=self.DNA[-1],
                                               Graph=self)
                self.N = [*self.N, *tempN]
                self.DNA[-1]._assignedNodes(tempN)

        self.Ncount = len(self.N)

        __SocialiserObj = randomSocialwithDNA(graph=self, percentageOfConnectionNodes=self.percentageOfConnectionNodes, p=self.p)
        __SocialiserObj.simpleRandomSocialiserSingleEdge(self.N)

        if self.keepHistory:
          self.evolutionHistory.append(self.__EvolutionHistory(adjMat=self.adjMatDict,explorationProbability=explorationProbability,connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes,DNA=DNA,DNAmutationIntensity='birthDNA',mutatePreference='birthDNA',mutatePreferenceProbability='birthDNA',edgeCount=self.edgeCount))


    def mutateDNAandSocialiseAgain(self,intensity,mutatePreference=False, mutatePreferenceProbability=True, explorationProbability=0.9, connectionPercentageWithMatchedNodes=20):

        for dna in self.DNA:
            dna.mutateDNA(intensity=intensity,mutatePreference=mutatePreference, mutatePreferenceProbability=mutatePreferenceProbability)

        __SocialiserObj = randomSocialwithDNA(graph=self, percentageOfConnectionNodes=self.percentageOfConnectionNodes, p=self.p)
        __SocialiserObj.simpleRandomSocialiserSingleEdge(self.N)

        if self.keepHistory:
            self.evolutionHistory.append(
                self.__EvolutionHistory(adjMat=self.adjMatDict, explorationProbability=explorationProbability,
                                      connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes, DNA=DNA,
                                      DNAmutationIntensity=intensity, mutatePreference=mutatePreference,
                                      mutatePreferenceProbability=mutatePreferenceProbability, edgeCount=self.edgeCount))
    def socialiseAgain(self, explorationProbability=0.9, connectionPercentageWithMatchedNodes=20):
        self.p = explorationProbability
        self.percentageOfConnectionNodes = connectionPercentageWithMatchedNodes

        __SocialiserObj = randomSocialwithDNA(graph=self, percentageOfConnectionNodes=self.percentageOfConnectionNodes, p=self.p)
        __SocialiserObj.simpleRandomSocialiserSingleEdge(self.N)

    class __EvolutionHistory():
        def __init__(self,adjMat,explorationProbability,connectionPercentageWithMatchedNodes,DNA,DNAmutationIntensity,mutatePreference,mutatePreferenceProbability,edgeCount):
            # deep copy all historical information
            self.adjMat = copy.deepcopy(adjMat)
            self.explorationProbability = copy.deepcopy(explorationProbability)
            self.connectionPercentageWithMatchedNodes = copy.deepcopy(connectionPercentageWithMatchedNodes)
            self.DNA = copy.deepcopy(DNA)
            self.DNAmutationIntensity = copy.deepcopy(DNAmutationIntensity)
            self.mutatePreference = copy.deepcopy(mutatePreference)
            self.mutatePreferenceProbability = copy.deepcopy(mutatePreferenceProbability)
            self.edgeCount = copy.deepcopy(edgeCount)

    def __getNodes(self):
        pass

    def A(self, externalAdjDict = None, nodeCount=None):
        return super().A()






