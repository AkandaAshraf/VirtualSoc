import numpy as np


class DNA:

    def __init__(self, value='random',*args, **kwargs):
        self.value = value
        if self.value== 'auto':
              self.value = self.autoGenDNA()

    def autoGenDNA(self,len = 10):
        dnaValue = []
        for i in range(1,len) :
            rand1 = np.random.uniform(low=0.0, high=1.0, size=None)
            rand2 = np.random.uniform(low=0.0, high=1.0, size=None)
            if rand1 >0.5:
               dnaValue.append(1)
            else:
                dnaValue.append(0)
            dnaValue.append(rand2)

        return dnaValue





    def getDnaType(self, *args, **kwargs):
        if self.value == 'random':
            print('Random')
        else:
            print('Mutation detected! (doesn\'t have a valid DNA)')
        return self.value


    def __str__(self):
        print(self.value)
