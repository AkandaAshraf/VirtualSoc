import UtilSAlib
from sklearn.datasets import make_regression
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import linear_model
import numpy as np
import pickle as pk
import pandas as pd
from sklearn.model_selection import KFold, cross_val_score
import os
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn import kernel_ridge
from sklearn import svm
from sklearn import gaussian_process
from sklearn import tree
from sklearn import neural_network
from sklearn import neighbors
from string import digits
import seaborn as sns
import matplotlib.pyplot as plt



#
#
# y = UtilSAlib.getCleanStats('D:\\sensitivityAnalaysisVirtualSoc\\')
# y = y.loc[:, 'NumberofEdges':'AvgGeodesicPath']
#
# X, y = make_regression(n_samples=10, n_targets=3, random_state=1)
# # X = pd.read_csv(problemFolderPath + '\\params', sep=' ', header=None)
#
# X = pd.read_csv( 'D:\\sensitivityAnalaysisVirtualSoc\\params', sep=' ', header=None)
# reg = linear_model.LinearRegression()
# y.head(2)
# # MultiOutputRegressor(GradientBoostingRegressor(random_state=0)).fit(X, y).predict(y)
#
# MOR = MultiOutputRegressor(linear_model.LinearRegression())
# MOR.fit(X,y)
# MOR.score(X,y)
# MOR.get_params()
#
# k_fold = KFold(n_splits=10)
# X = X.as_matrix()
# y = y.as_matrix()
# [MOR.fit(X[train], y[train]).score(X[test], y[test]) for train, test in k_fold.split(X)]
#
# cross_val_score(MOR, X, y, cv=k_fold, n_jobs=-1)
# ######################
# y_mat = y
# y = y_mat[:,0]
# Model = linear_model.LinearRegression()
# Model.fit(X,y)
# Model.score(X,y)
# Model.get_params()
#
# k_fold = KFold(n_splits=10)
#
# [Model.fit(X[train], y[train]).score(X[test], y[test]) for train, test in k_fold.split(X)]

# cross_val_score(Model, X, y, cv=k_fold, n_jobs=-1)

def trainModelsIndividual(folderPath, modelOutputFolder, modelTypes):

    y_df = UtilSAlib.getCleanStats(folderPath)
    y_df = y_df.loc[:, 'NumberofEdges':'AvgGeodesicPath']
    y_names = list(y_df)
    problem = pk.load(open(folderPath + '\\problemPickle.obj', 'rb'))
    x_names = problem['names']
    X_df = pd.read_csv(folderPath+'\\params', sep=' ', header=None)

    X_mat = X_df.as_matrix()
    y_mat = y_df.as_matrix()
    X = X_mat

    # os.mkdir(modelOutputFolder + '\\LinearRegression')
    # modelTypes = ['linear_model.LinearRegression()','linear_model.Ridge()','linear_model.LassoLarsIC(criterion=\'bic\')','linear_model.LassoLarsIC(criterion=\'aic\')']

    folderIndex = 12

    for modelType in modelTypes:
        Model = eval(modelType)

        os.mkdir(modelOutputFolder + '\\'+str(folderIndex)+(Model.__class__.__name__))
        results = []

        for i in range(0, y_mat.shape[1]):
            y = y_mat[:,i]


            Model.fit(X, y)
            Model.score(X, y)
            Model.get_params()
            pk.dump(Model, open(modelOutputFolder + '\\'+str(folderIndex)+Model.__class__.__name__+'\\'+y_names[i]+'model.obj', 'wb'))

            k_fold = KFold(n_splits=10)
            # [Model.fit(X[train], y[train]).score(X[test], y[test]) for train, test in k_fold.split(X)]

            results.append([Model.fit(X[train], y[train]).score(X[test], y[test]) for train, test in k_fold.split(X)])

        k = 0
        with open(modelOutputFolder + '\\'+str(folderIndex)+Model.__class__.__name__+'\\results', 'w') as f:
            f.write('propertyName,mean10fold')
            for m in range(1,11):
                f.write(',fold'+str(m))
            f.write('\n')

            for result in results:
                f.write(y_names[k]+','+str(np.average(result))+','+str(result)+'\n')
                k = k+1

        folderIndex = folderIndex+1

folderPath = 'D:\\outputTest\\'

def modelPerformance(folderPath):
    dir = os.listdir(folderPath)
    resultsList = []
    methodNames = []

    for d in dir:
        dfTemp = pd.read_csv(folderPath +d+ '\\results', sep=',', header='infer')
        remove_digits = str.maketrans('', '', digits)
        mtehodNameTemp = d.translate(remove_digits)
        dfTemp['method'] = mtehodNameTemp
        resultsList.append(dfTemp)
        # methodNames.append()

    # resultsList[0]['fold10'].replace(regex=True, inplace=True, to_replace=r'\D', value=r'')
    i = 0

    for result in resultsList:
       resultsList[i]['fold10'] =result['fold10'].map(lambda x: x.lstrip(']').rstrip(']'))
       if i==0:
           dfAll = resultsList[0][['method', 'propertyName', 'fold10']].copy()
       else:
           dfAll = dfAll.append(resultsList[i][['method', 'propertyName', 'fold10']].copy())

       i +=1
    dfAll["fold10"] = pd.to_numeric(dfAll["fold10"])

    ax = sns.catplot(x="propertyName", y="fold10", hue="method", kind="swarm", data=dfAll,
                     height=10,legend=False)

    ax.set_xticklabels(rotation=40, ha="right")

    # plt.title(UniquePropertyNames[i])
    plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5))

    plt.tight_layout()
    plt.show()
    ax.savefig('D://VirtualSocPlots//regression//All.eps', format='eps')

    UniquePropertyNames = dfAll.propertyName.unique()

    DataFrameDict = {elem: pd.DataFrame for elem in UniquePropertyNames}

    for key in DataFrameDict.keys():
        DataFrameDict[key] = dfAll[:][dfAll.propertyName == key]


    for i in range(0, len(UniquePropertyNames)):
        ax = sns.catplot(x="method", y="fold10", kind="swarm", data=DataFrameDict[UniquePropertyNames[i]],
                         height=10,legend=False)

        ax.set_xticklabels(rotation=40, ha="right")
        plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5))

        plt.title(UniquePropertyNames[i])
        plt.tight_layout()
        plt.show()
        ax.savefig('D://VirtualSocPlots//regression//' + UniquePropertyNames[i] + '.eps', format='eps')

    # dfAllPvted = dfAll.pivot(index='method', columns='propertyName', values='fold10')
    #
    # ax = sns.heatmap(dfAll)

    for i in range(0, len(UniquePropertyNames)):
        ax = sns.catplot(x="method", y="fold10", kind="swarm", data=DataFrameDict[UniquePropertyNames[i]],
                         height=10,legend=False)

        ax.set_xticklabels(rotation=40, ha="right")
        plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5))

        plt.title(UniquePropertyNames[i])
        plt.tight_layout()
        plt.show()
        ax.savefig('D://VirtualSocPlots//regression//' + UniquePropertyNames[i] + '.eps', format='eps')








