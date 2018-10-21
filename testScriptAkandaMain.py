from Node import *
from DNA import *
from Socialiser import *
from PetriDish import *
from Networks import *
import numpy as np


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


# G1 = RandomGraph(10, 0.5,undirected=False)

G2 = RandomSocialGraphAdvanced(labelSplit=[1,2,3],connectionPercentageWithMatchedNodes=30,explorationProbability=0.3,addTraidtionalFeatures=False,additionalFeatureLen=5, npDistFunc=['np.random.randint(18, high=80)','np.random.binomial(2, 0.5)'])
#
# G3 = RandomSocialGraph(labelSplit=[50,100],connectionPercentageWithMatchedNodes=30,explorationProbability=0.1)
#
# G4 = RandomSocialGraph(labelSplit=[50,100],connectionPercentageWithMatchedNodes=30,explorationProbability=0.01)


# adj1 = G1.A()


# adj2 = G2.A()

G2.mutateDNA(mutationIntensity=0.8)
G2.mutateDNAandSocialise(mutationIntensity=0.5)
G2.socialise()

adj2 = G2.A()
# np.random.beta()
test = ['np.random.beta(5,1)','binomial(10,0.5)']

#
# m = globals()['np.random']()
# func = getattr(m, 'beta')
# func('5,1')

e = eval(test[0])





a = 2+ 3

