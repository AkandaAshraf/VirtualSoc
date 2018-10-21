import numpy as np
import warnings


class DNA:

    def __init__(self, value='random', len=5, *args, **kwargs):
        self.value = value
        self.nodes = 'not assigned!'
        self.preferPopularity = None
        self.preferShorterPath = None
        self.preferPopularityIntensity = None
        self.preferShorterPathIntensity = None

        if self.value== 'auto':
              self.value = self._autoGenDNA(len=len)

    def _autoGenDNA(self, len):
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

    def mutateDNA(self, mutatePreference, mutatePreferenceProbability,intensity):

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

    def getDnaType(self, *args, **kwargs):
        if self.value == 'random':
            print('Random')
        return self.value

    def _assignedNodes(self, nodes):
         self.nodes = nodes

    def __str__(self):
        print(self.value)



class DNAadvanced(DNA):

    def __init__(self, value='random', len=5,preferPopularity=True,preferShorterPath=True,preferPopularityIntensity=None,preferShorterPathIntensity=None, *args, **kwargs):
        super(DNAadvanced, self).__init__(value=value, len=len)
        self.value = value
        self.nodes = 'not assigned!'
        self.preferPopularity = preferPopularity
        self.preferShorterPath = preferShorterPath
        self.preferPopularityIntensity = preferPopularityIntensity
        self.preferShorterPathIntensity = preferShorterPathIntensity

        if self.value== 'auto':
              self.value = self._autoGenDNA(len=len)


    def _autoGenDNA(self, len):
        if self.preferPopularity and self.preferPopularityIntensity is None:
            self.preferPopularityIntensity = np.random.uniform(low=0.0, high=1.0, size=None)

        if self.preferShorterPath and self.preferShorterPathIntensity is None:
            self.preferShorterPathIntensity = np.random.uniform(low=0.0, high=1.0, size=None)

        return super()._autoGenDNA(len=len)

    def mutateDNA(self, mutatePreference, mutatePreferenceProbability,intensity):
        super().mutateDNA(mutatePreference=mutatePreference, mutatePreferenceProbability=mutatePreferenceProbability,intensity=intensity)

    def getDnaType(self, *args, **kwargs):
        if self.value == 'random':
            print('Random')
        return self.value

    def _assignedNodes(self, nodes):
         self.nodes = nodes

    def __str__(self):
        print(self.value)
