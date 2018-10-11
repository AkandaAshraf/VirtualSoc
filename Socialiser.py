import numpy as np
import concurrent.futures


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
