import pickle as pk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from SALib.analyze import sobol

Si = pk.load(open('D:\\sensitivityAnalaysisVirtualSoc\\Sobol.obj', 'rb'))
problem = pk.load(open('D:\\sensitivityAnalaysisVirtualSoc\\problemPickle.obj', 'rb'))

Header = []
Header.append('method')
Header.append('property')
Header.append('param')
Header.append('S1')

df = pd.DataFrame(columns=Header)

for key, value in Si.items():
    i = 0
    for v in value['S1']:
        df=df.append(pd.DataFrame([('Sobol', key, problem['names'][i], v)], columns=Header))
        i += 1

Si = pk.load(open('D:\\sensitivityAnalaysisVirtualSocRBDFAST\\SiRDBFAST.obj', 'rb'))
problem = pk.load(open('D:\\sensitivityAnalaysisVirtualSocRBDFAST\\problemPickle.obj', 'rb'))

for key, value in Si.items():
    i = 0
    for v in value['S1']:
        df=df.append(pd.DataFrame([('RBDFAST', key, problem['names'][i], v)], columns=Header))
        i += 1

Si = pk.load(open('D:\\sensitivityAnalaysisVirtualSocRBDFAST\\SiDelta.obj', 'rb'))
problem = pk.load(open('D:\\sensitivityAnalaysisVirtualSocRBDFAST\\problemPickle.obj', 'rb'))

for key, value in Si.items():
    i = 0
    for v in value['S1']:
        df=df.append(pd.DataFrame([('Delta', key, problem['names'][i], v)], columns=Header))
        i += 1

Si = pk.load(open('D:\\sensitivityAnalaysisVirtualSocFAST\\FAST.obj', 'rb'))
problem = pk.load(open('D:\\sensitivityAnalaysisVirtualSocFAST\\problemPickle.obj', 'rb'))

for key, value in Si.items():
    i = 0
    for v in value['S1']:
        df=df.append(pd.DataFrame([('FAST', key, problem['names'][i], v)], columns=Header))
        i += 1
sns.set(rc={'figure.figsize':(60,60)})
plt.figure(figsize=(15, 8))

ax = sns.catplot(x="property", y="S1", hue="method", kind="swarm", data=df, height=10)


ax.set_xticklabels( rotation=40, ha="right")
plt.tight_layout()
plt.show()
ax.savefig('D://VirtualSocPlots/catplot1.eps', format='eps')

UniquePropertyNames = df.property.unique()

DataFrameDict = {elem : pd.DataFrame for elem in UniquePropertyNames}

for key in DataFrameDict.keys():
    DataFrameDict[key] = df[:][df.property == key]

test  = DataFrameDict['NumberofEdges']


for i in range(0,len(UniquePropertyNames)):

    ax = sns.catplot(x="param", y="S1", hue="method", kind="swarm", data=DataFrameDict[UniquePropertyNames[i]], height=10)

    ax.set_xticklabels( rotation=40, ha="right")
    plt.title(UniquePropertyNames[i])

    plt.tight_layout()
    plt.show()
    ax.savefig('D://VirtualSocPlots/'+UniquePropertyNames[i]+'.eps', format='eps')

# iris = sns.load_dataset("iris")
#
# g = sns.lmplot(x="method", y="S1", hue="param",  data=df)
# titanic = sns.load_dataset("titanic")
# g = sns.catplot(x="class", y="survived", hue="sex", data=titanic,
#                 height=6, kind="bar", palette="muted")
# g.despine(left=True)
# g.set_ylabels("survival probability")
# pk.dump(df,open('D://df', 'wb' ) )