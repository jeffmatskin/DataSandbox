## imports
from os import listdir
import h5py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

####################################################################################
## Functions
####################################################################################
def getOrganizedData(h5files):
    fileStrs = pd.Series([[files[i].split('_')[j] for j in range (0,m)] for i in range(0,n)])
    fileSeries = pd.DataFrame([fileStrs[x] for x in range(0,n)])
    fileSeries.rename(columns={0:'exch',1:'curr',2:'curr2',3:'freq'},inplace=True)

    datalist = []
    valueColumns = list(h5files[0]['block0_items'])

    for fi in range(0,n):
        tsFrame = pd.Series(h5files[fi]['axis1'], name='timestamp',dtype='datetime64[ns]')
        df = pd.DataFrame({valueColumns[i]:h5files[fi]['block0_values'][:,i] \
            for i in range(0,5)})
        df.insert(0,'timestamp', tsFrame)
        datalist.append(df)    
    fileSeries.insert(len(fileSeries.columns),'data',datalist)
    fileSeries.set_index('curr',inplace=True)
    return fileSeries

##expect src1/src2 to be dataframes consisting of time, first, last, min, max, sum
def compareCurr(src1, src2):
    arb = []
    # get spread over the minute (first vs last)
    # get maximal spread over the minute (min vs max)
    # compare the spreads
    #exchSpread = pd.DataFrame({'min': })
    # look for times at which src1.max < src2.min, src1.max < src2.min
    return arb


## add a column of spreads
def GetSpreads(df):
    df['dx'] = df[b'last']-df[b'first']
    df['sprd'] = df[b'max']-df[b'min']

def graphIt(df, col):

    df.plot()

####################################################################################

files = listdir("Minute")

h5files = list(map(lambda x: h5py.File(x, 'r')['data']['/data'],['Minute/' + fl for fl in files]))
datakeys = list(h5files[0].keys()) #same across all files.

n = len(files)
m = len(datakeys)
#get all the data into a DF
fileSeries = getOrganizedData(h5files)

currencies = list(fileSeries.index.unique())
for curr in currencies:
    currSet = fileSeries.loc[curr][['exch','data']]
    exchs = list(currSet['exch'])
    mins = pd.Series([0]*len(currSet.iloc[0]['data']),index=currSet.iloc[0]['data'].index)
    maxs = pd.Series([np.inf]*len(currSet.iloc[0]['data']))

    #exchSpread = pd.DataFrame(pd.Series
    for i in range(0,len(currSet)):
        #GetSpreads(currSet.iloc[i]['data'])
        currSet.iloc[i]['data'].set_index('timestamp', inplace=True)
        mins = pd.DataFrame({'min':mins,'thisxchg':currSet.iloc[i]['data'][b'min']})

    # construct spreads and compare spreads, vols, etc. 
    # std dev by different chunks.
    # compare every possible pair.
    

