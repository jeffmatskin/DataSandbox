from os import listdir
import h5py
import numpy as np
import matplotlib as plt
import pandas as pd

files = listdir("Minute")

h5files = list(map(lambda x: h5py.File(x, 'r')['data'],['Minute/' + fl for fl in files]))

#datakeys = list([h5files[x]['data'].keys() for x in range(0,len(h5files))])
datakeys = list(h5files[0]['data'].keys()) #same across all files.

n = len(files)
m = len(datakeys)

fileSeries = pd.DataFrame([pd.Series([files[i].split('_')[j] for j in range (0,m)]) for i in range(0,n)])
fileSeries['index'][0:len(fileSeries)]
fileSeries.rename(index=int, columns={0:'exch',1:'curr',2:'curr2',3:'freq'},inplace=True)

data = [[h5files[y][datakeys[x]] for x in range(0,m)] for y in range(0,n)]
dataArrays = np.array([list(data[x][:]) for x in range(0,n)])

#by currency:
fileSeries.set_index('curr',inplace=True)
currencies = list(fileSeries.index.unique())
currGroups = [fileSeries.loc[currencies[x]] for x in range(0,m)] # BAD. shouldn't return list.

for curr in currencies:
    thisCurrFiles = fileSeries.loc[curr]
    ## CHECK FOR ARB ##


## np.nanmean() avoids issues of nans.
##CLEAN OUT NANS

