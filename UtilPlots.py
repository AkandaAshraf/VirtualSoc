import pickle as pk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from SALib.analyze import sobol
import os
import pickle as pk

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

allStatsSortedWithParams=pd.DataFrame.from_csv('H:/sobolMeta/allStatsSortedWithParams.csv')

allStatsSortedWithParamsExplorationProbablity= allStatsSortedWithParams.sort_values(by='explorationProbability')

allStatsSortedWithParamsExplorationProbablityNew=allStatsSortedWithParamsExplorationProbablity.loc[allStatsSortedWithParamsExplorationProbablity['explorationProbability'] <=1.0]


# allStatsSortedWithParamsExplorationProbablityNew.to_csv('H:/sobolMeta/allStatsSortedWithParamsReducedExppl1.csv')


allStatsSortedWithParamsExplorationProbablityNew[['explorationProbability','NumberofEdges']]

sns.set_context("notebook", font_scale=2.5, rc={"lines.linewidth": 100.5})

g = sns.pairplot(allStatsSortedWithParamsExplorationProbablityNew[['explorationProbability','NumberofEdges']], kind="scatter",height =10)

plt.figure(figsize=(100,100))
plt.tight_layout()
plt.show()
g.savefig('H:/sobolMeta/explorationProbability_NumberofEdges'+'.eps', format='eps')

g = sns.pairplot(allStatsSortedWithParamsExplorationProbablityNew[['explorationProbability','NumberofEdges']], kind="scatter",height =10)
##################################################

plotNetProps('H:/sobolSmall/')
folderPath = 'H:/sobolSmall/'

def plotNetProps(folderPath):
    if not os.path.isdir(folderPath + '/plots'):
        os.makedirs(folderPath + '/plots')
    paramNames = [name.replace('V', '') for name in pk.load(open(folderPath+'/problemPickle.obj', 'rb'))['names']]

    allStats = pd.read_csv(folderPath + '/allStats.csv')
    allStatsSorted=allStats.sort_values(by='dataset').set_index('dataset').copy()

    params =  pd.read_csv(folderPath + '/params',sep=' ',header=None)
    params.columns = paramNames
    allStatsSortedWithParams=pd.concat([allStatsSorted, params], axis=1, sort=False,ignore_index=False)
    allStatsSortedWithParams.to_csv(folderPath + '/StatsParamsComb.csv')
    colNames = list(allStatsSortedWithParams)
    params = colNames[11:]
    properties = colNames[:11]

def plotNetPreds(folderPath):
        if not os.path.isdir(folderPath + '/plots'):
            os.makedirs(folderPath + '/plots')

        StatsParamsComb = pd.read_csv(folderPath + '/StatsParamsComb.csv')
        newCols = ['accFT','accT','accF','accFL','accBest','accTBest','accFLBest','accFBest']

        GCNOutputs = pd.read_csv(folderPath + '/GCNOutputs.csv', sep=',').sort_values(by = 'network').copy()

        GCNOutputsFT = GCNOutputs.loc[GCNOutputs['topologyOnly'] == False].set_index('network').copy()
        GCNOutputsFT = GCNOutputsFT[~GCNOutputsFT.index.duplicated(keep='first')]

        GCNOutputsT = GCNOutputs.loc[GCNOutputs['topologyOnly'] == True].set_index('network').copy()
        GCNOutputsT = GCNOutputsT[~GCNOutputsT.index.duplicated(keep='first')]


        GCNOutputsFL = pd.read_csv(folderPath + '/GCNOutputsFeatureOnlyLaplaced.csv', sep=',').sort_values(by = 'network').set_index('network').copy()
        GCNOutputsFL = GCNOutputsFL[~GCNOutputsFL.index.duplicated(keep='first')]


        GCNOutputsF = pd.read_csv(folderPath + '/GCNOutputsFeatureOnlyNonLaplaced.csv', sep=',').sort_values(by = 'network').set_index('network').copy()
        GCNOutputsF = GCNOutputsF[~GCNOutputsF.index.duplicated(keep='first')]

        GCNDF = pd.DataFrame(list(zip(GCNOutputsFT['test_acc'],GCNOutputsT['test_acc'],GCNOutputsFL['test_acc'],GCNOutputsF['test_acc'])),columns=['GCN_FT', 'GCN_T','GCN_FL','GCN_F'])
        AllDf    = pd.concat([StatsParamsComb,GCNDF],axis=1)
        AllDf.loc[(AllDf['GCN_FT']>=AllDf['GCN_T']) & (AllDf['GCN_FT']>=AllDf['GCN_F']) & (AllDf['GCN_FT']>=AllDf['GCN_FL']),'GCN_best'] = 'GCN_FT'

        AllDf.loc[(AllDf['GCN_T']>=AllDf['GCN_FT']) & (AllDf['GCN_T']>=AllDf['GCN_F']) & (AllDf['GCN_T']>=AllDf['GCN_FL']),'GCN_best'] = 'GCN_T'
        AllDf.loc[(AllDf['GCN_F']>=AllDf['GCN_FT']) & (AllDf['GCN_F']>=AllDf['GCN_T']) & (AllDf['GCN_F']>=AllDf['GCN_FL']),'GCN_best'] = 'GCN_F'
        AllDf.loc[(AllDf['GCN_FL']>=AllDf['GCN_FT']) & (AllDf['GCN_FL']>=AllDf['GCN_T']) & (AllDf['GCN_FL']>=AllDf['GCN_F']),'GCN_best'] = 'GCN_FL'
        AllDf.loc[(AllDf['GCN_FT']>=AllDf['GCN_T']) & (AllDf['GCN_FT']>=AllDf['GCN_F']) & (AllDf['GCN_FT']>=AllDf['GCN_FL']),'GCN_FT_best'] = 'True'
        AllDf.loc[(AllDf['GCN_FT']<AllDf['GCN_T']) | (AllDf['GCN_FT']<AllDf['GCN_F']) | (AllDf['GCN_FT']<AllDf['GCN_FL']),'GCN_FT_best'] = 'False'
        AllDf['diff_FT_T'] = AllDf['GCN_FT'] - AllDf['GCN_T']
        AllDf['diff_FT_FL'] = AllDf['GCN_FT'] - AllDf['GCN_FL']
        AllDf['diff_FT_F'] = AllDf['GCN_FT'] - AllDf['GCN_F']
        AllDf.to_csv(folderPath + '/StatsParamsGCNComb.csv')

        params  =  ['explorationProbability',
                    'popularityPreferenceIntensity',
                    'connectionPercentageWithMatchedNodes',
                    'mutualPreferenceIntensity2',
                    'mutualPreferenceIntensity3',
                    'mutualPreferenceIntensity4']


        for param in params :
            g = sns.pairplot(AllDf[[param,'diff_FT_T']],
                                                      kind="scatter", height=8)

            plt.figure(figsize=(100,100))
            plt.margins(x=0.1, y=0.1, tight=True)

            g.savefig(folderPath + '/plots/'+param+'_diff_FT_T.eps', format='eps' ,bbox_inches='tight')
        for param in params :
            g = sns.pairplot(AllDf[[param,'diff_FT_FL']],
                                                      kind="scatter", height=8)

            plt.figure(figsize=(100,100))
            plt.margins(x=0.1, y=0.1, tight=True)

            g.savefig(folderPath + '/plots/'+param+'diff_FT_FL.eps', format='eps' ,bbox_inches='tight')

        for param in params:
            g = sns.pairplot(AllDf[[param, 'diff_FT_F']],
                             kind="scatter", height=8)

            plt.figure(figsize=(100, 100))
            plt.margins(x=0.1, y=0.1, tight=True)
            g.savefig(folderPath + '/plots/' + param + 'diff_FT_F.eps', format='eps', bbox_inches='tight')

    # for param in params:
    #     for property in properties:
    #         sns.set_context("notebook", font_scale=2, rc={"lines.linewidth": 50})
    #
    #         g = sns.pairplot(allStatsSortedWithParams[[param, property]],
    #                          kind="scatter", height=8)aa
    #
    #         plt.figure(figsize=(100,100))
    #         plt.margins(x=0.1, y=0.1, tight=True)
    #
    #         g.savefig(folderPath + '/plots/'+param+'_'+property+'.eps', format='eps' ,bbox_inches='tight')
    #
    #




# iris = sns.load_dataset("iris")
#
# g = sns.lmplot(x="method", y="S1", hue="param",  data=df)
# titanic = sns.load_dataset("titanic")
# g = sns.catplot(x="class", y="survived", hue="sex", data=titanic,
#                 height=6, kind="bar", palette="muted")
# g.despine(left=True)
# g.set_ylabels("survival probability")
# pk.dump(df,open('D://df', 'wb' ) )
