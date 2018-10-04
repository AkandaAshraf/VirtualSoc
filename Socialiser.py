import numpy as np


class randomSocial:

    def __init__(self,p=0.5, selfConncetions=True):
        self.p = p
        self.selfConncetions = selfConncetions

    def simpleRandomSocialiser(self, nodes):

        # rands = np.random.random_sample(len(nodes)*len(nodes))
        i = 0
        j = 0
        for node1 in nodes:
            if node1.DNA.value=='random':
                for node2 in nodes:
                    if 1.0-self.p <= np.random.uniform(low=0.0, high=1.0, size=None):
                        # if node1.adjMatDict[]
                        if node1 is not node2:
                            node1+node2
                            node2+node1
                        else:
                            if not node1.selfConnected and self.selfConncetions:
                                 node1+node1
                                 # node1.selfConnected=True






#
# listOfNodes  = PetriDish.createSimpleNodes(PetriDish,numberOfNodes=5,nodeType=Node,DNA=DNA)
#
#
# SocialiserObj = randomSocial()
#
# SocialiserObj.simpleRandomSocialiser()