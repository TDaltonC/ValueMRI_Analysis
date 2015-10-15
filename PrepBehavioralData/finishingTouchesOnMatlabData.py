# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 15:09:06 2015

This script exists because MatLAB isn't so much a language as it is a toy for doing 
matrix algbra. I got all of the data out of MATLAB as painlessly as possible and 
now I'm doing the finishing touches here. 

So this takes in "dataFromMatLAB.csv" and rank.csv and the outputs "TrialbyTrial.csv"

@author: Dalton
"""

import pandas as pd

subjects = [3301, 3303, 3304, 3306, 3308, 3309, 3310, 3312, 3313, 3314]

def finishingTouches(subjID):
    trialByTrial = pd.read_csv("../../Data/RawData/SID" + str(subjID) + "/MatLabOutput/dataFromMatLAB.csv")
    optionRanks  = pd.read_csv("../../Data/RawData/SID" + str(subjID) + "/dataFrames/rank" + str(subjID) + ".csv")
    
    trialByTrial.drop(['Opt1Code', 'Opt2Code'], 1, inplace = True)
    #optionRanks.drop('type', 1, inplace = True)
    
    optionRanks.columns = ["Opt1Code","Opt1Item1","Opt1Item2", "Opt1Type"]
    
    trialByTrial = pd.merge(trialByTrial,optionRanks,on = ["Opt1Item1","Opt1Item2"], how = 'left')
    
    optionRanks.columns = ["Opt2Code","Opt2Item1","Opt2Item2", "Opt2Type"]
    
    trialByTrial = pd.merge(trialByTrial,optionRanks,on = ["Opt2Item1","Opt2Item2"], how = 'left')
    
    trialByTrial.to_csv("../../Data/RawData/SID" + str(subjID) + "/dataFrames/trialByTrial.csv")
    
    
for subjID in subjects:
    finishingTouches(subjID)