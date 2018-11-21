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
    N = len(currSet)
    exchs = list(currSet['exch'])
    mins = pd.DataFrame()
    maxs = pd.DataFrame()

    #exchSpread = pd.DataFrame(pd.Series
    for i in range(0,N):
        #GetSpreads(currSet.iloc[i]['data'])
        currSet.iloc[i]['data'].set_index('timestamp', inplace=True)
        mins[currSet.iloc[i][0]] = currSet.iloc[i][1][b'min']
        maxs[currSet.iloc[i][0]] = currSet.iloc[i][1][b'max']
    
    # TO DO: apply sum columns in measuring spread sizes in order to 
    # see available market at the given price
    # (taking the smaller of the two exchange's spreads)
    market_discr = [[0 for i in range(0,N)] for j in range(0,N)]
    if N > 1:
        for i in range(0,N-1):
            for j in range(i,N):
                sprd_ij = maxs[exchs[i]]-mins[exchs[j]]
                sprd_ij_size = -sum(sprd_ij[sprd_ij<0])
                sprd_ji = maxs[exchs[j]]-mins[exchs[i]]
                sprd_ji_size = -sum(sprd_ji[sprd_ji<0])
                market_discr[i][j] = sprd_ij_size + sprd_ji_size



    # construct spreads and compare spreads, vols, etc. 
    # std dev by different chunks.
    # compare every possible pair.
    

