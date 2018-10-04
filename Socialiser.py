import numpy as np


class randomSocial:

    def __init__(self,p=0.5):
        self.p = p

    def simpleRandomSocialiser(self, nodes):
        # rands = np.random.random_sample(len(nodes)*len(nodes))
        i = 0
        j = 0
        for node1 in nodes:
            if node1.DNA.value=='random':
                for node2 in nodes:
                    if 1-self.p < np.random.normal():
                        node1+node2
                        node2+node1




#
# listOfNodes  = PetriDish.createSimpleNodes(PetriDish,numberOfNodes=5,nodeType=Node,DNA=DNA)
#
#
# SocialiserObj = randomSocial()
#
# SocialiserObj.simpleRandomSocialiser()