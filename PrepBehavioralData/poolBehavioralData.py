# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 12:00:02 2015

@author: Dalton
"""
'''
Load OptionValue and TrialbyTrail dataframe for each subject 
add a subjectID column to the option value dataFrame
concatinate the trialbyTrial and option value data on to seperate csv's, which start as blank
'''
import pandas as pd

subjects = [3301, 3303, 3304, 3306, 3308, 3309, 3310, 3312, 3313, 3314,
            3316, 3318, 3319, 3320, 3321, 3325, 3326, 3328, 3329, 3330, 3331, 3332, 3333, 3334, 3335, 3336]


def poolDataFrames(subjID, loopCount, dataDir = "../../Data/"):
    trialByTrial = pd.read_csv(dataDir + "RawData/SID" + str(subjID) + "/dataFrames/trialByTrial.csv")
    optionValue  = pd.read_csv(dataDir + "RawData/SID" + str(subjID) + "/dataFrames/optionValue.csv")

    optionValue['SubjID'] = subjID
    
    if loopCount == 0:
        trialByTrial.to_csv(dataDir + "RawData/group/trialByTrial.csv")
        optionValue.to_csv(dataDir + "RawData/group/optionValue.csv")
    else:
        trialByTrial.to_csv(dataDir + "RawData/group/trialByTrial.csv", header = False, mode = 'a')
        optionValue.to_csv(dataDir + "RawData/group/optionValue.csv", header = False, mode = 'a')


# create blank dataFrame
# open data for 3301 and delete all of the rowns and then write just the header
# Use that header only CSV to write the rest of the data to. 


for loopCount, subjID in enumerate(subjects):
    poolDataFrames(subjID, loopCount)