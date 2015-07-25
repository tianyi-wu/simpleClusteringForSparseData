# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 18:23:59 2015

@author: Wu
"""

import re
import os

import numpy as np
import pandas as pd

CWDPath = os.getcwd() #.encode('utf-8')
digitRe = re.compile(r'\d+')
dimemsionRe = re.compile(r'd(?P<dim>\d+)\-\[(?P<left>-?\d+\.\d{2});\s(?P<right>-?\d+\.\d{2})\[')
IDdigitRe = re.compile(r'ID\=(?P<id>\d+)')



class Cluster(object):
    def __init__(self, number, subspace, n, unitList,  ifNoZero):
        self.number = number        
        self.subspace = subspace
        self.dim = len(subspace)
        self.sampleNum = n
        self.unitList = unitList
        self._updateRange(ifNoZero)
        
    def _updateRange(self, ifNoZero):
        self.dimRange = np.array(self.unitList[0])

        for i in range(1, len(self.unitList)):
            for j in range(self.dim):
                if self.unitList[i][j][1] < self.dimRange[j][1]:
                    self.dimRange[j][1] = self.unitList[i][j][1]
                if self.unitList[i][j][2] > self.dimRange[j][2]:
                    self.dimRange[j][2] = self.unitList[i][j][2]
        
        if ifNoZero:
            self.effectiveDim = sum([1 for i in range(self.dim) if self.dimRange[i][2] > -0.1])
        else:
            self.effectiveDim = sum([1 for i in range(self.dim) if self.dimRange[i][1] > 0.1])
            
  
def getClusterList(clusterDir):
    files = os.listdir(CWDPath + '\\' + clusterDir)
    files = [fname for fname in files if fname[0] == 'c']
    try:
        filesNum = [int(digitRe.search(fileName).group()) for fileName in files]
    except AttributeError as e:
        print e
    filesNum.sort(reverse=True)
    
    n = len(filesNum)
    assert n == filesNum[0]#, str(n) + ' should be equal to file number' + str(filesNum[0])
    
    fileList = [(num, CWDPath + '\\' + clusterDir + '\\cluster_' + str(num) + '.txt') for num in filesNum]    
    
    return fileList







    
def createClusterList(fileList, ifNoZero):
    clusterList = []    
    
    for num, name in fileList:
        with open(name, 'r') as f:
            for i in range(6):
                f.readline() #throw away the useless info
            
            dimemsion = [int(x) for x in digitRe.findall(f.readline())] #get the subdimemsion of the cluster
            sample = int(f.readline().split()[2]) #get the number in that cluster
            
            f.readline() # jumpu the #unit line
            
            unitList = []
            while True:
                line = f.readline()
                if line[0] != '#':
                    break
                unitList.append([[int(x.group('dim')), float(x.group('left')), float(x.group('right'))] for x in dimemsionRe.finditer(line)])
            
            c = Cluster(num, dimemsion, sample, unitList, ifNoZero)
            clusterList.append(c)
    return clusterList
            



def assignCluster(fileList, dataNum, clusterEffMap):
    dataToCluster = np.zeros(dataNum) - 1

    for num, name in fileList:
        with open(name, 'r') as f:
            line = f.readline()
            while line[:2] != 'ID':
                line = f.readline()
            
            while line:
                dataID = int(IDdigitRe.match(line).group('id'))
                if dataToCluster[dataID] < clusterEffMap[num]:
                    dataToCluster[dataID] = num
                line = f.readline()
                
    return dataToCluster
            
        
        
        
if __name__ == "__main__":
    clusterDir = 'NoZero_5_0.001_log13_cluster' #.encode('utf-8')
    dataNum = 23147
    if clusterDir[0] == 'N':
        ifNoZero = True
    else:
        ifNoZero = False
    
    print(ifNoZero)
    
    
    fileList = getClusterList(clusterDir)
    cl = createClusterList(fileList, ifNoZero = ifNoZero)
    cl.sort(key= lambda c : c.effectiveDim, reverse = True)
    
    print(cl[0].effectiveDim)    
    
    with open(CWDPath + '\\' + clusterDir + '\\aResultcluster.txt', 'w') as f:
        for c in cl:
            f.write(str(c.number) + ", " + str(c.effectiveDim) + ", " + str(c.sampleNum) + '\n')
    

#    clusterEffMap = {c.number : c.effectiveDim for c in cl}
#    dataToCluster = pd.Categorical(assignCluster(fileList, dataNum, clusterEffMap))
#    dataToCluster.describe()
    #summary
    
            
    