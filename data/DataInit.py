#  -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

meps = pd.read_csv("2012meps.csv", header = None)
mepsY = meps.ix[:,9:21]

#mepsY.to_csv('2012mepsY.csv', header = False, index = False)


mepsYlog = pd.DataFrame(np.log(mepsY+1))
#mepsYlog.to_csv('2012mepsYlog.csv', header = False, index = False)

mepsYlogNoZero = mepsYlog.copy()
mepsYlogNoZero[mepsYlog== 0.0] = mepsYlogNoZero[mepsYlog== 0.0] - np.max(mepsYlog)/3.0
#mepsYlogNoZero.to_csv('2012mepsYlogNoZero.csv', header = False, index = False)



"""12,18,19"""
mepsYlog3 = mepsYlog.ix[:,[11,17,18]]
mepsYlog3NoZero = mepsYlogNoZero.ix[:,[11,17,18]]
#mepsYlog3.to_csv('2012mepsYlog3.csv', header = False, index = False)
#mepsYlog3NoZero.to_csv('2012mepsYlog3NoZero.csv', header = False, index = False)


"""12,18,19,14,15"""
mepsYlog5 = mepsYlog.ix[:,[11,17,18,13,14]]
mepsYlog5NoZero = mepsYlogNoZero.ix[:,[11,17,18,13,14]]
#mepsYlog5.to_csv('2012mepsYlog5.csv', header = False, index = False)
#mepsYlog5NoZero.to_csv('2012mepsYlog5NoZero.csv', header = False, index = False)


"""12,18,19,14,15,21"""
mepsYlog6 = mepsYlog.ix[:,[11,17,18,13,14,20]]
mepsYlog6NoZero = mepsYlogNoZero.ix[:,[11,17,18,13,14,20]]
#mepsYlog6.to_csv('2012mepsYlog6.csv', header = False, index = False)
#mepsYlog6NoZero.to_csv('2012mepsYlog6NoZero.csv', header = False, index = False)


