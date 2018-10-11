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

        def __init__(self, graph, p=0.5):

            self.p = p
            self.graph = graph
            # self.selfConncetions = selfConncetions

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

        def simpleRandomSocialiserSingleEdge(self, nodes,percentageOfConnectionNodes=20):
            # nodes1 = []
            # nodes2 = []
            # scores = []
            #
            nodeScoreDict = {}


            for node1 in nodes:
                    for node2 in nodes:

                            if 1.0 - self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
                                if node1 is not node2:
                                    # scores.append(node1.getScore(node2)+node2.getScore(node1))
                                    # nodes1.append(node1)
                                    # nodes2.append(node2)

                                    nodeScoreDict[node1,node2] = node1.getScore(node2)+node2.getScore(node1)

                                    # self.graph.adjMatDict[node1.ID, node2.ID] = 1
                                    # self.graph.adjMatDict[node2.ID, node1.ID] = 1
                                #
                                # else:
                                #     if not node1.selfConnected and self.graph.selfConncetions:
                                #         node1 + node1
            nodeScoreDictSorted = sorted(nodeScoreDict.items(), key=operator.itemgetter(1), reverse=True)

            l = 0.0
            stoppingLen = len(nodeScoreDictSorted)*percentageOfConnectionNodes/100
            for node1,node2 in nodeScoreDictSorted:
                if not self.graph.checkSameEntryAdj(node1, node2,
                                                    warning=False) and not self.graph.checkSameEntryAdj(node2,
                                                                                                        node1,
                                                                                                        warning=False):
                        if l>= stoppingLen:
                            break
                        else:
                            node1+node2
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
