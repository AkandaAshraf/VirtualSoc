import numpy as np
import warnings
import cupy as cp


class DNA:
    '''
     This class is to define a preference for a node. NodeSocial has a DNA. A group of NodeSocial referring to the same DNA
    tells us that all the Nodes in that group has the same preference. In such case, those bunch of nodes would have the
     same label. The assumption here is, on social networks, people usually have different features but what we may want
     to predict as a label is their preferences. Preferences define categories in a social network. For example, a group
     of people on a social network with a certain political view have some commonalities although their features such as
     age, gender might be different. That political view may, in many cases, define their interest on social media in
     terms of connecting with other people. Those preferences are influence their choice of connecting other people and
     how they view their features. Another example could be, there are people who only connect with other people who are
     nearer to them in geolocation. As a result, those group of people would always consider the location feature on
     another person before the connect and will prefer to connect with a person which has a location feature closer
      to them.

    For example, if features are F = [25,10,200] , DNA = [0, 0.5, 1, 0.5, 0, 0.8]  The first two value of DNA,
    DNA[0,1]: 0, 0.5 correspond to the first feature F[0] : 25. The first value is a binary 0/1 called the preference and second is a weighting parameter.
    In this example, 0 implies that difference between the feature value 25 and the other node's feature will be multiplied by -1.
    Thus higher the difference is smaller the score will be.
    That means this Node for the specific feature 25 will prefer someone with a similar feature.
    Whereas, for the 2nd feature F[1]:10  the preference DNA is 1. Thus it will prefer someone with a different feature.
    Because if it's 1 then we do not multiply with -1. Thus higher the difference between nodes bigger the score will be.
    When called from the socialiser class, scores are calculated for both Nodes.
    As for the weighting factor, We multiply it with the other node's feature before calculating the difference. The intuition is, the definition of differences or similarities is different to different people with different taste or preferences. And the preference is defined by the DNA which also corresponds to the label.

    '''

    def __init__(self, value='random', len=5, *args, **kwargs):
        '''

        :param value: random','auto' or an vector, i.e. [0, 0.5, 1, 0.5, 0, 0.8]. If put auto DNA will be randomly
        generated from a uniform distribution'
         :param len: The length of the DNA , the vector length will be 2 * len. This is because there are two numbers
         per feature
        :param args:
        :param kwargs:
        '''
        self.value = value

        self.nodes = []
        self.preferPopularity = None
        self.preferShorterPath = None
        self.preferPopularityIntensity = None
        self.preferShorterPathIntensity = None

        if self.value== 'auto':
            self.value = self._autoGenDNA(len=len)
        elif self.value == 'autoWeightless':
            self.value = self._autoGenDNA2(len=len)

    def _autoGenDNA(self, len):
        '''
        This function is not meant to access by the user but called from the constructor if the DNA.value param is set to 'auto'
        :param len: length of the DNA, vector size will be 2 * len
        :return: a vector containing the DNA
        '''
        dnaValue = []
        for i in range(1,len+1) :
            rand1 = np.random.uniform(low=0.0, high=1.0, size=None)
            rand2 = np.random.uniform(low=0.0, high=1.0, size=None)
            if rand1 >0.5:
               dnaValue.append(1)
            else:
                dnaValue.append(-1)
            dnaValue.append(rand2)

        return dnaValue

    def _autoGenDNA2(self, len):
        '''
        This function is not meant to access by the user but called from the constructor if the DNA.value param is set to 'auto'
        :param len: length of the DNA, vector size will be 2 * len
        :return: a vector containing the DNA
        '''
        dnaValue = []
        for i in range(1, len + 1):
            rand1 = np.random.uniform(low=0.0, high=1.0, size=None)
            rand2 = 1
            if rand1 > 0.5:
                dnaValue.append(1)
            else:
                dnaValue.append(0)
            dnaValue.append(rand2)

        return dnaValue

    def mutateDNA(self, mutatePreference, mutatePreferenceProbability,intensity):
        '''
         This method can be called by the user. This is to mutate/change the DNA after instantiation if needed, mainly to
         to generate dynamic networks
        :param mutatePreference: whether you want to mutate/ change , True/False
        :param mutatePreferenceProbability: whether you want to mutate/ change mutatePreferenceProbability, True/False
        :param intensity: Intensity of mutation. If choosen high all of them will be mutated. Float, 0.00 to 1.00
        :return: void
        '''

        l = len(self.value)
        preferenceMutationCount = 0
        probablityMutationCount = 0

        for i in range(0,l,2):
            if self.value[i]!=0 and self.value[i]!=1:
                raise ValueError('invalid dna, first index is not Preference')
            else:
                if mutatePreference:
                    if 1.0 - intensity <= np.random.uniform(low=0.0, high=1.0, size=None):
                        rand1 = np.random.uniform(low=0.0, high=1.0, size=None)
                        if rand1 > 0.5:
                            self.value[i] = 1
                        else:
                            self.value[i] = 0
                        preferenceMutationCount +=1
                if mutatePreferenceProbability:
                    if 1.0 - intensity <= np.random.uniform(low=0.0, high=1.0, size=None):
                        self.value[i+1] = np.random.uniform(low=0.0, high=1.0, size=None)
                        probablityMutationCount +=1
            i +=1

        if preferenceMutationCount>0 or probablityMutationCount > 0:
           warnings.warn("mutation occured in %s preference(s) and %s probablity(ies)!" % (preferenceMutationCount, probablityMutationCount))
        else:
            warnings.warn("mutateDNA called but no mutation detected, try increasing intensity / changing mutatePreferenceProbability and/or mutatePreference = true!")
        self.valueWeight = cp.asarray(self.value[1::2], dtype=np.float64)
        self.valuePreference = cp.asarray(self.value[0::2], dtype=np.float64)
    def getDnaType(self, *args, **kwargs):
        '''

        :param args:
        :param kwargs:
        :return: show DNA value
        '''

        if self.value == 'random':
            print('Random')
        return self.value

    def _assignedNodes(self, nodes):
         self.nodes = nodes
    def _assignedNode(self, node):
         self.nodes.append(node)

    def __str__(self):
        print(self.value)



class DNAadvanced(DNA):
    '''
    This class inherits DNA class. In this type of DNA popularity preference and path length preference is included

    '''

    def __init__(self, value='random', len=5,preferPopularity=True,preferShorterPath=True,preferPopularityIntensity=None,preferShorterPathIntensity=None, *args, **kwargs):
        '''

        :param value: random','auto' or an vector, i.e. [0, 0.5, 1, 0.5, 0, 0.8]. If put auto DNA will be randomly
        generated from a uniform distribution'
        :param len: The length of the DNA , the vector length will be 2 * len. This is because there are two numbers
         per feature
        :param preferPopularity: Whether or not to prefer popularity/Degree of the nodes. True/False
        :param preferShorterPath: Whether or not to prefer shorter path length nodes. True/False
        :param preferPopularityIntensity: The intensity of the preference of popularity. The preferential Attachment parameter.
        Numeric value.
        :param preferShorterPathIntensity: The intensity of shorter path preference (not implemented)
        :param args:
        :param kwargs:
        '''
        super(DNAadvanced, self).__init__(value=value, len=len)


        self.value = value
        # self.nodes = []
        self.preferPopularity = preferPopularity
        self.preferShorterPath = preferShorterPath
        self.preferPopularityIntensity = preferPopularityIntensity
        self.preferShorterPathIntensity = preferShorterPathIntensity
        # self.percentageOfConnectionNodes = percentageOfConnectionNodes

        if self.value== 'auto':
              self.value = self._autoGenDNA(len=len)
        elif self.value == 'autoWeightless':
            self.value = self._autoGenDNA2(len=len)
        self.valueWeight = cp.asarray(self.value[1::2],dtype=np.float64)
        self.valuePreference = cp.asarray(self.value[0::2], dtype=np.float64)


    def _autoGenDNA(self, len):
        '''
        same as parent class's method but extends to incorporate preferPopularityIntensity , and  preferShorterPathIntensity
        This method meant to be called from the instructor.

        :param len:  length of the DNA, vector size will be 2 * len
        :return:
        '''
        if self.preferPopularity and self.preferPopularityIntensity is None:
            self.preferPopularityIntensity = np.random.uniform(low=0.0, high=1.0, size=None)

        if self.preferShorterPath and self.preferShorterPathIntensity is None:
            self.preferShorterPathIntensity = np.random.uniform(low=0.0, high=1.0, size=None)

        return super()._autoGenDNA(len=len)

    def _autoGenDNA2(self, len):
        '''
        same as parent class's method but extends to incorporate preferPopularityIntensity , and  preferShorterPathIntensity
        This method meant to be called from the instructor.

        :param len:  length of the DNA, vector size will be 2 * len
        :return:
        '''
        if self.preferPopularity and self.preferPopularityIntensity is None:
            self.preferPopularityIntensity = np.random.uniform(low=0.0, high=1.0, size=None)

        if self.preferShorterPath and self.preferShorterPathIntensity is None:
            self.preferShorterPathIntensity = np.random.uniform(low=0.0, high=1.0, size=None)

        return super()._autoGenDNA2(len=len)

    def mutateDNA(self, mutatePreference, mutatePreferenceProbability,intensity):
        '''
        Same as parent class's method but extends to incorporate mutatePreference and mutatePreferenceProbability
        :param mutatePreference: whether you want to mutate/ change , True/False
        :param mutatePreferenceProbability: whether you want to mutate/ change mutatePreferenceProbability, True/False
        :param intensity: Intensity of mutation. If choosen high all of them will be mutated. Float, 0.00 to 1.00
        :return: void
        '''
        super().mutateDNA(mutatePreference=mutatePreference, mutatePreferenceProbability=mutatePreferenceProbability,intensity=intensity)

    def getDnaType(self, *args, **kwargs):
        '''

        :param args:
        :param kwargs:
        :return: DNA value
        '''
        if self.value == 'random':
            print('Random')
        return self.value

    def _assignedNodes(self, nodes):

         self.nodes = nodes

    def __str__(self):
        print(self.value)
