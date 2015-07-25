# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 16:39:45 2015

@author: Wu
"""

import pandas as pd
import numpy as np

import itertools


def kDimNozeroList(NozeroYmasked, k, ymin = 9, ymax = 21):
    '''
    find the Nozero number in all k-dim combinations
    '''
    result = []
    for index in itertools.combinations(range(ymin, ymax+1), k):
        ind = list(index)        
        nonzero = np.sum(np.all(NozeroYmasked.loc[:,ind], 1))
        result.append((index, nonzero))
    #result.sort(reverse = True, key = lambda x : x[1])
    return max(result, key = lambda x:x[1])
    

def selectBiggestDim(NozeroY, mask, cluster, clusterNum, k, threhold):
    
    dim, number = kDimNozeroList(NozeroY[mask], k)
    #print dim, number
    if number < threhold:
        raise ValueError
    else:
        for i in range(len(NozeroY)):
            if mask[i] and all(NozeroY.loc[i,list(dim)]):
                mask[i] = False
                cluster[i] = clusterNum + 1
    return dim, number, clusterNum    
                



def clusterByNozero(NozeroY, threhold):
    n, m = NozeroY.shape

    DataToclusters = np.zeros(n)
    clustersMask = np.ones(n, bool)
    clusterNum = 0
    clusters = []
    i = 6
    while i >= 1:
        try:
            dim, number, clusterNum = selectBiggestDim(NozeroY, clustersMask, DataToclusters, clusterNum, i, threhold)
        except ValueError:
            print("no data enough for dim {0}".format(i))
            i = i - 1
            continue
        
        clusters.append((dim, number, clusterNum))
        clusterNum += 1
    return DataToclusters, clusters











if __name__ == "__main__":
    meps = pd.read_csv("2012meps.csv", header = None)
    mepsY = meps.ix[:,9:21]
    NoZeroMepsY = mepsY != 0.0 
    
    threhold = 150
    DataTocluster, clusters = clusterByNozero(NoZeroMepsY, threhold)


    ZeroSum = 0
    NoZeroSum = 0
    for i in range(len(DataTocluster)):
        if DataTocluster[i] == 0.0:
            if any(NoZeroMepsY.loc[i,:]) != False:
                NoZeroSum += 1
            else:
                ZeroSum += 1

    
    with open('simpleClustering\\' + str(threhold) +  'DataTocluster.txt', 'w') as fd:
        for i in range(len(DataTocluster)):
            fd.write('{0}, {1} \n'.format(i+1, int(DataTocluster[i])))
            
    with open('simpleClustering\\' + str(threhold) +  'Clusters.txt', 'w') as fc:
        for c in clusters:
            fc.write('cluster {0}, subspace: {1}, dataInCluster: {2} \n'.format(int(c[2]+1), c[0], c[1]))
        fc.write('cluster {0}, subspace: {1}, dataInCluster: {2} (allzero: {3}, notallzero: {4} \n'.format(0, 'others', ZeroSum + NoZeroSum, ZeroSum, NoZeroSum))
        
    
