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
modelName = "Model_002_S_RT"


# subject directories
subject_list = ['SID3301', 'SID3303', 'SID3304', 'SID3306', 'SID3308', 'SID3309', 'SID3310', 'SID3312', 'SID3313', 'SID3314']


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

#    sb.regplot("OptValue", "OptValueDiff", trialByTrial[trialByTrial["Run"]!=0], label= subjectID)
    trialByTrial[trialByTrial["Run"]!=0].plot(kind ="scatter", x = "OptValue", y = "OptValueDiff")

#%% make the event files for each run
    print(subjectID)
    runs = [1,2,3,4,5]
    for run in runs:
#       make the event files for each run seperately.  
#       make the three column format eventfile [onsetTime, Durration, Magnitude]
            # to remove nans, test if a number equals itself
        control3Col = trialByTrial[(trialByTrial.Opt1Type == 1) & (trialByTrial.Run  == run)][['ReactionTime','ones']]
        controlValue3Col = trialByTrial[(trialByTrial.Opt1Type == 1) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['ReactionTime','OptValue']]
        controlDifficulty3Col = trialByTrial[(trialByTrial.Opt1Type == 1) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['ReactionTime','OptValueDiff']]
        controlReactionTime3Col = trialByTrial[(trialByTrial.Opt1Type == 1) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['ReactionTime','ReactionTime']]

        scaling3Col = trialByTrial[(trialByTrial.Opt1Type == 2) & (trialByTrial.Run  == run)][['ReactionTime','ones']]
        scalingValue3Col = trialByTrial[(trialByTrial.Opt1Type == 2) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['ReactionTime','OptValue']]
        scalingDifficulty3Col = trialByTrial[(trialByTrial.Opt1Type == 2) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['ReactionTime','OptValueDiff']]
        scalingReactionTime3Col = trialByTrial[(trialByTrial.Opt1Type == 2) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['ReactionTime','ReactionTime']]

        bundling3Col = trialByTrial[(trialByTrial.Opt1Type == 3) & (trialByTrial.Run  == run)][['ReactionTime','ones']]
        bundlingValue3Col = trialByTrial[(trialByTrial.Opt1Type == 3) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['ReactionTime','OptValue']]
        bundlingDifficulty3Col = trialByTrial[(trialByTrial.Opt1Type == 3) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['ReactionTime','OptValueDiff']]
        bundlingReactionTime3Col = trialByTrial[(trialByTrial.Opt1Type == 3) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['ReactionTime','ReactionTime']]
        
#       De-Mean the parametric pregressors
        controlValue3Col['OptValue'] = controlValue3Col['OptValue'] - controlValue3Col['OptValue'].mean()
        controlDifficulty3Col['OptValueDiff'] = controlDifficulty3Col['OptValueDiff'] - controlDifficulty3Col['OptValueDiff'].mean()
        controlReactionTime3Col['ReactionTime'] = controlReactionTime3Col['ReactionTime'] - controlReactionTime3Col['ReactionTime'].mean()

        scalingValue3Col['OptValue'] = scalingValue3Col['OptValue'] - scalingValue3Col['OptValue'].mean()
        scalingDifficulty3Col['OptValueDiff'] = scalingDifficulty3Col['OptValueDiff'] - scalingDifficulty3Col['OptValueDiff'].mean()
        scalingReactionTime3Col['ReactionTime'] = scalingReactionTime3Col['ReactionTime'] - scalingReactionTime3Col['ReactionTime'].mean()
        
        bundlingValue3Col['OptValue'] = bundlingValue3Col['OptValue'] - bundlingValue3Col['OptValue'].mean()
        bundlingDifficulty3Col['OptValueDiff'] = bundlingDifficulty3Col['OptValueDiff'] - bundlingDifficulty3Col['OptValueDiff'].mean()
        bundlingReactionTime3Col['ReactionTime'] = bundlingReactionTime3Col['ReactionTime'] - bundlingReactionTime3Col['ReactionTime'].mean()

#       Name and open the destinations for event files
        controlDir            = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/Control.run00'+ str(run) +'.txt')
        controlValueDir       = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/ControlValue.run00'+ str(run) +'.txt')
        controlDifficultyDir  = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/ControlDifficulty.run00'+ str(run) +'.txt')
        controlReactionTimeDir= safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/ControlReactionTime.run00'+ str(run) +'.txt')

        scalingDir            = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/Scaling.run00'+ str(run) +'.txt')
        scalingValueDir       = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/ScalingValue.run00'+ str(run) +'.txt')
        scalingDifficultyDir  = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/ScalingDifficulty.run00'+ str(run) +'.txt')
        scalingReactionTimeDir= safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/ScalingReactionTime.run00'+ str(run) +'.txt')

        bundlingDir            = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/Bundling.run00'+ str(run) +'.txt')
        bundlingValueDir       = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/BundlingValue.run00'+ str(run) +'.txt')
        bundlingDifficultyDir  = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/BundlingDifficulty.run00'+ str(run) +'.txt')
        bundlingReactionTimeDir= safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/BundlingReactionTime.run00'+ str(run) +'.txt')

#       write each 3-column event file as a tab dilimited csv
        control3Col.to_csv(controlDir, sep ='\t', header = False)
        controlValue3Col.to_csv(controlValueDir, sep ='\t', header = False)
        controlDifficulty3Col.to_csv(controlDifficultyDir, sep ='\t', header = False)
        controlReactionTime3Col.to_csv(controlReactionTimeDir, sep ='\t', header = False)
        
        scaling3Col.to_csv(scalingDir, sep ='\t', header = False)
        scalingValue3Col.to_csv(scalingValueDir, sep ='\t', header = False)
        scalingDifficulty3Col.to_csv(scalingDifficultyDir, sep ='\t', header = False)
        scalingReactionTime3Col.to_csv(scalingReactionTimeDir, sep ='\t', header = False)

        bundling3Col.to_csv(bundlingDir, sep ='\t', header = False)
        bundlingValue3Col.to_csv(bundlingValueDir, sep ='\t', header = False)
        bundlingDifficulty3Col.to_csv(bundlingDifficultyDir, sep ='\t', header = False)
        bundlingReactionTime3Col.to_csv(bundlingReactionTimeDir, sep ='\t', header = False)
#       Be Tidy! Close all of those open files! 
        controlDir.close()
        controlValueDir.close()
        controlDifficultyDir.close()
        controlReactionTimeDir.close()

        scalingDir.close()
        scalingValueDir.close()
        scalingDifficultyDir.close()
        scalingReactionTimeDir.close()

        bundlingDir.close()
        bundlingValueDir.close()
        bundlingDifficultyDir.close()
        bundlingReactionTimeDir.close()


contrasts_dir = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/contrasts.json')

json.dump(Contrasts.contrasts, contrasts_dir)
contrasts_dir.close()

