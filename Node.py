import numpy as np
from scipy.sparse import dok_matrix
import DNA as d
import warnings
import collections
import copy
import cupy as cp
class Node:
    ''' This is a root/parent class which creates objects with the basic structure of nodes. It does not have an features.'''


    # nodeCount = 0
    # edgeCount = 0
    # adjMatDict = collections.defaultdict(lambda: None)
    #
    # def adj(cls):
    #     A = dok_matrix((cls.nodeCount, cls.nodeCount),dtype=np.int)
    #     for key1,key2 in cls.adjMatDict:
    #         A[key1,key2] = 1
    #     return A

    def __init__(self, DNA, Graph):
        '''
        :param DNA: this filed refers to a DNA type object and also passed through the constructor(__init__()).  The is a reference type filed i.e. shallow copied
        :param this field refers to a graph type object and passed through the constructor(__init__()).  The is a reference type filed i.e. shallow copied. The assumption is, all the nodes should belong to a graph. The graph type object would contain global properties of the network, such as an adjacency matrix. For more info, refer to the Graph class documentation

        outDegree: and self.inDegree are degree counts and are not available to initialise through the constructor.  At instantiation, these two fileds are set to zero and incremented whenever a new connection is created the node object. For an undirected graph, both are incremented

        ID:  this is the unique id of a Node object and automatically set from the self.Graph.nodeCount. This is deep copied and should not be set explicitly.

        selfConnected: this is a binary True/False field defines if self-connection exists for a given node. The default value is False. Whenever a self-connection is created this is set to True.

        ConnectionsNumber: this filed counts number of self-connection a node has.

        Graph.nodeCount: this filed is referenced to the global Graph object's nodeCount field. Whenever a node is created this field is incremented.

        connectionsObj: this is a list contains the reference to the connected node(s)' objects.

        connectionsID: this is a list contains a list of the connected node(s)' id(s).

        '''

        self.Graph = Graph
        self.connectionsObj = []
        self.connectionsID = []
        self.outDegree = 0
        self.inDegree = 0
        self.ID = copy.deepcopy(self.Graph.nodeCount)
        self.DNA = DNA
        self.selfConnected=False
        self.selfConnectionsNumber = 0
        self.Graph.nodeCount += 1

    def __del__(self):
        '''
        This function is built in special function which is called when an object is destroyed. When delete is called it also decreases the node count from the Graph object        :return: no return
        '''

        self.Graph.nodeCount -= 1

    def __add__(self, other):
        '''
        This is a special function which is called when + operation is performed between two Node type objects.
        This function builds a connection(s) between the nodes. If it's an undirected graph (if self.Graph.undirected) then when this is called it:
        - increases outDegree and inDegree by 1
        - puts a reference of the self and other object in both of them's connectionsObj  fields
        - puts a value of the self and other object's label in both of them's connectionsID fields
        - increases the referenced graph object's edge count through Graph.edgeCount
        - puts the connection in the adjacency matrix in the referenced graph object's Graph.adjMatDict field.
        For the case of an undirected graph (i.e. when self.Graph.undirected is false) the left side object of the + operator gets an out degree and the right side gets an in degree.
        The Graph.edgeCount is incremented by 0.5 for each connection when it's directed (but for directed it's 1)
        :param other: the other Node object to the right side of the + operator
        :return: void
        '''

        if self.Graph.undirected:
            # if not self.Graph.checkSelfConnection(self, other):

                self.connectionsObj.append(other)
                self.connectionsID.append(other.ID)
                other.connectionsObj.append(self)
                other.connectionsID.append(self.ID)
                self.Graph.edgeCount += 1

                self.outDegree += 1
                self.inDegree += 1

                other.inDegree += 1
                other.outDegree += 1

                self.Graph.adjMatDict[self.ID, other.ID] = 1
                self.Graph.adjMatDict[other.ID, self.ID] = 1



        elif not self.Graph.undirected:

            # if not self.Graph.checkSelfConnection(self, other):

            self.connectionsObj.append(other)
            self.connectionsID.append(other.ID)
            self.Graph.edgeCount += 0.5
            self.outDegree += 1
            other.inDegree += 1

            self.Graph.adjMatDict[self.ID, other.ID] = 1



class NodeSocial(Node):
    '''
    This is a child class of class Node. Objects with this class type have features and can calculate score against another node
    '''


    def __init__(self, label, DNA, Graph, additionalFeatures=None, age=None, gender=None, location=None):
        '''

        :param label: The label corresponds to the type of DNA object a NodeSocial object refers to.
        The assumption here is, all the NodeSocial node's preference will be defined by their DNAs which gives the label of the preference.

        :param DNA: same as parent class Node , inherited

        :param Graph: same as parent class Node, inherited
        :param additionalFeatures: If there are more features other than age, gender, location, the are passed as a list.
        The default value is None
        :param age: feature Age, integer. Default is None
        :param gender: feature gender, integer 0 or 1. Default is None
        :param location: feature gender, integer Default is None

        The features filed creates a list of all the features including age, gender, location and additional features

        '''
        super(NodeSocial, self).__init__(DNA, Graph)


        self.features = []

        if age is not None:
            self.age = age
            self.features.append(age)
        if gender is not None:
            self.gender = gender
            self.features.append(gender)

        if gender is not None:
             self.location = location
             self.features.append(location)



        self.label =label
        ### add all the features in the following list

        # self.features = [self.age, self.gender, self.location]
        if additionalFeatures is not None:
            for value in additionalFeatures:
                self.features.append(value)
        if Graph._useGPU and Graph.createInGPUMem:
            self.featuresCP = cp.asarray(self.features)

    def __del__(self):
        '''
        This simply calls the parent class method (no overriding)
        :return: void
        '''
        super(NodeSocial, self).__del__()

    def __add__(self, other):
        '''
        This simply calls the parent class method (no overriding)

        :param other: see parent class's method
        :return: void
        '''
        super(NodeSocial, self).__add__(other)

    def getScore(self, other):
        '''
         This method calculates the score between two nodes to provide the likelihood of two nodes making a connection.
         However, if the decision of connection depends on the socialiser object. The score is calculated based on the DNA and features.
        The size of the DNA vector is twice the size of the feature vector.
         For example, if features are F = [25,10,200] , DNA = [0, 0.5, 1, 0.5, 0, 0.8]  The first two value of DNA,
         DNA[0,1]: 0, 0.5 correspond to the first feature F[0] : 25. The first value is a binary 0/1 called the preference and second is a weighting parameter.
         In this example, 0 implies that difference between the feature value 25 and the other node's feature will be multiplied by -1.
         Thus higher the difference is smaller the score will be.
         That means this Node for the specific feature 25 will prefer someone with a similar feature.
         Whereas, for the 2nd feature F[1]:10  the preference DNA is 1. Thus it will prefer someone with a different feature.
         Because if it's 1 then we do not multiply with -1. Thus higher the difference between nodes bigger the score will be.
         When called from the socialiser class, scores are calculated for both Nodes.
         As for the weighting factor, We multiply it with the other node's feature before calculating the difference. The intuition is, the definition of differences or similarities is different to different people with different taste or preferences. And the preference is defined by the DNA which also corresponds to the label.

        :param other: the other node.
        :return: void
        '''
        i=0

        sumScore = 0

        for featureSelf in self.features:
              featDiff = abs(featureSelf - other.features[i]) * self.DNA.value[i+1]
              if self.DNA.value[i] == 0:
                  featDiff = -1 * featDiff
              sumScore = sumScore + featDiff

        # ageDiff = abs(self.age - other.age)*self.DNA.value[1]
        #
        # if self.DNA.value[0] ==0:
        #     ageDiff = -1*ageDiff
        # locationDiff = abs(self.age- other.age)*self.DNA.value[3]
        #
        # if self.DNA.value[2] ==0:
        #     locationDiff = -1*locationDiff
        #
        # genderDiff = abs(self.age- other.age)*self.DNA.value[5]
        #
        # if self.DNA.value[4] == 0:
        #     genderDiff = -1 * genderDiff

        return sumScore

    def getScoreAdvanced(self, other, popularityPreferenceIntensity, mutualPreferenceIntensity, multPopularityPreference=False,multMutualPreference=False):
        '''
        This is same as getScore, except it considers degree of the Node.

        This method calculates the score between two nodes to provide the likelihood of two nodes making a connection.
         However, if the decision of connection depends on the socialiser object. The score is calculated based on the DNA and features.
        The size of the DNA vector is twice the size of the feature vector.
         For example, if features are F = [25,10,200] , DNA = [0, 0.5, 1, 0.5, 0, 0.8]  The first two value of DNA,
         DNA[0,1]: 0, 0.5 correspond to the first feature F[0] : 25. The first value is a binary 0/1 called the preference and second is a weighting parameter.
         In this example, 0 implies that difference between the feature value 25 and the other node's feature will be multiplied by -1.
         Thus higher the difference is smaller the score will be.
         That means this Node for the specific feature 25 will prefer someone with a similar feature.
         Whereas, for the 2nd feature F[1]:10  the preference DNA is 1. Thus it will prefer someone with a different feature.
         Because if it's 1 then we do not multiply with -1. Thus higher the difference between nodes bigger the score will be.
         When called from the socialiser class, scores are calculated for both Nodes.
         As for the weighting factor, We multiply it with the other node's feature before calculating the difference. The intuition is, the definition of differences or similarities is different to different people with different taste or preferences. And the preference is defined by the DNA which also corresponds to the label.




        :param other:  other Node
        :param popularityPreferenceIntensity: The parameter for preferential attachment. If it's 0 then degree of the given
        Node and the other Node is not considered. If it's >0 then the degree of the other Other Node is weighted.
        are not considered
        :param mutualPreferenceIntensity: Not implemented
        :return: void
        '''



        # i = 0
        # j=0
        #
        # sumScore2 = 0
        #
        # # for featureSelf in self.features:
        # #     featDiff = abs(featureSelf - other.features[i]) * self.DNA.value[i + 1]
        # #     if self.DNA.value[i] == 0:
        # #         featDiff = -1 * featDiff
        # #     sumScore = sumScore + featDiff
        # #     i = i+1
        # #
        # for featureSelf in self.features:
        #     featDiff = abs(featureSelf - other.features[j]) * self.DNA.value[i+1]
        #     # print(self.DNA.value[i+1])
        #     # print(self.DNA.value[i])
        #
        #     if self.DNA.value[i] == -1:
        #         featDiff = -1 * featDiff
        #     sumScore2 = sumScore2 + featDiff
        #     j = j+1
        #     i = i+2
        useGPU = self.Graph._useGPU
        createInGPUMem = self.Graph.createInGPUMem
        if cp.cuda.is_available() and useGPU:
            if createInGPUMem:
                sumScore = cp.asnumpy(cp.sum(cp.multiply(
                    cp.multiply(cp.absolute(cp.subtract(self.featuresCP, other.featuresCP)), self.DNA.valueWeight),
                    self.DNA.valuePreference)))
            else:    
                dnaValueWeight = cp.asarray(self.DNA.value[1::2],dtype=np.float64)
                dnaValuePreference = cp.asarray(self.DNA.value[0::2],dtype=np.float64)
                selfFeatures =  cp.asarray(self.features,dtype=np.float64)
                otherFeatures =  cp.asarray(other.features,dtype=np.float64)
                featDiffV = cp.subtract(selfFeatures, otherFeatures)
                featDiffAbsV = cp.absolute(featDiffV)
                featDiffAbsWeightedV = cp.multiply(featDiffAbsV,dnaValueWeight)
                featDiffAbsWeightedPreferencedV =  cp.multiply(featDiffAbsWeightedV,dnaValuePreference)
                sumScore = cp.sum(featDiffAbsWeightedPreferencedV)
            # sumScore = cp.asnumpy(cp.sum(cp.multiply(cp.multiply(cp.absolute(cp.subtract(self.featuresCP, other.featuresCP)),self.DNA.valueWeight),self.DNA.valuePreference)))
        else:
            sumScore = np.sum(np.multiply(np.multiply(np.absolute(np.subtract(self.features, other.features)),self.DNA.value[1::2]),self.DNA.value[0::2]))
              
        # dnaValueWeight = dnaValueTemp[1::2]

        if multPopularityPreference:
            sumScore = sumScore * popularityPreferenceIntensity * (other.outDegree + other.inDegree)
        else:
            sumScore = sumScore + popularityPreferenceIntensity*(other.outDegree+other.inDegree)*self.DNA.preferPopularityIntensity


        if self.Graph.Socialised:
            if mutualPreferenceIntensity is not None:
                i = 0
                tempPath2 = 0
                tempPath3 = 0
                tempPath4 = 0

                for mpi in mutualPreferenceIntensity:
                    if i == 0:
                        if self.Graph.adjP2[self.ID, other.ID]>0:
                            tempPath2 = mpi*self.DNA.preferShorterPathIntensity[0]
                    elif i ==1:
                        if self.Graph.adjP3[self.ID, other.ID]>0:
                            tempPath3 = mpi*self.DNA.preferShorterPathIntensity[1]
                    elif i ==2:
                        if self.Graph.adjP4[self.ID, other.ID]>0:
                            tempPath4 =mpi*self.DNA.preferShorterPathIntensity[2]
                    i +=1
                if multMutualPreference:
                    if tempPath2!=0:
                        sumScore = sumScore * tempPath2
                    if tempPath3 != 0:
                        sumScore = sumScore * tempPath3
                    if tempPath4 != 0:
                        sumScore = sumScore * tempPath4
                # else:
                    sumScore = sumScore + tempPath2 + tempPath3 + tempPath4

        # if self.DNA.

        # ageDiff = abs(self.age - other.age)*self.DNA.value[1]
        #
        # if self.DNA.value[0] ==0:
        #     ageDiff = -1*ageDiff
        # locationDiff = abs(self.age- other.age)*self.DNA.value[3]
        #
        # if self.DNA.value[2] ==0:
        #     locationDiff = -1*locationDiff
        #
        # genderDiff = abs(self.age- other.age)*self.DNA.value[5]
        #
        # if self.DNA.value[4] == 0:
        #     genderDiff = -1 * genderDiff

        return sumScore








