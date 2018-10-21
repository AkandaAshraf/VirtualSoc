from Node import *
from DNA import *
import Networks
import numpy as np




def createSimpleNodes( numberOfNodes, nodeType, DNA, Graph):

        return [ nodeType(DNA,Graph=Graph) for i in range(numberOfNodes)]

def createSocialNodesThreeFeatures( numberOfNodes, nodeType, DNA,commonLabel, Graph):

         age = np.random.randint(18, high=65, size=numberOfNodes)
         gender = np.random.randint(0, high=2, size=numberOfNodes)
         location = np.random.randint(1, high=100, size=numberOfNodes)

         # if len(DNA)!=numberOfNodes:
         #    label = DNA
         # else:
         #     location = np.random.randint(1, high=100, size=numberOfNodes)

         return [ nodeType(age=age[i], gender=gender[i], location=location[i], label=commonLabel, DNA=DNA, Graph=Graph) for i in range(numberOfNodes)]



def createSocialNodesNFeatures(numberOfNodes, nodeType, DNA, commonLabel, Graph, additionalFeatureLen, addTraidtionalFeatures, npDistFunc):


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

# test = PetriDish.createSimpleNodes(PetriDish,numberOfNodes=5,nodeType=Node,DNA='auto',Graph=Networks.RandomSocialGraph())


# a = 2+3
