import numpy as np
import warnings


class DNA:

    def __init__(self, value='random', len=5, *args, **kwargs):
        self.value = value
        self.nodes = 'not assigned!'

        if self.value== 'auto':
              self.value = self.__autoGenDNA(len=len)

    def __autoGenDNA(self, len):
        dnaValue = []
        for i in range(1,len+1) :
            rand1 = np.random.uniform(low=0.0, high=1.0, size=None)
            rand2 = np.random.uniform(low=0.0, high=1.0, size=None)
            if rand1 >0.5:
               dnaValue.append(1)
            else:
                dnaValue.append(0)
            dnaValue.append(rand2)

        return dnaValue

    def mutateDNA(self, mutatePreference, mutatePreferenceProbability,intensity=0.1):

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
            warnings.warn("mutateDNA called but no mutation detected, try increasing intensity!")

    def getDnaType(self, *args, **kwargs):
        if self.value == 'random':
            print('Random')
        else:
            print('Mutation detected! (doesn\'t have a valid DNA)')
        return self.value

    def _assignedNodes(self, nodes):
         self.nodes = nodes

    def __str__(self):
        print(self.value)
