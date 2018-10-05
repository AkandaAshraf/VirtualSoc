import numpy as np
import concurrent.futures


class randomSocial:


    def __init__(self, p=0.5, selfConncetions=True):

        self.p = p
        self.selfConncetions = selfConncetions

    def simpleRandomSocialiser(self, nodes):

        for node1 in nodes:
            if node1.DNA.value=='random':
                for node2 in nodes:
                    if 1.0-self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
                        if node1 is not node2:
                            node1+node2
                            node2+node1
                        else:
                            if not node1.selfConnected and self.selfConncetions:
                                 node1+node1

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
