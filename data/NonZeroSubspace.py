# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 18:20:50 2015

@author: Wu
"""
import pandas as pd
import numpy as np

import itertools

meps = pd.read_csv("2012meps.csv", header = None)
mepsY = meps.ix[:,9:21]
NoZeroMepsY = mepsY != 0.0 
#mepsY.to_csv('2012mepsY.csv', header = False, index = False)

#result = []
#for i,j,k in itertools.combinations(range(9,22),3):
#    nonzero = sum([all([x, y, z]) for x, y, z in zip(NoZeroMepsY[i], NoZeroMepsY[j], NoZeroMepsY[k]) ])
#    result.append([(i, j, k),nonzero])
#    
#    
#result300 = [str(x)+' \n' for x in result if x[1] >= 300]
#num300 = sum([x[1] > 300 for x in result])
#
#with open('summary_3d.txt', 'w') as f:
#    f.write('the number of 3d > 300 data is {0}.\n'.format(num300))
#    f.writelines(result300)
#

result = []
for i, j, k, l in itertools.combinations(range(9,22),4):
    nonzero = sum([all([x, y, z, w]) for x, y, z, w in zip(NoZeroMepsY[i], NoZeroMepsY[j], NoZeroMepsY[k], NoZeroMepsY[l])])
    result.append([(i, j, k),nonzero])
    
    
result400 = [str(x)+' \n' for x in result if x[1] >= 300]


with open('summary_4d.txt', 'w') as f:
    f.write('the number of 3d > 150 data is {0}.\n'.format(sum([x[1] > 150 for x in result])))
    
    f.write('the number of 3d > 200 data is {0}.\n'.format(sum([x[1] > 200 for x in result])))
    
    f.write('the number of 3d > 250 data is {0}.\n'.format(sum([x[1] > 250 for x in result])))
    
    f.write('the number of 3d > 300 data is {0}.\n'.format(sum([x[1] > 300 for x in result])))
    

    
    f.writelines(result400)