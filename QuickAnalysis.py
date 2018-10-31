from os import listdir
import h5py
import numpy as np
import matplotlib as plt
import pandas as pd

files = listdir("Minute")

h5files = list(map(lambda x: h5py.File(x, 'r')['data']['/data'],['Minute/' + fl for fl in files]))

#datakeys = list([h5files[x]['data'].keys() for x in range(0,len(h5files))])
datakeys = list(h5files[0].keys()) #same across all files.

n = len(files)
m = len(datakeys)

#sort by file names
fileStrs = pd.Series([[files[i].split('_')[j] for j in range (0,m)] for i in range(0,n)])
fileSeries = pd.DataFrame([fileStrs[x] for x in range(0,n)])

#fileSeries['index']=range(0,len(fileSeries))
fileSeries.rename(columns={0:'exch',1:'curr',2:'curr2',3:'freq'},inplace=True)
fileSeries['index'] = range(0,30)
fileSeries.set_index(['curr','exch'])
#fileSeries.reset_index()

#data = [[h5files[y][datakeys[x]] for x in range(0,m)] for y in range(0,n)]

data = [pd.DataFrame([pd.Series(h5files[i]['axis1'], dtype='datetime64[ns]'), 
    pd.Series(h5files[i]['block0_values'])]).transpose()  for i in range(0,n)]

#by currency:
fileSeries.set_index('curr',inplace=True)
currencies = list(fileSeries.index.unique())
currGroups = pd.Series([fileSeries.loc[currencies[x]] for x in range(0,len(currencies))])

for curr in currencies:
    exchs = list(fileSeries.loc[curr]['exch','freq'])
    ## CHECK FOR ARB ##


## np.nanmean() avoids issues of nans.
##CLEAN OUT NANS

def getCurrency(curr):


