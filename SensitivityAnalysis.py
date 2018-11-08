from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami
import numpy as np
import pandas as pd
import re
#

# param_values = saltelli.sample(problem, 1000)
# Y = Ishigami.evaluate(param_values)
# Si = sobol.analyze(problem, Y)

df=pd.read_csv('D://allStats.csv', sep=',',header='infer')

df1 = df.drop(df[(df.dataset!='0') & (df.dataset!='1') & (df.dataset!='2') ].index)

df1 = df1.drop('Vertices', 1)
df1 = df1.drop('dataset', 1)

explorationProbabilityV = np.linspace(0.01, 1, 300)

Y = []
for i in range(0,300):
    Y.append(explorationProbabilityV[i])
    Y.append(explorationProbabilityV[i])
    Y.append(explorationProbabilityV[i])


maxList = df1.max()
minList = df1.min()
l = len(maxList)
boundsList = []
for i in range(0,l):
    boundsList.append([maxList[i],maxList[i]])


problem = {
    'num_vars': 3,
    'names': list(df1),
    'bounds': boundsList
}
