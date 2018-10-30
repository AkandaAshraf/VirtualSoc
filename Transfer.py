from Networks import *
class WriteToFile:

    def __init__(self,Graph):
        self.Graph = Graph

    def easySaveEverything(self,folderPath):
        fileName = '\\nodesWithFeatures.csv'
        if type(self.Graph) is RandomSocialGraphAdvanced:

                with open(folderPath+fileName, 'w') as f:
                    f.write('Id,label(DNA),inDegree,outDegree')
                    for i in range(len(self.Graph.N[0].features)):
                        f.write(',feat'+str(i))
                    f.write('\n')
                    for n in self.Graph.N:
                        f.write('%s,%s,%s,%s' % (n.ID, n.label,n.inDegree,n.outDegree))
                        for feature in n.features:
                            f.write(',%s' % feature)
                        f.write('\n')





