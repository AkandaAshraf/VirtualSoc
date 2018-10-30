from Networks import *
class WriteToFile:

    def __init__(self,Graph):
        self.Graph = Graph

    def easySaveEverything(self,folderPath):
        fileNameNode = '\\nodesWithFeatures.csv'
        fileGraphInfo = '\\graphInfo.csv'

        if type(self.Graph) is RandomSocialGraphAdvanced:
                with open(folderPath+fileNameNode, 'w') as f:
                    f.write('Id,label(DNA),inDegree,outDegree')
                    for i in range(len(self.Graph.N[0].features)):
                        f.write(',feat'+str(i))
                    f.write('\n')
                    for n in self.Graph.N:
                        f.write('%s,%s,%s,%s' % (n.ID, n.label,n.inDegree,n.outDegree))
                        for feature in n.features:
                            f.write(',%s' % feature)
                        f.write('\n')
                with open(folderPath+fileGraphInfo,'w') as f:
                    f.write('Nodes,Edges,Features,keenness to connect (percentageOfConnectionNodes),keenness to explore (explorationProbability)')
                    for i in range(len(self.Graph.labelSplit)):
                        f.write(',labelSplit'+str(i))
                    f.write('\n')

                    f.write('%s,%s,%s,%s,%s'%(self.Graph.nodeCount, self.Graph.edgeCount, len(self.Graph.N[0].features), self.Graph.percentageOfConnectionNodes, self.Graph.explorationProbability))
                    for ls in self.Graph.labelSplit:
                        f.write(','+str(ls))






