from Networks import *
class WriteToFile:

    def __init__(self,Graph):
        self.Graph = Graph

    def easySaveEverything(self,folderPath):
        fileNameNode = '\\nodesWithFeatures.csv'
        fileGraphInfo = '\\graphInfo.csv'
        fileCurrentEdges =  '\\edges.csv'
        fileDNA = '\\dna.csv'
        self.Graph.writeFileA(folderPath+fileCurrentEdges)

        if type(self.Graph) is RandomSocialGraph:

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

        elif type(self.Graph) is RandomSocialGraphAdvanced:

                with open(folderPath+fileNameNode, 'w') as f:
                    f.write('Id,label(DNA),inDegree,outDegree')
                    for i in range(len(self.Graph.N[0].features)):
                        f.write(',feat'+str(i))
                    f.write('\n')
                    for n in self.Graph.N:
                        f.write('%s,%s,%s,%s' % (n.ID, n.label, n.inDegree, n.outDegree))
                        for feature in n.features:
                            f.write(',%s' % feature)
                        f.write('\n')

                with open(folderPath+fileGraphInfo,'w') as f:
                    f.write('Nodes,Edges,Features,keenness to connect (percentageOfConnectionNodes),keenness to explore (explorationProbability),popularity preference intensity')
                    for i in range(len(self.Graph.labelSplit)):
                        f.write(',labelSplit' + str(i))
                    if self.Graph.mutualPreferenceIntensity is not None:
                        for i in range(len(self.Graph.mutualPreferenceIntensity)):
                            f.write(',mutualPreferenceIntensityLen'+str(i+2))
                    if self.Graph.npDistFunc is not None:
                        for i in range(len(self.Graph.npDistFunc)):
                            f.write(',feature dist function'+str(i))
                        f.write('\n')
                    f.write('%s,%s,%s,%s,%s,%s'%(self.Graph.nodeCount, self.Graph.edgeCount, len(self.Graph.N[0].features), self.Graph.percentageOfConnectionNodes, self.Graph.explorationProbability, self.Graph.popularityPreferenceIntensity))
                    for ls in self.Graph.labelSplit:
                        f.write(','+str(ls))
                    if self.Graph.mutualPreferenceIntensity is not None:
                        for mpi in self.Graph.mutualPreferenceIntensity:
                            f.write(',' + str(mpi))
                    if self.Graph.npDistFunc is not None:
                        for ndf in self.Graph.npDistFunc:
                            f.write(',' + str(ndf).replace(","," "))

                with open(folderPath+fileDNA,'w') as f:
                    label = 0
                    f.write('label,preferPopularityIntensity,preferShorterPathIntensity,value,nodes\n')
                    for dna in self.Graph.DNA:
                        f.write('%s,%s,%s'%(str(label),str(dna.preferPopularityIntensity),str(dna.preferShorterPathIntensity)))
                        f.write(',')

                        for v in dna.value:
                            f.write('%s:' % str(v))
                        f.write(',')
                        for node in dna.nodes:
                            f.write('%s:' % str(node.ID))
                        f.write('\n')
                        label +=1

















