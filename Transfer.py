from Networks import *
import os
class WriteToFile:

    def __init__(self,Graph):
        self.Graph = Graph

    def saveRandomSocialGraphAdvanced(self,graph,folderPath):
        fileGraphInfo = '\\graphInfo.csv'
        fileCurrentEdges =  '\\edges.csv'
        fileDNA = '\\dna.csv'
        graph.writeFileA(folderPath+fileCurrentEdges)

        with open(folderPath + fileGraphInfo, 'w') as f:
            f.write(
                'Nodes,Edges,Features,keenness to connect (percentageOfConnectionNodes),keenness to explore (explorationProbability),popularity preference intensity')
            for i in range(len(graph.labelSplit)):
                f.write(',labelSplit' + str(i))
            if graph.mutualPreferenceIntensity is not None:
                for i in range(len(graph.mutualPreferenceIntensity)):
                    f.write(',mutualPreferenceIntensityLen' + str(i + 2))
            if graph.npDistFunc is not None:
                for i in range(len(graph.npDistFunc)):
                    f.write(',feature dist function' + str(i))
                f.write('\n')
            f.write('%s,%s,%s,%s,%s,%s' % (graph.nodeCount, graph.edgeCount, len(graph.N[0].features),
                                           graph.percentageOfConnectionNodes, graph.explorationProbability,
                                           graph.popularityPreferenceIntensity))
            for ls in graph.labelSplit:
                f.write(',' + str(ls))
            if graph.mutualPreferenceIntensity is not None:
                for mpi in graph.mutualPreferenceIntensity:
                    f.write(',' + str(mpi))
            if graph.npDistFunc is not None:
                for ndf in graph.npDistFunc:
                    f.write(',' + str(ndf).replace(",", " "))

        with open(folderPath + fileDNA, 'w') as f:
            label = 0
            f.write('label,preferPopularityIntensity,preferShorterPathIntensity,value,nodes\n')
            for dna in graph.DNA:
                f.write(
                    '%s,%s,%s' % (str(label), str(dna.preferPopularityIntensity), str(dna.preferShorterPathIntensity)))
                f.write(',')

                for v in dna.value:
                    f.write('%s:' % str(v))
                f.write(',')
                for node in dna.nodes:
                    f.write('%s:' % str(node.ID))
                f.write('\n')
                label += 1

    def easySaveEverything(self,folderPath):
        fileNameNode = '\\nodesWithFeatures.csv'
        fileGraphInfo = '\\graphInfo.csv'
        fileCurrentEdges = '\\edges.csv'
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
            fileNameNode = '\\nodesWithFeatures.csv'
            with open(folderPath + fileNameNode, 'w') as f:
                f.write('Id,label(DNA),inDegree,outDegree')
                for i in range(len(self.Graph.N[0].features)):
                    f.write(',feat' + str(i))
                f.write('\n')
                for n in self.Graph.N:
                    f.write('%s,%s,%s,%s' % (n.ID, n.label, n.inDegree, n.outDegree))
                    for feature in n.features:
                        f.write(',%s' % feature)
                    f.write('\n')
            info = []
            if not self.Graph.keepHistory:
                self.saveRandomSocialGraphAdvanced(folderPath)
                # info.append({'mutationIntensity': self.Graph.mutationIntensity, 'mutatePreference': self.Graph.mutatePreference,
                #              'mutatePreferenceProbability': self.Graph.mutatePreferenceProbability})

            else:
                i = 0
                for evol in self.Graph.evolutionHistory:
                    os.mkdir(folderPath+'\\'+str(i))
                    info.append({'i':i,'mutationIntensity':evol.mutationIntensity, 'mutatePreference':evol.mutatePreference, 'mutatePreferenceProbability':evol.mutatePreferenceProbability})
                    self.saveRandomSocialGraphAdvanced(graph=evol.Graph,folderPath=folderPath+'\\'+str(i))
                    i +=1
                with open(folderPath + '\\info.txt', 'w') as f:
                 for fo in info:
                       f.write('folder:'+ str(fo['i'])+' mutationIntensity: '+str(fo['mutationIntensity'])+' mutatePreference: '+str(fo['mutatePreference'])+' mutatePreferenceProbability: '+str(fo['mutatePreferenceProbability']))
                       f.write('\n')



















