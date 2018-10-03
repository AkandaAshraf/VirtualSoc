import numpy as np
from scipy.sparse import dok_matrix



class Node:


    nodeCount = 0
    edgeCount = 0
    adjMatDict = {}

    def adj(cls):
        A = dok_matrix((cls.nodeCount, cls.nodeCount),dtype=np.int)
        for key1,key2 in cls.adjMatDict:
            A[key1,key2] = 1
        return  A


    def __init__(self):
        self.connections = []
        self.ID = Node.nodeCount
        Node.nodeCount +=1





    def __del__(self):
        Node.nodeCount -= 1

    def __add__(self, other):
        self.connections.append(other)
        Node.edgeCount += 0.5
        Node.adjMatDict[self.ID,other.ID]=1




class NodeSocial(Node):

    def __init__(self, age, gender, location, **kwargs):
        super(NodeSocial,self).__init__()
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









A = NodeSocial(age=23,gender='M',location=(215,111))
B = NodeSocial(age=77, gender='F',location=(2,1251))
C = NodeSocial(age=23,gender='M',location=(215,111))

# A = NodeSocial(age=29, gender='F',location=(2,1251))

A+C
C+A


adj = NodeSocial.adj(NodeSocial)
adj_dense = adj.todense()
a = 0




