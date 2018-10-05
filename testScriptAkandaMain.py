from Node import *
from DNA import *
from Socialiser import *
from PetriDish import *
from Networks import *


#
# listOfNodes = PetriDish.createSimpleNodes(PetriDish, numberOfNodes=10, nodeType=Node, DNA=DNA('random'))
#
#
# SocialiserObj = randomSocial(p=0.5)
#
#     # executor = concurrent.futures.ProcessPoolExecutor(10)
#
#
# SocialiserObj.simpleRandomSocialiser(listOfNodes)
# # if __name__ == '__main__':
# #
#
# adj = Node.adj(Node)

G1 = RandomGraph(10,0.5)

G2 = RandomGraph(5,0.8)


adj = G2.A(undirected=True,dense=False)
adjDir = G2.A(undirected=False,dense=False)


a = 2+ 3

