import numpy as np
import concurrent.futures
import operator
# from cupy.cuda import MemoryPool
import pyprind
import sys
import itertools
from pathos.multiprocessing import ProcessingPool as Pool
from pathos.multiprocessing import ProcessingPool as ParallelPool
from sys import platform
import multiprocess.context as ctx

if platform == "linux" or platform == "linux2":
    ctx._force_start_method('spawn')

import collections
class randomSocial:
    '''

    '''


    def __init__(self,graph, p):

        self.p = p
        self.graph = graph

    def simpleRandomSocialiserMultipleEdgesSelfConnectedDirected(self, nodes):

        for node1 in nodes:
            if node1.DNA.value == 'random':
                for node2 in nodes:
                    if 1.0-self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
                        if node1 is not node2:
                            node1+node2
                        else:
                            if not node1.selfConnected and self.graph.selfConncetions:
                                 node1+node1

    def simpleRandomSocialiserSingleEdgeSelfConnectedDirected(self, nodes):

        for node1 in nodes:
            if node1.DNA.value == 'random':
                for node2 in nodes:
                    if not self.graph.checkSameEntryAdj(node1, node2,warning=False):
                        if 1.0 - self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
                                node1 + node2


    def simpleRandomSocialiserSingleEdge(self):
        nodes = self.graph.N
        for node1 in nodes:
            if node1.DNA.value == 'random':
                for node2 in nodes:
                    if not self.graph.checkSameEntryAdj(node1, node2, warning=False) or not self.graph.checkSameEntryAdj(node2, node1, warning=False):
                        if 1.0 - self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
                            if node1 is not node2:
                                node1 + node2


    def simpleRandomSocialiserThreaded(self, nodes):

          raise Exception('not implemented!')

class randomSocialwithDNA(randomSocial):

        def __init__(self, graph,percentageOfConnectionNodes, p=0.5):
            super(randomSocialwithDNA, self).__init__(graph, p)

            self.popularityPreferenceIntensity = None
            self.mutualPreferenceIntensity = None
            self.pathLenghtLimit = None

            # self.p = p
            # self.graph = graph
            self.percentageOfConnectionNodes = percentageOfConnectionNodes
            # self.selfConncetions = selfConncetions
        class _NodesScore:
            def __init__(self,node1,node2, score, graph):
                self.node1 = node1
                self.node2 = node2
                self.score = score
                self.graph = graph

            def addNodes(self):
                if not self.graph.checkSameEntryAdj(self.node1, self.node2,
                                                    warning=False) or not self.graph.checkSameEntryAdj(self.node2,
                                                                                                        self.node1,
                                                                                                        warning=False):
                       self.node1 + self.node2


        def simpleRandomSocialiserSingleEdge(self):

            NodesScoreListOfObjects = []
            nodes = self.graph.N

            for node1 in nodes:
                    for node2 in nodes:

                            if 1.0 - self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
                                if node1 is not node2:

                                    NodesScoreListOfObjects.append(self._NodesScore(node1=node1, node2=node2, score=node1.getScore(node2) + node2.getScore(node1), graph=self.graph))

            NodesScoreListOfObjectsSorted = sorted(NodesScoreListOfObjects, key=lambda x: x.score, reverse=True)



            l = 0.0
            stoppingLen = len(NodesScoreListOfObjectsSorted)*self.percentageOfConnectionNodes/100
            for  NodesScoreObj in NodesScoreListOfObjectsSorted:

                        if l>= stoppingLen:
                            break
                        else:
                            NodesScoreObj.addNodes()
                        l +=1



class randomSocialwithDNAadvanced(randomSocialwithDNA):


    def __init__(self,popularityPreferenceIntensity,mutualPreferenceIntensity,pathLenghtLimit,graph,percentageOfConnectionNodes,p,connectionPercentageWithMatchedNodesWithRandomness=None, **kwargs):
        super(randomSocialwithDNAadvanced, self).__init__(graph=graph,percentageOfConnectionNodes=percentageOfConnectionNodes, p=p)
        self.popularityPreferenceIntensity = popularityPreferenceIntensity
        self.mutualPreferenceIntensity = mutualPreferenceIntensity
        self.pathLenghtLimit = pathLenghtLimit
        self._bar = None





    def simpleRandomSocialiserSingleEdge(self):
        print('socialising')
        NodesScoreListOfObjects = []
        nodes = self.graph.N
        print('Calculating node scores!')
        bar = pyprind.ProgBar(len(nodes)*len(nodes), stream=sys.stdout)


        for node1 in nodes:
            for node2 in nodes:

                if 1.0 - self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
                    if node1 is not node2:
                        NodesScoreListOfObjects.append(self._NodesScore(node1=node1, node2=node2,
                                                                         score=node1.getScoreAdvanced(node2,popularityPreferenceIntensity=self.popularityPreferenceIntensity,mutualPreferenceIntensity=self.mutualPreferenceIntensity) + node2.getScoreAdvanced(
                                                                             node1,popularityPreferenceIntensity=self.popularityPreferenceIntensity,mutualPreferenceIntensity=self.mutualPreferenceIntensity), graph=self.graph))
                        bar.update()
        # NodesScoreListOfObjectsSorted = sorted(NodesScoreListOfObjects, key=lambda x: x.score, reverse=True)
        NodesScoreListOfObjectsSorted = sorted(NodesScoreListOfObjects, key=lambda x: x.score, reverse=True)
        l = 0.0

        stoppingLen = len(NodesScoreListOfObjectsSorted) * self.percentageOfConnectionNodes / 100

        bar = pyprind.ProgBar(stoppingLen, stream=sys.stdout)


        for NodesScoreObj in NodesScoreListOfObjectsSorted:

            if l >= stoppingLen:
                break
            else:
                NodesScoreObj.addNodes()
            bar.update()
            l += 1
        # bar.finish()

        if self.mutualPreferenceIntensity is not None:
                self.graph.adjPower(self.mutualPreferenceIntensity,self.graph._useGPU)

    # def _getScoresSingleProcess(self,nodes):
    #
    #     node1 = nodes[0]
    #     node2 = nodes[1]
    #     self._bar.update()
    #     return self._NodesScore2(node1=node1, node2=node2,
    #                              score=node1.getScoreAdvanced(node2,popularityPreferenceIntensity=self.popularityPreferenceIntensity,
    #                                                          mutualPreferenceIntensity=self.mutualPreferenceIntensity) +
    #                                                          node2.getScoreAdvanced(node1, popularityPreferenceIntensity=self.popularityPreferenceIntensity,
    #                                                          mutualPreferenceIntensity=self.mutualPreferenceIntensity))

   # def checkifEdgeAlreadyExists():
   #     if not graph.checkSameEntryAdj(self.node1, self.node2,
   #                                    warning=False) or not graph.checkSameEntryAdj(self.node2,
   #                                                                                  self.node1,
   #                                                                                  warning=False):
   #         pass

    class NodesScore2:
        def __init__(self, node1, node2, popularityPreferenceIntensity, mutualPreferenceIntensity):
            self.node1 = node1
            self.node2 = node2
            self.node1ID = node1.ID
            self.node2ID = node2.ID

            self.popularityPreferenceIntensity = popularityPreferenceIntensity
            self.mutualPreferenceIntensity = mutualPreferenceIntensity
            self.score = node1.getScoreAdvanced(self.node2,
                                                popularityPreferenceIntensity=self.popularityPreferenceIntensity,
                                                mutualPreferenceIntensity=self.mutualPreferenceIntensity) + self.node2.getScoreAdvanced(
                node1,
                popularityPreferenceIntensity=self.popularityPreferenceIntensity,
                mutualPreferenceIntensity=self.mutualPreferenceIntensity)

        def addNodes(self,graph):
            if not graph.checkSameEntryAdj(self.node1, self.node2,
                                                warning=False) or not graph.checkSameEntryAdj(self.node2,
                                                                                                   self.node1,
                                                                                                   warning=False):
                   self.node1 + self.node2

    def getScoresSingleProcess(self, nodes):
        node1 = nodes[0]
        node2 = nodes[1]
        self._bar.update()
        return self.NodesScore2(node1=node1, node2=node2, popularityPreferenceIntensity=self.popularityPreferenceIntensity,
                            mutualPreferenceIntensity=self.mutualPreferenceIntensity)

    def simpleRandomSocialiserSingleEdgeMultiProcessed(self,numberofProcesses, resocialising=False):
        print('socialising')
        NodesScoreListOfObjects = []
        nodes = self.graph.N


        nodesCombination = list(set(itertools.combinations(nodes, 2)))
        # tempSameEntryCheck =collections.defaultdict(lambda: None)
        indicesToBeDeltedtemp = []
        if resocialising:
            l = 0
            for nodes in nodesCombination:
                # tempSameEntryCheck[nodes[0].ID,nodes[1].ID] =1
                if  self.graph.checkSameEntryAdj(nodes[0], nodes[1],
                                               warning=False) or  self.graph.checkSameEntryAdj(nodes[1],
                                                                                             nodes[0],
                                                                                             warning=False) or nodes[0].ID==nodes[1].ID:
                     # del nodesCombination[l]
                     indicesToBeDeltedtemp.append(l)

                l +=1

        nodesCombination = [x for i, x in enumerate(nodesCombination) if i not in indicesToBeDeltedtemp]
        np.random.shuffle(nodesCombination)
        np.random.shuffle(nodesCombination)
        np.random.shuffle(nodesCombination)
        np.random.shuffle(nodesCombination)
        nodesCombination = nodesCombination[0:int(np.floor(len(nodesCombination) * self.p))]

        nodesCombinationDict =collections.defaultdict(lambda: None)
        for nodes in nodesCombination:
            if nodes[0] is not None:
                nodesCombinationDict[nodes[0].ID,nodes[1].ID] = [nodes[0],nodes[1]]



        self._bar = pyprind.ProgBar(len(nodesCombination), stream=sys.stdout)
        if numberofProcesses is not None:
            pool = Pool(numberofProcesses)
            print('Calculating node scores!')
            # cp.cuda.MemoryPool(allocator=_malloc)

            NodesScoreListOfObjects = pool.imap(self.getScoresSingleProcess, nodesCombination)
        else:
            NodesScoreListOfObjects = []
            for nodes in nodesCombination:
                NodesScoreListOfObjects.append(self.getScoresSingleProcess(nodes))
        # print("Number of cpu : ", multiprocessing.cpu_count())

        # for node1 in nodes:
        #     for node2 in nodes:
        #
        #         if 1.0 - self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
        #             if node1 is not node2:
        #                 NodesScoreListOfObjects.append(self._NodesScore(node1=node1, node2=node2,
        #                                                                  score=node1.getScoreAdvanced(node2,popularityPreferenceIntensity=self.popularityPreferenceIntensity,mutualPreferenceIntensity=self.mutualPreferenceIntensity) + node2.getScoreAdvanced(
        #                                                                      node1,popularityPreferenceIntensity=self.popularityPreferenceIntensity,mutualPreferenceIntensity=self.mutualPreferenceIntensity), graph=self.graph))
        # # NodesScoreListOfObjectsSorted = sorted(NodesScoreListOfObjects, key=lambda x: x.score, reverse=True)
        NodesScoreListOfObjectsSorted = sorted(NodesScoreListOfObjects, key=lambda x: x.score, reverse=True)
        l = 0.0

        stoppingLen = len(NodesScoreListOfObjectsSorted) * self.percentageOfConnectionNodes / 100

        bar = pyprind.ProgBar(stoppingLen, stream=sys.stdout)


        for NodesScoreObj in NodesScoreListOfObjectsSorted:

            if l >= stoppingLen:
                break
            else:
                tempNodes = nodesCombinationDict[NodesScoreObj.node1ID, NodesScoreObj.node2ID]
                tempNodes[0]+tempNodes[1]
            bar.update()
            l += 1
        # bar.finish()

        if self.mutualPreferenceIntensity is not None:
                self.graph.adjPower(self.mutualPreferenceIntensity,self.graph._useGPU)







