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
import seaborn as sb
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
modelName = "Model_002_S_last500ms"


# subject directories
subject_list = [
                'SID3301', 'SID3303', 'SID3304', 'SID3306', 'SID3308', 'SID3309', 'SID3310', 'SID3312', 'SID3313', 'SID3314',
                'SID3316', 'SID3318', 'SID3319', 'SID3320', 'SID3321', 'SID3325', 'SID3326', 'SID3328', 'SID3329', 'SID3330', 'SID3331', 'SID3332', 'SID3333', 'SID3334', 'SID3335', 'SID3336'
                ]

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
for subjectID in subject_list:
#   load the trial by trial data for this subject
    trialByTrial = pandas.DataFrame.from_csv(data_dir + '/RawData/' + subjectID + '/DataFrames/trialByTrial.csv', index_col = 'OnsetTime')
    optionValues = pandas.DataFrame.from_csv(data_dir + '/RawData/' + subjectID + '/DataFrames/optionValue.csv')
    optionValues.reset_index(inplace=True)
    optionValues.set_index('rank', drop=False, inplace=True)
    # Join the data frames
    #join trialbytrial and optionvalue on option number so that trailbytrial now has a column for value
    # Which value model should be used?
    values1 = optionValues[['MLEValueS']]
    # add the value for the screen option
    values1.columns = ['OptValue']
    trialByTrial = trialByTrial.merge(values1, how = 'left', left_on = 'Opt1Code', right_index = True)
    # add the value for the fixed option
    values1.columns = ['FixedValue']
    trialByTrial = trialByTrial.merge(values1, how = 'left', left_on = 'Opt2Code', right_index = True)
    
    # Add a column of ones to the dataframe (this is usefull for creating the three column files)        
    trialByTrial['ones'] = 1
    
    # Create the diff column
    # subtract the control option value from the value vector to make a vector for diff
    trialByTrial['OptValueDiff'] = abs(trialByTrial['OptValue'] - trialByTrial['FixedValue'])
    
#    Pop the index out, 
    trialByTrial.reset_index(inplace=True)
#    add reaction time to it, and subtract 0.5 seconds
    trialByTrial['OnsetTime'] = trialByTrial['OnsetTime'] + trialByTrial['ReactionTime'] - 0.5
     # put it back as the index, 
    trialByTrial.set_index('OnsetTime', drop=False, inplace=True)
    # use a fixed boxcar leangth of 0.5 seconds (instead of reaction time)
    trialByTrial['halfSec'] = 0.5

#%% make the event files for each run
    print(subjectID)
    runs = [1,2,3,4,5]
    for run in runs:
#       make the event files for each run seperately.  
#       make the three column format eventfile [onsetTime, Durration, Magnitude]
            # to remove nans, test if a number equals itself
        control3Col = trialByTrial[(trialByTrial.Opt1Type == 1) & (trialByTrial.Run  == run)][['halfSec','ones']]
        controlValue3Col = trialByTrial[(trialByTrial.Opt1Type == 1) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['halfSec','OptValue']]
        controlDifficulty3Col = trialByTrial[(trialByTrial.Opt1Type == 1) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['halfSec','OptValueDiff']]
        
        scaling3Col = trialByTrial[(trialByTrial.Opt1Type == 2) & (trialByTrial.Run  == run)][['halfSec','ones']]
        scalingValue3Col = trialByTrial[(trialByTrial.Opt1Type == 2) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['halfSec','OptValue']]
        scalingDifficulty3Col = trialByTrial[(trialByTrial.Opt1Type == 2) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['halfSec','OptValueDiff']]
        
        bundling3Col = trialByTrial[(trialByTrial.Opt1Type == 3) & (trialByTrial.Run  == run)][['halfSec','ones']]
        bundlingValue3Col = trialByTrial[(trialByTrial.Opt1Type == 3) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['halfSec','OptValue']]
        bundlingDifficulty3Col = trialByTrial[(trialByTrial.Opt1Type == 3) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['halfSec','OptValueDiff']]
        
#       De-Mean the parametric pregressors
        controlValue3Col['OptValue'] = controlValue3Col['OptValue'] - controlValue3Col['OptValue'].mean()
        controlDifficulty3Col['OptValueDiff'] = controlDifficulty3Col['OptValueDiff'] - controlDifficulty3Col['OptValueDiff'].mean()

        scalingValue3Col['OptValue'] = scalingValue3Col['OptValue'] - scalingValue3Col['OptValue'].mean()
        scalingDifficulty3Col['OptValueDiff'] = scalingDifficulty3Col['OptValueDiff'] - scalingDifficulty3Col['OptValueDiff'].mean()
        
        bundlingValue3Col['OptValue'] = bundlingValue3Col['OptValue'] - bundlingValue3Col['OptValue'].mean()
        bundlingDifficulty3Col['OptValueDiff'] = bundlingDifficulty3Col['OptValueDiff'] - bundlingDifficulty3Col['OptValueDiff'].mean()
        
#       Name and open the destinations for event files
        controlDir            = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/Control.run00'+ str(run) +'.txt')
        controlValueDir       = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/ControlValue.run00'+ str(run) +'.txt')
        controlDifficultyDir = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/ControlDifficulty.run00'+ str(run) +'.txt')

        scalingDir            = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/Scaling.run00'+ str(run) +'.txt')
        scalingValueDir       = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/ScalingValue.run00'+ str(run) +'.txt')
        scalingDifficultyDir  = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/ScalingDifficulty.run00'+ str(run) +'.txt')

        bundlingDir           = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/Bundling.run00'+ str(run) +'.txt')
        bundlingValueDir      = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/BundlingValue.run00'+ str(run) +'.txt')
        bundlingDifficultyDir = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/BundlingDifficulty.run00'+ str(run) +'.txt')

#       write each 3-column event file as a tab dilimited csv
        control3Col.to_csv(controlDir, sep ='\t', header = False)
        controlValue3Col.to_csv(controlValueDir, sep ='\t', header = False)
        controlDifficulty3Col.to_csv(controlDifficultyDir, sep ='\t', header = False)

        scaling3Col.to_csv(scalingDir, sep ='\t', header = False)
        scalingValue3Col.to_csv(scalingValueDir, sep ='\t', header = False)
        scalingDifficulty3Col.to_csv(scalingDifficultyDir, sep ='\t', header = False)

        bundling3Col.to_csv(bundlingDir, sep ='\t', header = False)
        bundlingValue3Col.to_csv(bundlingValueDir, sep ='\t', header = False)
        bundlingDifficulty3Col.to_csv(bundlingDifficultyDir, sep ='\t', header = False)
#       Be Tidy! Close all of those open files! 
        controlDir.close()
        controlValueDir.close()
        controlDifficultyDir.close()

        scalingDir.close()
        scalingValueDir.close()
        scalingDifficultyDir.close()

        bundlingDir.close()
        bundlingValueDir.close()
        bundlingDifficultyDir.close()


contrasts_dir = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/contrasts.json')

json.dump(Contrasts.contrasts, contrasts_dir)
contrasts_dir.close()

