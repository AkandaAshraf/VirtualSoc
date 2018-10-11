import numpy as np
from scipy.sparse import dok_matrix
import DNA as d
import warnings
import collections


class Node:


    # nodeCount = 0
    # edgeCount = 0
    # adjMatDict = collections.defaultdict(lambda: None)
    #
    # def adj(cls):
    #     A = dok_matrix((cls.nodeCount, cls.nodeCount),dtype=np.int)
    #     for key1,key2 in cls.adjMatDict:
    #         A[key1,key2] = 1
    #     return A

    def __init__(self, DNA, Graph):
        self.Graph = Graph
        self.connectionsObj = []
        self.connectionsID = []
        self.outDegree = 0
        self.inDegree = 0
        self.ID = self.Graph.nodeCount
        self.DNA = DNA
        self.selfConnected=False
        self.selfConnectionsNumber = 0
        self.Graph.nodeCount += 1

    def __del__(self):
        self.Graph.nodeCount -= 1

    def __add__(self, other):

        if self.Graph.undirected:
            # if not self.Graph.checkSelfConnection(self, other):

                self.connectionsObj.append(other)
                self.connectionsID.append(other.ID)
                other.connectionsObj.append(self)
                other.connectionsID.append(self.ID)
                self.Graph.edgeCount += 0.5

                self.outDegree += 1
                self.inDegree += 1

                other.inDegree += 1
                other.outDegree += 1

                self.Graph.adjMatDict[self.ID, other.ID] = 1
                self.Graph.adjMatDict[other.ID, self.ID] = 1



        elif not self.Graph.undirected:

            # if not self.Graph.checkSelfConnection(self, other):

            self.connectionsObj.append(other)
            self.connectionsID.append(other.ID)
            self.Graph.edgeCount += 0.5
            self.outDegree += 1
            other.inDegree += 1

            self.Graph.adjMatDict[self.ID, other.ID] = 1



class NodeSocial(Node):

    def __init__(self, age, gender, location, label, DNA, Graph, **kwargs):
        super(NodeSocial, self).__init__(DNA, Graph)
        self.age = age
        self.gender = gender
        self.location = location
        self.label =label
        self.features = {}
        if kwargs is not None:
            for key, value in kwargs.items():
                self.features[key] = value

    def __del__(self):
        super(NodeSocial, self).__del__()

    def __add__(self, other):
        super(NodeSocial, self).__add__(other)

    def getScore(self, other):

        ageDiff = abs(self.age - other.age)*self.DNA.value[1]

        if self.DNA.value[0] ==0:
            ageDiff = -1*ageDiff
        locationDiff = abs(self.age- other.age)*self.DNA.value[3]

        if self.DNA.value[2] ==0:
            locationDiff = -1*locationDiff

        genderDiff = abs(self.age- other.age)*self.DNA.value[5]

        if self.DNA.value[4] == 0:
            genderDiff = -1 * genderDiff

        return ageDiff + locationDiff + genderDiff







