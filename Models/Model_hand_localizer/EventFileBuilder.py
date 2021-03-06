# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 12:39:45 2014

@author: Dalton
"""

"""
=========
Imports
=========
"""
import os
import errno
import pandas
import numpy as np
import json
import Contrasts

"""
=========
Functions
=========
"""
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')

"""
=============
CONFIGURATION
=============
""" 
# Model name (make sure the model names in 'code' and 'data' match!)
modelName = "Model_hand_localizer"


# subject directories
subject_list = [
                'SID3301', 'SID3303', 'SID3304', 'SID3306', 'SID3308', 'SID3309', 'SID3310', 'SID3312', 'SID3313', 'SID3314',
                'SID3316', 'SID3318', 'SID3319', 'SID3320', 'SID3321', 'SID3325', 'SID3326', 'SID3328', 'SID3329', 'SID3330', 'SID3331', 'SID3332', 'SID3333', 'SID3334', 'SID3335', 'SID3336'
                ]
# subject_list = ['SID3308']


# System Setting (Local(MAC) or Remote(linux))
# system = "Darwin" # Mac 
system = "Linux"
if system == "Darwin":
    data_dir = "/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data"
    fsl_dir = "/usr/local/fsl"
elif system == "Linux":
    data_dir = "/data"
    fsl_dir = "/usr/share/fsl/5.0"

"""
==============
MEAT & POTATOS
==============
""" 
fixedTime = .2

for subjectID in subject_list:
#   load the trial by trial data for this subject
    trialByTrial = pandas.DataFrame.from_csv(data_dir + '/RawData/' + subjectID + '/DataFrames/trialByTrial.csv', index_col = 'Unnamed: 0')
    trialByTrial['OnsetTime'] = trialByTrial['OnsetTime'] + trialByTrial['ReactionTime'] - fixedTime
    trialByTrial.set_index('OnsetTime', inplace = True, drop = True)
    optionValues = pandas.DataFrame.from_csv(data_dir + '/RawData/' + subjectID + '/DataFrames/optionValue.csv')
    optionValues.reset_index(inplace=True)
    optionValues.set_index('rank', drop=False, inplace=True)
    # # Join the data frames
    # #join trialbytrial and optionvalue on option number so that trailbytrial now has a column for value
    # # Which value model should be used?
    # optionValues.sort('MLEValueS', inplace = True, ascending = False)
    # optionValues['MLE_Rank'] = np.linspace(1, -1, optionValues.shape[0])
    # values1 = optionValues[['MLE_Rank']]
    # # add the value for the screen option
    # values1.columns = ['OptValue']
    # trialByTrial = trialByTrial.merge(values1, how = 'left', left_on = 'Opt1Code', right_index = True)
    # # add the value for the fixed option
    # values1.columns = ['FixedValue']
    # trialByTrial = trialByTrial.merge(values1, how = 'left', left_on = 'Opt2Code', right_index = True)
    
    # # Add a column of ones to the dataframe (this is usefull for creating the three column files)        
    # trialByTrial['ones'] = 1
    
    # # Create the diff column
    # # subtract the control option value from the value vector to make a vector for diff
    # trialByTrial['OptValueDiff'] = abs(trialByTrial['OptValue'] - trialByTrial['FixedValue']

    trialByTrial['Left'] = (trialByTrial['Button']==1)
    trialByTrial['Right']= (trialByTrial['Button']==2)
    trialByTrial['Left'] = trialByTrial['Left'].astype(np.int)
    trialByTrial['Right'] = trialByTrial['Right'].astype(np.int)

    trialByTrial['fixedTime'] = fixedTime

#%% make the event files for each run
    print(subjectID)
    runs = [1,2,3,4,5]
    for run in runs:
#       make the event files for each run seperately.  
#       make the three column format eventfile [onsetTime, Durration, Magnitude]
            # to remove nans, test if a number equals itself
        left3Col = trialByTrial[(trialByTrial.Left  == 1) & (trialByTrial.Run  == run)][['fixedTime','Left']]
        right3Col= trialByTrial[(trialByTrial.Right  == 1) & (trialByTrial.Run  == run)][['fixedTime','Right']]
#       Name and open the destinations for event files
        leftDir  = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/Left.run00'+ str(run) +'.txt')
        rightDir = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/Right.run00'+ str(run) +'.txt')
        
#       write each 3-column event file as a tab dilimited csv
        left3Col.to_csv(leftDir, sep ='\t', header = False)
        right3Col.to_csv(rightDir, sep ='\t', header = False)
#       Be Tidy! Close all of those open files! 
        leftDir.close()
        rightDir.close()

contrasts_dir = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/contrasts.json')
Contrasts.contrasts
json.dump(Contrasts.contrasts, contrasts_dir)
contrasts_dir.close()

