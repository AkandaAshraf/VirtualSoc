from Node import *
from DNA import *
from Socialiser import *
from PetriDish import *





listOfNodes  = PetriDish.createSimpleNodes(PetriDish,numberOfNodes=5,nodeType=Node,DNA=DNA('random'))


SocialiserObj = randomSocial()

SocialiserObj.simpleRandomSocialiser(listOfNodes)

adj = Node.adj(Node)



a = 2+ 3