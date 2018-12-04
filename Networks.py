from Node import *
from DNA import *
from Socialiser import *
import PetriDish
import collections
import numpy as np
from scipy.sparse import dok_matrix
from scipy.sparse import linalg
import warnings
import collections
import copy
import cupy as cp

class Graph:

    def __init__(self, undirected=True, selfConncetions=False):
        self.nodeCount = 0
        self.edgeCount = 0
        self.adjMatDict = collections.defaultdict(lambda: None)
        self.E = self.adjMatDict
        self.undirected = undirected
        self.selfConncetions=selfConncetions
        self.evolutionHistory = []
        self.N = []
        self.adj = None
        self.adjP2 = None
        self.adjP3 = None
        self.adjP4 = None


    def A(self, externalAdjDict = None, nodeCount=None):

        if externalAdjDict is None:
            adj = dok_matrix((self.nodeCount, self.nodeCount),dtype=np.int)
            for key1,key2 in self.adjMatDict:
                if self.adjMatDict[key1,key2] is not None:
                    adj[key1,key2] = 1
                    self.adj = adj
            return adj

        else:
            adj = dok_matrix((nodeCount, nodeCount),dtype=np.int)
            for key1,key2 in externalAdjDict:
                if externalAdjDict[key1, key2] is not None:
                    adj[key1,key2] = 1
            return adj

    def writeFileA(self,filePath):
        with open(filePath, 'w') as f:
            for key1, key2 in self.adjMatDict:
                if self.adjMatDict[key1, key2] is not None:
                    f.write('%s,%s\n' % (key1, key2))


    def adjPower(self,P,useGPU=False):
        if self.adj is None:
            self.A()
        i = 2
        if useGPU and cp.cuda.is_available():
            for p in P:
                cpAdj = cp.asarray(self.adj.toarray())
                if i == 2:
                    self.adjP2 = dok_matrix(np.asmatrix(cp.asnumpy(cp.matmul(cpAdj,cpAdj))))
                if i == 3:
                    self.adjP3 = dok_matrix(np.asmatrix(cp.asnumpy(cp.matmul(cp.asarray(self.adjP2.toarray()),cpAdj))))
                if i == 4:
                    self.adjP4 = dok_matrix(np.asmatrix(cp.asnumpy(cp.matmul(cp.asarray(self.adjP3.toarray()),cpAdj))))
                i += 1
        else:
            for p in P:
                 if i == 2:
                     self.adjP2 = self.adj.dot(self.adj)
                 if i == 3:
                     self.adjP3 = self.adjP2.dot(self.adj)
                 if i == 4:
                     self.adjP4 = self.adjP3.dot(self.adj)
                 i +=1








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

    #
    # class __EvolutionHistory():
    #     def __init__(self,adjMat,explorationProbability,connectionPercentageWithMatchedNodes,DNA,DNAmutationIntensity,mutatePreference,mutatePreferenceProbability,edgeCount):
    #         # deep copy all historical information
    #         self.adjMat = copy.deepcopy(adjMat)
    #         self.explorationProbability = copy.deepcopy(explorationProbability)
    #         self.connectionPercentageWithMatchedNodes = copy.deepcopy(connectionPercentageWithMatchedNodes)
    #         self.DNA = copy.deepcopy(DNA)
    #         self.DNAmutationIntensity = copy.deepcopy(DNAmutationIntensity)
    #         self.mutatePreference = copy.deepcopy(mutatePreference)
    #         self.mutatePreferenceProbability = copy.deepcopy(mutatePreferenceProbability)
    #         self.edgeCount = copy.deepcopy(edgeCount)


    def edge_list(self):
        pass


class RandomGraph(Graph):


    def __init__(self, n, p, type='gnp', undirected=True, selfConncetions=False, keepHistory=True,labelSplit=None,dna=None):
        super(RandomGraph, self).__init__(undirected, selfConncetions)
        self.type =type
        self.p = p

        # Dish = PetriDish()

        self.N = PetriDish.createSimpleNodes(numberOfNodes=n, nodeType=Node, DNA=DNA('random'), Graph=self)
        self.socialiseRandomGraph()

        # __SocialiserObj = randomSocial(graph=self, p=p)
        # __SocialiserObj.simpleRandomSocialiserSingleEdge(self.N)
        # Graph.nodeCount = len(self.N)
        self.keepHistory = keepHistory

        #
        # if self.keepHistory:
        #      self.evolutionHistory = []
        #


    def socialiseRandomGraph(self):
        __SocialiserObj = randomSocial(graph=self, p=self.p)
        __SocialiserObj.simpleRandomSocialiserSingleEdge()





    def A(self, externalAdjDict = None, nodeCount=None):
        return super().A()





class RandomSocialGraph(Graph):

    def __init__(self, labelSplit, explorationProbability=0.9, connectionPercentageWithMatchedNodes=20 , n='auto', dna='auto', p=None, undirected=True, selfConncetions=False, keepHistory = True):
        super(RandomSocialGraph, self).__init__(undirected=undirected, selfConncetions=selfConncetions)
        self.DNA = []
        self.dna =dna

        self.explorationProbability = explorationProbability
        self.percentageOfConnectionNodes = connectionPercentageWithMatchedNodes
        self.keepHistory = keepHistory
        self.labelSplit =labelSplit
        self.mutationIntensity = 0.5
        self.mutatePreference = False
        self.mutatePreferenceProbability= True
        self._birthDNA = True

        for i in range(0,len(self.labelSplit)):
            # we will gen using createSocialNodesThreeFeatures which has three features thus len =3
            self.DNA.append(DNA(self.dna, len=3))

            if i ==0:
                tempN = PetriDish.createSocialNodesThreeFeatures(numberOfNodes=self.labelSplit[i], nodeType=NodeSocial, DNA=self.DNA[-1],commonLabel=i, Graph=self)
                self.N = tempN
                self.DNA[-1]._assignedNodes(tempN)
            else:
                tempN = PetriDish.createSocialNodesThreeFeatures(numberOfNodes=self.labelSplit[i]-self.labelSplit[i-1], nodeType=NodeSocial,commonLabel=i, DNA=self.DNA[-1],
                                                   Graph=self)
                self.N = [*self.N, *tempN]
                self.DNA[-1]._assignedNodes(tempN)

        self.socialise()


        # if self.keepHistory:
        #   self.evolutionHistory.append(self.__EvolutionHistory(adjMat=self.adjMatDict, explorationProbability=explorationProbability, connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes, DNA=DNA,
        #                                                        mutationIntensity='birthDNA', mutatePreference='birthDNA', mutatePreferenceProbability='birthDNA', edgeCount=self.edgeCount))

    #
    #
    # def _socialiseRandomSocialGraph(self):
    #     __SocialiserObj = randomSocialwithDNA(graph=self, percentageOfConnectionNodes=self.percentageOfConnectionNodes, p=self.explorationProbability)
    #     __SocialiserObj.simpleRandomSocialiserSingleEdge()
    #
    def mutateDNA(self, mutationIntensity=None, mutatePreference=None, mutatePreferenceProbability=None):

        if mutationIntensity is not None:
            self.mutationIntensity =mutationIntensity

        if mutatePreference is not None:
            self.mutatePreference = mutatePreference

        if mutatePreferenceProbability is not None:
           self.mutatePreferenceProbability = mutatePreferenceProbability

        for dna in self.DNA:
            dna.mutateDNA(intensity=self.mutationIntensity, mutatePreference=self.mutatePreference,
                          mutatePreferenceProbability=self.mutatePreferenceProbability)

        # __SocialiserObj = randomSocialwithDNA(graph=self, percentageOfConnectionNodes=self.percentageOfConnectionNodes,
        #                                       p=self.explorationProbability)
        # __SocialiserObj.simpleRandomSocialiserSingleEdge()

        if self.keepHistory:
            self.evolutionHistory.append(
                self.__EvolutionHistory(adjMat=self.adjMatDict, explorationProbability=self.explorationProbability,
                                        connectionPercentageWithMatchedNodes='onlyMutated',
                                        DNA=DNA,
                                        mutationIntensity=self.mutationIntensity, mutatePreference=self.mutatePreference,
                                        mutatePreferenceProbability=self.mutatePreferenceProbability,
                                        edgeCount=self.edgeCount))

    def mutateDNAandSocialise(self, mutationIntensity=None, mutatePreference=None, mutatePreferenceProbability=None, explorationProbability=None, connectionPercentageWithMatchedNodes=None):

        if mutationIntensity is not None:
            self.mutationIntensity = mutationIntensity

        if mutatePreference is not None:
            self.mutatePreference = mutatePreference

        if mutatePreferenceProbability is not None:
            self.mutatePreferenceProbability = mutatePreferenceProbability

        if explorationProbability is not None:
            self.explorationProbability = explorationProbability

        if connectionPercentageWithMatchedNodes is not None:
            self.percentageOfConnectionNodes = connectionPercentageWithMatchedNodes



        for dna in self.DNA:
            dna.mutateDNA(intensity=self.mutationIntensity, mutatePreference=self.mutatePreference, mutatePreferenceProbability=self.mutatePreferenceProbability)

        __SocialiserObj = randomSocialwithDNA(graph=self, percentageOfConnectionNodes=self.percentageOfConnectionNodes, p=self.explorationProbability)
        __SocialiserObj.simpleRandomSocialiserSingleEdge()

        if self.keepHistory:
            self.evolutionHistory.append(
                self.__EvolutionHistory(adjMat=self.adjMatDict, explorationProbability=self.explorationProbability,
                                        connectionPercentageWithMatchedNodes=self.percentageOfConnectionNodes, DNA=DNA,
                                        mutationIntensity=self.mutationIntensity, mutatePreference=self.mutatePreference,
                                        mutatePreferenceProbability=self.mutatePreferenceProbability, edgeCount=self.edgeCount))

    def socialise(self, explorationProbability=None, connectionPercentageWithMatchedNodes=None):

        if explorationProbability is not None:
             self.explorationProbability = explorationProbability

        if connectionPercentageWithMatchedNodes is not None:
             self.percentageOfConnectionNodes = connectionPercentageWithMatchedNodes

        __SocialiserObj = randomSocialwithDNA(graph=self, percentageOfConnectionNodes=self.percentageOfConnectionNodes, p=self.explorationProbability)
        __SocialiserObj.simpleRandomSocialiserSingleEdge()

        if not self._birthDNA:
                self.evolutionHistory.append(
                    self.__EvolutionHistory(adjMat=self.adjMatDict, explorationProbability=self.explorationProbability,
                                            connectionPercentageWithMatchedNodes=self.percentageOfConnectionNodes,
                                            DNA=DNA,
                                            mutationIntensity='noMutationOccuredInThisStage',
                                            mutatePreference='noMutationOccuredInThisStage',
                                            mutatePreferenceProbability='noMutationOccuredInThisStage',
                                            edgeCount=self.edgeCount))

        else:
            self.evolutionHistory.append(
                self.__EvolutionHistory(adjMat=self.adjMatDict, explorationProbability=self.explorationProbability,
                                        connectionPercentageWithMatchedNodes=self.percentageOfConnectionNodes, DNA=DNA,
                                        mutationIntensity='birthDNA', mutatePreference='birthDNA',
                                        mutatePreferenceProbability='birthDNA', edgeCount=self.edgeCount))
        self._birthDNA = False


    class __EvolutionHistory():
        def __init__(self, adjMat, explorationProbability, connectionPercentageWithMatchedNodes, DNA, mutationIntensity, mutatePreference, mutatePreferenceProbability, edgeCount):
            # deep copy all historical information
            self.adjMat = copy.deepcopy(adjMat)
            self.explorationProbability = copy.deepcopy(explorationProbability)
            self.connectionPercentageWithMatchedNodes = copy.deepcopy(connectionPercentageWithMatchedNodes)
            self.DNA = copy.deepcopy(DNA)
            self.mutationIntensity = copy.deepcopy(mutationIntensity)
            self.mutatePreference = copy.deepcopy(mutatePreference)
            self.mutatePreferenceProbability = copy.deepcopy(mutatePreferenceProbability)
            self.edgeCount = copy.deepcopy(edgeCount)

    def __getNodes(self):
        pass

    def A(self, externalAdjDict = None, nodeCount=None):
        return super().A()




class RandomSocialGraphAdvanced(Graph):

    def __init__(self, labelSplit,popularityPreferenceIntensity=1,mutualPreferenceIntensity=None,connectionPercentageWithMatchedNodesWithRandomness=None,pathLenghtLimit=4, explorationProbability=0.9, connectionPercentageWithMatchedNodes=20 , n='auto', dna='auto', p=None, undirected=True, selfConncetions=False, keepHistory = True,addTraidtionalFeatures=True,npDistFunc=None,additionalFeatureLen=0,genFeaturesFromSameDistforAllLabel=True,socialiseOnCreation=True,shuffledDNA=True,useGPU=True,createInGPUMem=True,numberofProcesses=None):
        super(RandomSocialGraphAdvanced, self).__init__(undirected=undirected, selfConncetions=selfConncetions)
        self.DNA = []
        self.dna =dna

        self.explorationProbability = explorationProbability
        self.percentageOfConnectionNodes = connectionPercentageWithMatchedNodes
        self.keepHistory = keepHistory
        self.labelSplit =labelSplit
        self.mutationIntensity = 0.5
        self.mutatePreference = False
        self.mutatePreferenceProbability= True
        self._birthDNA = True
        self.numberofProcesses = numberofProcesses

        self.additionalFeatureLen= additionalFeatureLen
        self.addTraidtionalFeatures= addTraidtionalFeatures
        self.npDistFunc= npDistFunc
        self.popularityPreferenceIntensity = popularityPreferenceIntensity
        self.mutualPreferenceIntensity = mutualPreferenceIntensity
        self.pathLenghtLimit = pathLenghtLimit
        self.Socialised = False
        self.connectionPercentageWithMatchedNodesWithRandomness = connectionPercentageWithMatchedNodesWithRandomness
        self._useGPU = useGPU
        self.createInGPUMem = createInGPUMem



        if genFeaturesFromSameDistforAllLabel:
            for i in range(0,len(self.labelSplit)):
                # we will gen using createSocialNodesThreeFeatures which has three features thus len =3
                featureLen = 0
                if addTraidtionalFeatures:
                    featureLen = 3
                if additionalFeatureLen is not None:
                    featureLen = featureLen + additionalFeatureLen
                self.DNA.append(DNAadvanced(self.dna, len=featureLen,useGPU=self._useGPU,createInGPUMem=createInGPUMem))

                if i ==0:
                    tempN = PetriDish.createSocialNodesNFeatures(numberOfNodes=self.labelSplit[i], nodeType=NodeSocial, DNA=self.DNA[-1], commonLabel=i, Graph=self,additionalFeatureLen=self.additionalFeatureLen,npDistFunc=self.npDistFunc,addTraidtionalFeatures=self.addTraidtionalFeatures)
                    self.N = tempN
                    self.DNA[-1]._assignedNodes(tempN)
                else:
                    tempN = PetriDish.createSocialNodesNFeatures(numberOfNodes=self.labelSplit[i]-self.labelSplit[i-1], nodeType=NodeSocial, commonLabel=i, DNA=self.DNA[-1],
                                                                 Graph=self, additionalFeatureLen=self.additionalFeatureLen,npDistFunc=self.npDistFunc,addTraidtionalFeatures=self.addTraidtionalFeatures)
                    self.N = [*self.N, *tempN]
                    self.DNA[-1]._assignedNodes(tempN)

        else:
            if shuffledDNA:
                self.N = PetriDish.createSocialNodesNFeaturesSameDistWithDNAShuffled(numberOfNodes=self.labelSplit[-1], nodeType=NodeSocial, dna=self.dna, Graph=self, additionalFeatureLen=self.additionalFeatureLen,
                                               addTraidtionalFeatures=self.addTraidtionalFeatures, npDistFunc=self.npDistFunc, labelSplit=self.labelSplit,DnaObjType=DNAadvanced)
            else:
                self.N=PetriDish.createSocialNodesNFeaturesSameDist(numberOfNodes=self.labelSplit[-1], nodeType=NodeSocial, dna=self.dna, Graph=self, additionalFeatureLen=self.additionalFeatureLen,
                                               addTraidtionalFeatures=self.addTraidtionalFeatures, npDistFunc=self.npDistFunc, labelSplit=self.labelSplit,DnaObjType=DNAadvanced)
        if socialiseOnCreation:
            self.socialise()

        # if self.keepHistory:
        #   self.evolutionHistory.append(self.__EvolutionHistory(adjMat=self.adjMatDict, explorationProbability=explorationProbability, connectionPercentageWithMatchedNodes=connectionPercentageWithMatchedNodes, DNA=DNA,
        #                                                        mutationIntensity='birthDNA', mutatePreference='birthDNA', mutatePreferenceProbability='birthDNA', edgeCount=self.edgeCount))

    #
    #
    # def _socialiseRandomSocialGraph(self):
    #     __SocialiserObj = randomSocialwithDNA(graph=self, percentageOfConnectionNodes=self.percentageOfConnectionNodes, p=self.explorationProbability)
    #     __SocialiserObj.simpleRandomSocialiserSingleEdge()
    #
    def mutateDNA(self, mutationIntensity=None, mutatePreference=None, mutatePreferenceProbability=None):

        if mutationIntensity is not None:
            self.mutationIntensity =mutationIntensity

        if mutatePreference is not None:
            self.mutatePreference = mutatePreference

        if mutatePreferenceProbability is not None:
           self.mutatePreferenceProbability = mutatePreferenceProbability

        for dna in self.DNA:
            dna.mutateDNA(intensity=self.mutationIntensity, mutatePreference=self.mutatePreference,
                          mutatePreferenceProbability=self.mutatePreferenceProbability)

        # __SocialiserObj = randomSocialwithDNA(graph=self, percentageOfConnectionNodes=self.percentageOfConnectionNodes,
        #                                       p=self.explorationProbability)
        # __SocialiserObj.simpleRandomSocialiserSingleEdge()

        if self.keepHistory:
            self.evolutionHistory.append(
                self.__EvolutionHistory(adjMat=self.adjMatDict, explorationProbability=self.explorationProbability,
                                        connectionPercentageWithMatchedNodes='onlyMutated',
                                        DNA=DNA,
                                        mutationIntensity=self.mutationIntensity, mutatePreference=self.mutatePreference,
                                        mutatePreferenceProbability=self.mutatePreferenceProbability,
                                        edgeCount=self.edgeCount, Graph=self))

    def mutateDNAandSocialise(self, mutationIntensity=None, mutatePreference=None, mutatePreferenceProbability=None, explorationProbability=None, connectionPercentageWithMatchedNodes=None):

        if mutationIntensity is not None:
            self.mutationIntensity = mutationIntensity

        if mutatePreference is not None:
            self.mutatePreference = mutatePreference

        if mutatePreferenceProbability is not None:
            self.mutatePreferenceProbability = mutatePreferenceProbability

        if explorationProbability is not None:
            self.explorationProbability = explorationProbability

        if connectionPercentageWithMatchedNodes is not None:
            self.percentageOfConnectionNodes = connectionPercentageWithMatchedNodes



        for dna in self.DNA:
            dna.mutateDNA(intensity=self.mutationIntensity, mutatePreference=self.mutatePreference, mutatePreferenceProbability=self.mutatePreferenceProbability)

        __SocialiserObj = randomSocialwithDNAadvanced(graph=self, percentageOfConnectionNodes=self.percentageOfConnectionNodes, p=self.explorationProbability,mutualPreferenceIntensity=self.mutualPreferenceIntensity,popularityPreferenceIntensity=self.popularityPreferenceIntensity,pathLenghtLimit=self.pathLenghtLimit)
        if self.numberofProcesses is not None:
            __SocialiserObj.simpleRandomSocialiserSingleEdgeMultiProcessed(self.numberofProcesses,resocialising=True)
        else:
            __SocialiserObj.simpleRandomSocialiserSingleEdge()

        if self.keepHistory:
            self.evolutionHistory.append(
                self.__EvolutionHistory(adjMat=self.adjMatDict, explorationProbability=self.explorationProbability,
                                        connectionPercentageWithMatchedNodes=self.percentageOfConnectionNodes, DNA=DNA,
                                        mutationIntensity=self.mutationIntensity, mutatePreference=self.mutatePreference,
                                        mutatePreferenceProbability=self.mutatePreferenceProbability, edgeCount=self.edgeCount, Graph=self))
        self.Socialised = True

    def socialise(self, explorationProbability=None, connectionPercentageWithMatchedNodes=None):

        if explorationProbability is not None:
             self.explorationProbability = explorationProbability

        if connectionPercentageWithMatchedNodes is not None:
             self.percentageOfConnectionNodes = connectionPercentageWithMatchedNodes

        __SocialiserObj = randomSocialwithDNAadvanced(graph=self, percentageOfConnectionNodes=self.percentageOfConnectionNodes, p=self.explorationProbability,mutualPreferenceIntensity=self.mutualPreferenceIntensity,popularityPreferenceIntensity=self.popularityPreferenceIntensity,pathLenghtLimit=self.pathLenghtLimit)
        if self.numberofProcesses is not None:
            __SocialiserObj.simpleRandomSocialiserSingleEdgeMultiProcessed(self.numberofProcesses)
        else:
            __SocialiserObj.simpleRandomSocialiserSingleEdge()

        if self.keepHistory:
            if not self._birthDNA:
                    self.evolutionHistory.append(
                        self.__EvolutionHistory(adjMat=self.adjMatDict, explorationProbability=self.explorationProbability,
                                                connectionPercentageWithMatchedNodes=self.percentageOfConnectionNodes,
                                                DNA=DNA,
                                                mutationIntensity='noMutationOccuredInThisStage',
                                                mutatePreference='noMutationOccuredInThisStage',
                                                mutatePreferenceProbability='noMutationOccuredInThisStage',
                                                edgeCount=self.edgeCount, Graph=self))

            else:
                self.evolutionHistory.append(
                    self.__EvolutionHistory(adjMat=self.adjMatDict, explorationProbability=self.explorationProbability,
                                            connectionPercentageWithMatchedNodes=self.percentageOfConnectionNodes, DNA=DNA,
                                            mutationIntensity='birthDNA', mutatePreference='birthDNA',
                                            mutatePreferenceProbability='birthDNA', edgeCount=self.edgeCount, Graph=self))
            self._birthDNA = False
        self.Socialised = True



    class __EvolutionHistory():
        def __init__(self, adjMat, explorationProbability, connectionPercentageWithMatchedNodes, DNA, mutationIntensity, mutatePreference, mutatePreferenceProbability, edgeCount,Graph):
            # deep copy all historical information
            self.adjMat = copy.deepcopy(adjMat)
            self.explorationProbability = copy.deepcopy(explorationProbability)
            self.connectionPercentageWithMatchedNodes = copy.deepcopy(connectionPercentageWithMatchedNodes)
            self.DNA = copy.deepcopy(DNA)
            self.mutationIntensity = copy.deepcopy(mutationIntensity)
            self.mutatePreference = copy.deepcopy(mutatePreference)
            self.mutatePreferenceProbability = copy.deepcopy(mutatePreferenceProbability)
            self.edgeCount = copy.deepcopy(edgeCount)
            self.Graph = copy.deepcopy(Graph)

    def __getNodes(self):
        pass

    def A(self, externalAdjDict = None, nodeCount=None):
        return super().A()



