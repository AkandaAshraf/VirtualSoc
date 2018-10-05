import numpy as np
from scipy.sparse import dok_matrix
import DNA as d
import warnings
import collections


class Node:


    nodeCount = 0
    edgeCount = 0
    adjMatDict = collections.defaultdict(lambda: None)

    def adj(cls):
        A = dok_matrix((cls.nodeCount, cls.nodeCount),dtype=np.int)
        for key1,key2 in cls.adjMatDict:
            A[key1,key2] = 1
        return A

    def __init__(self, DNA):
        self.connectionsObj = []
        self.connectionsID = []
        self.outDegree = 0
        self.inDegree = 0
        self.ID = Node.nodeCount
        self.DNA = DNA
        self.selfConnected=False
        self.selfConnectionsNumber = 0
        Node.nodeCount += 1

    def __del__(self):
        Node.nodeCount -= 1

    def __add__(self, other):

        if not checkSelfConnection(self,other):
            if not checkSameEntryAdj(self, other):
                Node.adjMatDict[self.ID, other.ID] = 1
                self.connectionsObj.append(other)
                self.connectionsID.append(other.ID)
                Node.edgeCount += 0.5
                self.outDegree += 1
                other.inDegree += 1

        else:
            self.selfConnected = True
            self.selfConnectionsNumber +=1
            Node.adjMatDict[self.ID, other.ID] = 1



class NodeSocial(Node):

    def __init__(self, age, gender, location,DNA, **kwargs):
        super(NodeSocial,self).__init__(DNA)
        self.age = age
        self.gender = gender
        self.location = location
        self.features = {}
        if kwargs is not None:
            for key, value in kwargs.items():
                self.features[key] = value

    def __del__(self):
        super(NodeSocial,self).__del__()

    def __add__(self, other):
        super(NodeSocial,self).__add__(other)




def checkSameEntryAdj(node1,node2):
    if Node.adjMatDict[node1.ID, node2.ID] == 1 or Node.adjMatDict[node1.ID, node2.ID] != None:
        warnings.warn(
            "multiple edge connection detected and ignored!",

        )
        return True
    else:
        return False


def checkSelfConnection(node1, node2):
    if node1 is node2:
        warnings.warn(
            "self connection detected!",

        )
        return True
    else:
        return False



