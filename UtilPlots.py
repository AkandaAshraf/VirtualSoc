import pickle as pk
import pandas as pd
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
        df=df.append(pd.DataFrame([('Delta', key, problem['names'][i], v)], columns=Header))
        i += 1

