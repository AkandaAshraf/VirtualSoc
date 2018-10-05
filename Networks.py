from Node import *
from DNA import *
from Socialiser import *
from PetriDish import *
import collections
import numpy as np
from scipy.sparse import dok_matrix
import warnings
import collections




class Graph:

    def __init__(self):
        self.nodeCount = 0
        self.edgeCount = 0
        self.adjMatDict = collections.defaultdict(lambda: None)
        self.E = self.adjMatDict

    def A(self,undirected=False, dense=False):
        if not undirected and not dense:
            adj = dok_matrix((self.nodeCount, self.nodeCount),dtype=np.int)
            for key1,key2 in self.adjMatDict:
                adj[key1,key2] = 1
            return adj
        elif not undirected and dense:
            adj = dok_matrix((self.nodeCount, self.nodeCount), dtype=np.int)
            for key1, key2 in self.adjMatDict:
                adj[key1, key2] = 1
            return adj.todense()
        elif undirected and not dense:
            adj = dok_matrix((self.nodeCount, self.nodeCount), dtype=np.int)
            for key1, key2 in self.adjMatDict:
                    adj[key1, key2] = 1
            return  adj + adj.T.multiply(adj.T > adj) - adj.multiply(adj.T > adj)

        elif undirected and dense:
            adj = dok_matrix((self.nodeCount, self.nodeCount), dtype=np.int)
            for key1, key2 in self.adjMatDict:
                    adj[key1, key2] = 1
            return  (adj + adj.T.multiply(adj.T > adj) - adj.multiply(adj.T > adj)).todense()



    def checkSameEntryAdj(self, node1, node2):
        if self.adjMatDict[node1.ID, node2.ID] == 1 or self.adjMatDict[node1.ID, node2.ID] is not None:
            warnings.warn(
                "multiple edge connection detected and ignored!",

            )
            return True
        else:
            return False

    def checkSelfConnection(self,node1, node2):
        if node1 is node2:
            warnings.warn(
                "self connection detected!",

            )
            return True
        else:
            return False

    # def A(self,undirected=False):
    #     pass
    def edge_list(self):
        pass

class RandomGraph(Graph):

    def __init__(self,n,p,type='gnp'):
        super(RandomGraph,self).__init__()
        self.type =type
        self.p = p
        Dish = PetriDish()
        self.N = Dish.createSimpleNodes(numberOfNodes=n, nodeType=Node, DNA=DNA('random'), Graph=self)
        self.SocialiserObj = randomSocial(p=p)
        self.SocialiserObj.simpleRandomSocialiser(self.N)
        # self.E = Node.adjMatDict
        # self.A = Node.adj(Node)
        self.Ncount = len(self.N)
        # self.Ecount = Node.edgeCount
    def A(self, undirected=False, dense=False):
        return super().A(undirected, dense)





