from Node import *
from DNA import *
import Networks
import numpy as np




def createSimpleNodes( numberOfNodes, nodeType, DNA, Graph):

        return [ nodeType(DNA,Graph=Graph) for i in range(numberOfNodes)]

def createSocialNodes( numberOfNodes, nodeType, DNA,commonLabel, Graph):

         age = np.random.randint(18, high=65, size=numberOfNodes)
         gender = np.random.randint(0, high=1, size=numberOfNodes)
         location = np.random.randint(1, high=100, size=numberOfNodes)

         # if len(DNA)!=numberOfNodes:
         #    label = DNA
         # else:
         #     location = np.random.randint(1, high=100, size=numberOfNodes)

         return [ nodeType(age=age[i], gender=gender[i], location=location[i], label=commonLabel,DNA=DNA, Graph=Graph) for i in range(numberOfNodes)]








# test = PetriDish.createSimpleNodes(PetriDish,numberOfNodes=5,nodeType=Node,DNA='auto',Graph=Networks.RandomSocialGraph())


# a = 2+3
