from Node import *
from DNA import *

class PetriDish:

    def __init__(self):
        pass

    def createSimpleNodes(self, numberOfNodes, nodeType, DNA):

        return [ nodeType(DNA) for i in range(numberOfNodes)]





# test = PetriDish.createSimpleNodes(PetriDish,numberOfNodes=5,nodeType=Node,DNA=DNA)


# a = 2+3
