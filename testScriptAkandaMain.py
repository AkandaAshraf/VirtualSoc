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


G1 = RandomGraph(10, 0.5,undirected=False)

G2 = RandomSocialGraph(labelSplit=[50,100],connectionPercentageWithMatchedNodes=30,explorationProbability=0.3)
#
# G3 = RandomSocialGraph(labelSplit=[50,100],connectionPercentageWithMatchedNodes=30,explorationProbability=0.1)
#
# G4 = RandomSocialGraph(labelSplit=[50,100],connectionPercentageWithMatchedNodes=30,explorationProbability=0.01)


adj1 = G1.A()


adj2 = G2.A()

G2.mutateDNAandSocialiseAgain(intensity=0.5)



a = 2+ 3

