from Node import *
from DNA import *
from Socialiser import *
from PetriDish import *





listOfNodes  = PetriDish.createSimpleNodes(PetriDish,numberOfNodes=2,nodeType=Node,DNA=DNA('random'))


SocialiserObj = randomSocial(p=1)

SocialiserObj.simpleRandomSocialiser(listOfNodes)

adj = Node.adj(Node)



a = 2+ 3