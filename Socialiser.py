import numpy as np
import concurrent.futures
import operator

class randomSocial:


    def __init__(self,graph, p=0.5):

        self.p = p
        self.graph = graph
        # self.selfConncetions = selfConncetions

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
                            if node1 is not node2:
                                node1 + node2
                                # self.graph.adjMatDict[node1.ID, node2.ID] = 1

                            else:
                                if not node1.selfConnected and self.graph.selfConncetions:
                                    node1 + node1




    def simpleRandomSocialiserSingleEdge(self, nodes):

        for node1 in nodes:
            if node1.DNA.value == 'random':
                for node2 in nodes:
                    if not self.graph.checkSameEntryAdj(node1, node2, warning=False) and not self.graph.checkSameEntryAdj(node2, node1, warning=False):
                        if 1.0 - self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
                            if node1 is not node2:
                                node1 + node2
                                # self.graph.adjMatDict[node1.ID, node2.ID] = 1
                                # self.graph.adjMatDict[node2.ID, node1.ID] = 1

                            else:
                                if not node1.selfConnected and self.graph.selfConncetions:
                                    node1 + node1


    def simpleRandomSocialiserThreaded(self, nodes):

          raise Exception('not implemented!')

class randomSocialwithDNA:

        def __init__(self, graph,percentageOfConnectionNodes=20, p=0.5):

            self.p = p
            self.graph = graph
            self.percentageOfConnectionNodes = percentageOfConnectionNodes
            # self.selfConncetions = selfConncetions
        class NodesScore:
            def __init__(self,node1,node2, score, graph):
                self.node1 = node1
                self.node2 = node2
                self.score = score
                self.graph = graph

            def addNodes(self):
                if not self.graph.checkSameEntryAdj(self.node1, self.node2,
                                                    warning=False) and not self.graph.checkSameEntryAdj(self.node2,
                                                                                                        self.node1,
                                                                                                        warning=False):
                       self.node1 + self.node2

        # def simpleRandomSocialiserMultipleEdgesSelfConnectedDirected(self, nodes):
        #
        #     for node1 in nodes:
        #         if node1.DNA.value == 'random':
        #             for node2 in nodes:
        #                 if 1.0 - self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
        #                     if node1 is not node2:
        #                         node1 + node2
        #                     else:
        #                         if not node1.selfConnected and self.graph.selfConncetions:
        #                             node1 + node1
        #
        # def simpleRandomSocialiserSingleEdgeSelfConnectedDirected(self, nodes):
        #
        #     for node1 in nodes:
        #         if node1.DNA.value == 'random':
        #             for node2 in nodes:
        #                 if not self.graph.checkSameEntryAdj(node1, node2, warning=False):
        #                     if 1.0 - self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
        #                         if node1 is not node2:
        #                             node1 + node2
        #                             # self.graph.adjMatDict[node1.ID, node2.ID] = 1
        #
        #                         else:
        #                             if not node1.selfConnected and self.graph.selfConncetions:
        #                                 node1 + node1

        def simpleRandomSocialiserSingleEdge(self, nodes):
            # nodes1 = []
            # nodes2 = []
            # scores = []
            # #
            # nodeScoreDict = {}
            NodesScoreListOfObjects = []


            for node1 in nodes:
                    for node2 in nodes:

                            if 1.0 - self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
                                if node1 is not node2:
                                    # scores.append(node1.getScore(node2)+node2.getScore(node1))
                                    # nodes1.append(node1)
                                    # nodes2.append(node2)

                                    NodesScoreListOfObjects.append(self.NodesScore(node1=node1,node2=node2,score=node1.getScore(node2)+node2.getScore(node1),graph=self.graph))
                                    #
                                    # nodeScoreDict[node1,node2] = node1.getScore(node2)+node2.getScore(node1)
                                    #
                                    # nodeScore.append(node1.getScore(node2) + node2.getScore(node1), node1, node2)
                                    # # nodeScore.append(node1)
                                    # nodeScore.append(node2)

                                    # self.graph.adjMatDict[node1.ID, node2.ID] = 1
                                    # self.graph.adjMatDict[node2.ID, node1.ID] = 1
                                #
                                # else:
                                #     if not node1.selfConnected and self.graph.selfConncetions:
                                #         node1 + node1

            NodesScoreListOfObjectsSorted = sorted(NodesScoreListOfObjects, key=lambda x: x.score, reverse=True)

            l = 0.0
            stoppingLen = len(NodesScoreListOfObjectsSorted)*self.percentageOfConnectionNodes/100
            for  NodesScoreObj in NodesScoreListOfObjectsSorted:

                        if l>= stoppingLen:
                            break
                        else:
                            NodesScoreObj.addNodes()
                        l +=1



        def simpleRandomSocialiserThreaded(self, nodes):

            raise Exception('not implemented!')

    #         self.nodes =nodes
    #         executor = concurrent.futures.ProcessPoolExecutor(10)
    #         futures = [executor.submit(self.simpleRandomSocilaiserConnectMultiThreaded, node1=node,nodes=nodes, p=self.p,selfConnections=self.selfConncetions) for node in nodes]
    #         concurrent.futures.wait(futures)
    #
# def simpleRandomSocilaiserConnectMultiThreaded(node1):
#             if node1.DNA.value == 'random':
#                 for node2 in self.nodes:
#                     if 1.0 - self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
#                         if node1 is not node2:
#                             node1 + node2
#                             node2 + node1
#                         else:
#                             if not node1.selfConnected and self.selfConncetions:
#                                 node1 + node1
#
#
#
