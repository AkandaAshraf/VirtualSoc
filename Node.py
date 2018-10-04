import numpy as np
from scipy.sparse import dok_matrix
import DNA as d



class Node:


    nodeCount = 0
    edgeCount = 0
    adjMatDict = {}

    def adj(cls):
        A = dok_matrix((cls.nodeCount, cls.nodeCount),dtype=np.int)
        for key1,key2 in cls.adjMatDict:
            A[key1,key2] = 1
        return A

    def __init__(self, DNA):
        self.connections = []
        self.degree = 0
        self.ID = Node.nodeCount
        self.DNA = DNA
        Node.nodeCount += 1

    def __del__(self):
        Node.nodeCount -= 1

    def __add__(self, other):
        self.connections.append(other)
        Node.edgeCount += 0.5
        Node.adjMatDict[self.ID, other.ID] = 1
        self.degree += 1




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








#
# A = NodeSocial(age=23,gender='M',location=(215,111),DNA = d)
# B = NodeSocial(age=77, gender='F',location=(2,1251),DNA = d.DNA())
# C = NodeSocial(age=23,gender='M',location=(215,111),DNA = d.DNA())
#
# # A = NodeSocial(age=29, gender='F',location=(2,1251))
#
# A+C
# C+A
#
#
# adj = NodeSocial.adj(NodeSocial)
# adj_dense = adj.todense()
# a = 0
#
#
#

