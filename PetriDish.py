from Node import *
from DNA import *
import Networks
import numpy as np

#All methods here are to generate Nodes


def createSimpleNodes( numberOfNodes, nodeType, DNA, Graph):
        '''
        This method generate simplest type of Nodes. No features are added.
        :param numberOfNodes: The total number of  nodes to be generated. Integer
        :param nodeType: Class type of the Node, Node . Class name. Not to be passed as a string but the name only
        :param DNA: The DNA object
        :param Graph: Graph type object. All generated nodes must be contained within a graph to enable socialisation.
        :return: list of Node type objects
        '''


        return [ nodeType(DNA,Graph=Graph) for i in range(numberOfNodes)]

def createSocialNodesThreeFeatures( numberOfNodes, nodeType, DNA,commonLabel, Graph):
         '''
         This method generates NodeSocial type of nodes with three basic auto-generated features.

         :param numberOfNodes: numberOfNodes: The total number of  nodes to be generated. Integer
         :param nodeType: The Node type must be NodeSocial or more advanced child class of Node but not Node. Class name. Not to be passed as a string but the name only
         :param DNA:  The DNA object.
         :param commonLabel: Label of the generated objects. EVery Node objects refers to one signle DNA object. And that DNA object defines label of the nodes. In this method label is not auto generated and must be
         passed in this param.
         :param Graph: Graph type object. All generated nodes must be contained within a graph to enable socialisation.
         :return:  list of NodeSocial or more advanced type of objects
         '''
         age = np.random.randint(18, high=65, size=numberOfNodes)
         gender = np.random.randint(0, high=2, size=numberOfNodes)
         location = np.random.randint(1, high=100, size=numberOfNodes)

         # if len(DNA)!=numberOfNodes:
         #    label = DNA
         # else:
         #     location = np.random.randint(1, high=100, size=numberOfNodes)

         return [ nodeType(age=age[i], gender=gender[i], location=location[i], label=commonLabel, DNA=DNA, Graph=Graph) for i in range(numberOfNodes)]



def createSocialNodesNFeatures(numberOfNodes, nodeType, DNA, commonLabel, Graph, additionalFeatureLen, addTraidtionalFeatures, npDistFunc):
         '''

         :param numberOfNodes: The total number of  nodes to be generated. Integer
         :param nodeType: The Node type must be NodeSocial or more advanced child class of Node but not Node. Class name. Not to be passed as a string but the name only
         :param DNA: DNA object
         :param commonLabel: Label of the generated objects. EVery Node objects refers to one signle DNA object. And that DNA object defines label of the nodes. In this method label is not auto generated and must be
         passed in this param.
         :param Graph: Graph type object. All generated nodes must be contained within a graph to enable socialisation.
         :param additionalFeatureLen: Number of additional features other than age, gender, and location. Integer
         :param addTraidtionalFeatures: Whether or not to add than age, gender, and location features by default. True/False
         :param npDistFunc: Distribution of additional features. Usually a numpy method as a string. Do not define the size of the generated numbers. Include package name i.e. numpy/np. If it's not a numpy
         method but if it's an user written method then make sure it contains an integer param named size which is used to get the number of random numbers.
         :return:   list of NodeSocial or more advanced type of objects
         '''


         featuresAgeGenderLocation = []
         features = []
         if addTraidtionalFeatures:
             featuresAgeGenderLocation.append(np.random.randint(18, high=80, size=numberOfNodes))
             featuresAgeGenderLocation.append(np.random.randint(0, high=2, size=numberOfNodes))
             featuresAgeGenderLocation.append(np.random.randint(1, high=100, size=numberOfNodes))

         if npDistFunc is not None:


             if not isinstance(npDistFunc, list):
                 for i in range(0, additionalFeatureLen):
                         # if npDistFunc is None:
                         #     features.append(np.random.randint(0, high=100, size=numberOfNodes))
                         # elif npDistFunc is not None:
                         l = len(npDistFunc)
                         #npDistFunc=npDistFunc[:l-2] + 'size=' +numberOfNodes+ npDistFunc[l-2:]
                         features.append(eval(npDistFunc[:l-1] + ',size=' +str(numberOfNodes)+ npDistFunc[l-1:]))
             elif len(npDistFunc)==additionalFeatureLen:
                 for ndf in npDistFunc:
                     l = len(ndf)

                     features.append(eval(ndf[:l - 1] + ',size=' + str(numberOfNodes) + ndf[l - 1:]))

                     # features.append(ndf)
             else:
                 randIntIndexnpDistFunc= np.random.randint(low=0, high=len(npDistFunc), size=additionalFeatureLen)
                 for index in randIntIndexnpDistFunc:
                     npDistFuncTemp = npDistFunc[index]
                     l = len(npDistFuncTemp)
                     features.append(eval(npDistFuncTemp[:l - 1] + ',size=' + str(numberOfNodes) + npDistFuncTemp[l - 1:]))
             featuresNP=np.array(features)

         # if len(DNA)!=numberOfNodes:
         #    label = DNA
         # else:
         #     location = np.random.randint(1, high=100, size=numberOfNodes)


         if addTraidtionalFeatures and additionalFeatureLen >0:
              return [ nodeType(age=featuresAgeGenderLocation[0][i], gender=featuresAgeGenderLocation[1][i], location=featuresAgeGenderLocation[2][i], label=commonLabel, DNA=DNA, Graph=Graph, additionalFeatures= featuresNP[:,i]) for i in range(numberOfNodes)]
         elif addTraidtionalFeatures and additionalFeatureLen ==0:
             return [nodeType(age=featuresAgeGenderLocation[0][i], gender=featuresAgeGenderLocation[1][i],
                              location=featuresAgeGenderLocation[2][i], label=commonLabel, DNA=DNA, Graph=Graph) for i in range(numberOfNodes)]
         elif not addTraidtionalFeatures and additionalFeatureLen >0:
             return [nodeType( label=commonLabel, DNA=DNA, Graph=Graph, additionalFeatures=featuresNP[:, i]) for i in range(numberOfNodes)]

def createSocialNodesNFeaturesSameDist(numberOfNodes, nodeType, dna, Graph, additionalFeatureLen,
                                        addTraidtionalFeatures, npDistFunc,labelSplit,DnaObjType):
             '''

             :param numberOfNodes: The total number of  nodes to be generated. Integer
             :param nodeType: he Node type must be NodeSocial or more advanced child class of Node but not Node. Class name. Not to be passed as a string but the name only
             :param dna: 'auto' , string. This is different from other methods of generating nodes. This is because here labels and DNA's are generated implicitly within the method.
             :param Graph: Graph type object. All generated nodes must be contained within a graph to enable socialisation.
             :param additionalFeatureLen:  Number of additional features other than age, gender, and location. Integer
             :param addTraidtionalFeatures: Whether or not to add than age, gender, and location features by default. True/False
             :param npDistFunc: Distribution of additional features. Usually a numpy method as a string. Do not define the size of the generated numbers. Include package name i.e. numpy/np. If it's not a numpy
             method but if it's an user written method then make sure it contains an integer param named size which is used to get the number of random numbers.
             :param labelSplit: the split of lablel passed as a vector or single integer number. For example, if it's [10 , 20, 30] then 30 nodes will be generated and first 10 nodes will have DNA object 1,
             2nd snd DNA object and 3rd will have  DNA object 3. In this function DNA objects are auto generated and assigned. These DNA also correspond to the label of nodes. So, the first 10 Nodes will have
             label 0, 2nd 10 label 1 , and finally 3rd 10 nodes will have label 2. If you want each node to have a distinct DNA and label then pass a vector such as [1,2,3,.....,28,29]
             :param DnaObjType: DNA class name, DNA or any other advanced DNA class. Single name passed not as a string but name of the class
             :return: list of NodeSocial or more advanced type of objects
             '''

             featuresAgeGenderLocation = []
             features = []
             featureLen = 0
             if addTraidtionalFeatures:
                 featuresAgeGenderLocation.append(np.random.randint(18, high=80, size=numberOfNodes))
                 featuresAgeGenderLocation.append(np.random.randint(0, high=2, size=numberOfNodes))
                 featuresAgeGenderLocation.append(np.random.randint(1, high=100, size=numberOfNodes))
                 featureLen=len(featuresAgeGenderLocation)+featureLen

             if npDistFunc is not None:

                 if not isinstance(npDistFunc, list):
                     for i in range(0, additionalFeatureLen):
                         # if npDistFunc is None:
                         #     features.append(np.random.randint(0, high=100, size=numberOfNodes))
                         # elif npDistFunc is not None:
                         l = len(npDistFunc)
                         # npDistFunc=npDistFunc[:l-2] + 'size=' +numberOfNodes+ npDistFunc[l-2:]
                         features.append(eval(npDistFunc[:l - 1] + ',size=' + str(numberOfNodes) + npDistFunc[l - 1:]))
                 elif len(npDistFunc) == additionalFeatureLen:
                     for ndf in npDistFunc:
                         l = len(ndf)

                         features.append(eval(ndf[:l - 1] + ',size=' + str(numberOfNodes) + ndf[l - 1:]))

                         # features.append(ndf)
                 else:
                     randIntIndexnpDistFunc = np.random.randint(low=0, high=len(npDistFunc), size=additionalFeatureLen)
                     for index in randIntIndexnpDistFunc:
                         npDistFuncTemp = npDistFunc[index]
                         l = len(npDistFuncTemp)
                         features.append(
                             eval(npDistFuncTemp[:l - 1] + ',size=' + str(numberOfNodes) + npDistFuncTemp[l - 1:]))
                 featuresNP = np.array(features)
                 featureLen=len(features)+featureLen

             # if len(DNA)!=numberOfNodes:
             #    label = DNA
             # else:
             #     location = np.random.randint(1, high=100, size=numberOfNodes)
             N = []
             tempN = []
             DNAlist = []
             # DNASpreadIndex = np.empty(labelSplit[-1])
             # startIndexTemp = 0
             # # np.full(i, labelSplit[i])
             # for i in range(0, len(labelSplit)):
             #     DNASpreadIndex[startIndexTemp:labelSplit[i]]= i
             #     startIndexTemp = labelSplit[i]
             # np.random.shuffle(DNASpreadIndex)
             # np.random.shuffle(DNASpreadIndex)
             # np.random.shuffle(DNASpreadIndex)
             # np.random.shuffle(DNASpreadIndex)
             # np.random.shuffle(DNASpreadIndex)

             for i in range(0, len(labelSplit)):
                 DNAlist.append(DnaObjType(dna, len=featureLen))

                 if i ==0:
                     startingIndex = 0
                     endingIndex = labelSplit[i] - 1
                 else:
                     endingIndex = labelSplit[i] - 1



                 if addTraidtionalFeatures and additionalFeatureLen > 0:
                     tempN = [nodeType(age=featuresAgeGenderLocation[0][j], gender=featuresAgeGenderLocation[1][j],
                                      location=featuresAgeGenderLocation[2][j], label=i, DNA=DNAlist[i], Graph=Graph,
                                      additionalFeatures=featuresNP[:, j]) for j in range(startingIndex,endingIndex+1)]
                 elif addTraidtionalFeatures and additionalFeatureLen == 0:
                     tempN = [nodeType(age=featuresAgeGenderLocation[0][j], gender=featuresAgeGenderLocation[1][j],
                                      location=featuresAgeGenderLocation[2][j], label=i, DNA=DNAlist[j], Graph=Graph) for
                              j in range(startingIndex,endingIndex+1)]
                 elif not addTraidtionalFeatures and additionalFeatureLen > 0:
                     tempN = [nodeType(label=i, DNA=DNAlist[i], Graph=Graph, additionalFeatures=featuresNP[:, j]) for j in
                              range(startingIndex, endingIndex + 1)]
                 startingIndex =  labelSplit[i]
                 N = [*N, *tempN]
                 DNAlist[-1]._assignedNodes(tempN)
             Graph.DNA = DNAlist
             return N

def createSocialNodesNFeaturesSameDistWithDNAShuffled(numberOfNodes, nodeType, dna, Graph, additionalFeatureLen,
                                        addTraidtionalFeatures, npDistFunc,labelSplit,DnaObjType):
             '''

             :param numberOfNodes: The total number of  nodes to be generated. Integer
             :param nodeType: he Node type must be NodeSocial or more advanced child class of Node but not Node. Class name. Not to be passed as a string but the name only
             :param dna: 'auto' , string. This is different from other methods of generating nodes. This is because here labels and DNA's are generated implicitly within the method.
             :param Graph: Graph type object. All generated nodes must be contained within a graph to enable socialisation.
             :param additionalFeatureLen:  Number of additional features other than age, gender, and location. Integer
             :param addTraidtionalFeatures: Whether or not to add than age, gender, and location features by default. True/False
             :param npDistFunc: Distribution of additional features. Usually a numpy method as a string. Do not define the size of the generated numbers. Include package name i.e. numpy/np. If it's not a numpy
             method but if it's an user written method then make sure it contains an integer param named size which is used to get the number of random numbers.
             :param labelSplit: the split of lablel passed as a vector or single integer number. For example, if it's [10 , 20, 30] then 30 nodes will be generated and first 10 nodes will have DNA object 1,
             2nd snd DNA object and 3rd will have  DNA object 3. In this function DNA objects are auto generated and assigned. These DNA also correspond to the label of nodes. So, the first 10 Nodes will have
             label 0, 2nd 10 label 1 , and finally 3rd 10 nodes will have label 2. If you want each node to have a distinct DNA and label then pass a vector such as [1,2,3,.....,28,29]
             :param DnaObjType: DNA class name, DNA or any other advanced DNA class. Single name passed not as a string but name of the class
             :return: list of NodeSocial or more advanced type of objects
             '''

             featuresAgeGenderLocation = []
             features = []
             featureLen = 0
             if addTraidtionalFeatures:
                 featuresAgeGenderLocation.append(np.random.randint(18, high=80, size=numberOfNodes))
                 featuresAgeGenderLocation.append(np.random.randint(0, high=2, size=numberOfNodes))
                 featuresAgeGenderLocation.append(np.random.randint(1, high=100, size=numberOfNodes))
                 featureLen=len(featuresAgeGenderLocation)+featureLen

             if npDistFunc is not None:

                 if not isinstance(npDistFunc, list):
                     for i in range(0, additionalFeatureLen):
                         # if npDistFunc is None:
                         #     features.append(np.random.randint(0, high=100, size=numberOfNodes))
                         # elif npDistFunc is not None:
                         l = len(npDistFunc)
                         # npDistFunc=npDistFunc[:l-2] + 'size=' +numberOfNodes+ npDistFunc[l-2:]
                         features.append(eval(npDistFunc[:l - 1] + ',size=' + str(numberOfNodes) + npDistFunc[l - 1:]))
                 elif len(npDistFunc) == additionalFeatureLen:
                     for ndf in npDistFunc:
                         l = len(ndf)

                         features.append(eval(ndf[:l - 1] + ',size=' + str(numberOfNodes) + ndf[l - 1:]))

                         # features.append(ndf)
                 else:
                     randIntIndexnpDistFunc = np.random.randint(low=0, high=len(npDistFunc), size=additionalFeatureLen)
                     for index in randIntIndexnpDistFunc:
                         npDistFuncTemp = npDistFunc[index]
                         l = len(npDistFuncTemp)
                         features.append(
                             eval(npDistFuncTemp[:l - 1] + ',size=' + str(numberOfNodes) + npDistFuncTemp[l - 1:]))
                 featuresNP = np.array(features)
                 featureLen=len(features)+featureLen

             # if len(DNA)!=numberOfNodes:
             #    label = DNA
             # else:
             #     location = np.random.randint(1, high=100, size=numberOfNodes)
             N = []
             tempN = []
             DNAlist = []
             DNASpreadIndex = np.empty(labelSplit[-1],dtype=int)
             startIndexTemp = 0
             # np.full(i, labelSplit[i])
             for i in range(0, len(labelSplit)):
                 DNASpreadIndex[startIndexTemp:labelSplit[i]]= i
                 startIndexTemp = labelSplit[i]
                 DNAlist.append(DnaObjType(dna, len=featureLen))

             np.random.shuffle(DNASpreadIndex)
             np.random.shuffle(DNASpreadIndex)
             np.random.shuffle(DNASpreadIndex)
             np.random.shuffle(DNASpreadIndex)
             np.random.shuffle(DNASpreadIndex)

             for i in range(0, len(labelSplit)):
                 print('getting nodes first:'+str(labelSplit[i]))

                 if i ==0:
                     startingIndex = 0
                     endingIndex = labelSplit[i] - 1
                 else:
                     endingIndex = labelSplit[i] - 1



                 if addTraidtionalFeatures and additionalFeatureLen > 0:
                     for j in range(startingIndex, endingIndex + 1):
                         tempN.append(nodeType(age=featuresAgeGenderLocation[0][j], gender=featuresAgeGenderLocation[1][j],
                                          location=featuresAgeGenderLocation[2][j], label=DNASpreadIndex[j], DNA=DNAlist[DNASpreadIndex[j]], Graph=Graph,
                                          additionalFeatures=featuresNP[:, j]))
                         DNAlist[DNASpreadIndex[j]]._assignedNode(tempN[-1])

                 elif addTraidtionalFeatures and additionalFeatureLen == 0:
                     for j in range(startingIndex,endingIndex+1):
                         tempN.append(nodeType(age=featuresAgeGenderLocation[0][j], gender=featuresAgeGenderLocation[1][j],
                                          location=featuresAgeGenderLocation[2][j], label=DNASpreadIndex[j], DNA=DNAlist[DNASpreadIndex[j]], Graph=Graph))
                         DNAlist[DNASpreadIndex[j]]._assignedNode(tempN[-1])

                 elif not addTraidtionalFeatures and additionalFeatureLen > 0:
                     for j in range(startingIndex, endingIndex + 1):
                         tempN.append(nodeType(label=DNASpreadIndex[j], DNA=DNAlist[DNASpreadIndex[j]], Graph=Graph, additionalFeatures=featuresNP[:, j]))
                         DNAlist[DNASpreadIndex[j]]._assignedNode(tempN[-1])

                 startingIndex =  labelSplit[i]
                 N = [*N, *tempN]
                 tempN = []
             Graph.DNA = DNAlist
             return N

# test = PetriDish.createSimpleNodes(PetriDish,numberOfNodes=5,nodeType=Node,DNA='auto',Graph=Networks.RandomSocialGraph())


# a = 2+3
