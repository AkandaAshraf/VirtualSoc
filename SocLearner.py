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


y = UtilSAlib.getCleanStats('D:\\sensitivityAnalaysisVirtualSoc\\')
y = y.loc[:, 'NumberofEdges':'AvgGeodesicPath']

X, y = make_regression(n_samples=10, n_targets=3, random_state=1)
# X = pd.read_csv(problemFolderPath + '\\params', sep=' ', header=None)

X = pd.read_csv( 'D:\\sensitivityAnalaysisVirtualSoc\\params', sep=' ', header=None)
reg = linear_model.LinearRegression()
y.head(2)
# MultiOutputRegressor(GradientBoostingRegressor(random_state=0)).fit(X, y).predict(y)

MOR = MultiOutputRegressor(linear_model.LinearRegression())
MOR.fit(X,y)
MOR.score(X,y)
MOR.get_params()

k_fold = KFold(n_splits=10)
X = X.as_matrix()
y = y.as_matrix()
[MOR.fit(X[train], y[train]).score(X[test], y[test]) for train, test in k_fold.split(X)]

cross_val_score(MOR, X, y, cv=k_fold, n_jobs=-1)
######################
y_mat = y
y = y_mat[:,0]
Model = linear_model.LinearRegression()
Model.fit(X,y)
Model.score(X,y)
Model.get_params()

k_fold = KFold(n_splits=10)

[Model.fit(X[train], y[train]).score(X[test], y[test]) for train, test in k_fold.split(X)]

cross_val_score(Model, X, y, cv=k_fold, n_jobs=-1)
folderPath = 'D:\\sensitivityAnalaysisVirtualSoc\\'
modelOutputFolder = 'D:\\outputTest\\'
def trainModelsIndividual(folderPath, modelOutputFolder):

    y_df = UtilSAlib.getCleanStats(folderPath)
    y_df = y_df.loc[:, 'NumberofEdges':'AvgGeodesicPath']
    y_names = list(y_df)
    problem = pk.load(open(folderPath + '\\problemPickle.obj', 'rb'))
    x_names = problem['names']
    X_df = pd.read_csv(folderPath+'\\params', sep=' ', header=None)

    X_mat = X_df.as_matrix()
    y_mat = y_df.as_matrix()
    X = X_mat

    result = []
    os.mkdir(modelOutputFolder + '\\LinearRegression')
    modelTypes = [linear_model.LinearRegression,linear_model.Ridge]



    for modelType in modelTypes:
        os.mkdir(modelOutputFolder + '\\'+modelType.__name__)

        for i in range(0, y_mat.shape[1]):
            y = y_mat[:,i]
            Model = modelType()
            Model.fit(X, y)
            Model.score(X, y)
            Model.get_params()
            pk.dump(Model, open(modelOutputFolder + '\\'+modelType.__name__+'\\'+y_names[i]+'model.obj', 'wb'))

            k_fold = KFold(n_splits=10)
            # [Model.fit(X[train], y[train]).score(X[test], y[test]) for train, test in k_fold.split(X)]

            result.append([Model.fit(X[train], y[train]).score(X[test], y[test]) for train, test in k_fold.split(X)])

        k = 0
        with open(modelOutputFolder + '\\'+modelType.__name__+'\\results', 'w') as f:
            f.write('propertyName,mean10fold')
            for m in range(1,11):
                f.write(',fold'+str(m))
            f.write('\n')

            for result in result:
                f.write(y_names[k]+','+str(np.average(result))+','+str(result)+'\n')
                k = k+1









