from Node import *
from DNA import *
from Socialiser import *
from PetriDish import *



class Graph:

    def __init__(self):
       pass


    def A(self,undirected=False):
        pass
    def edge_list(self):
        pass

class RandomGraph(Graph):

    def __init__(self,n,p,type='gnp'):
        super(RandomGraph,self).__init__()
        self.type =type
        self.p = p
        Dish = PetriDish()
        self.N = Dish.createSimpleNodes(numberOfNodes=n, nodeType=Node, DNA=DNA('random'))
        self.SocialiserObj = randomSocial(p=p)
        self.SocialiserObj.simpleRandomSocialiser(self.N)
        self.E = Node.adjMatDict
        self.A = Node.adj(Node)
        self.Ncount = len(self.N)
        self.Ecount = Node.edgeCount






