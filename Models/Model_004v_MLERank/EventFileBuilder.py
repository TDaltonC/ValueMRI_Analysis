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
from scipy import stats
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
modelName = "Model_004v_MLERank"


# subject directories
subject_list = [
                'SID3301', 'SID3303', 'SID3304', 'SID3306', 'SID3308', 'SID3309', 'SID3310', 'SID3312', 'SID3313', 'SID3314',
                'SID3316', 'SID3318', 'SID3319', 'SID3320', 'SID3321', 'SID3325', 'SID3326', 'SID3328', 'SID3329', 'SID3330', 'SID3331', 'SID3332', 'SID3333', 'SID3334', 'SID3335', 'SID3336'
                ]

# System Setting (Local(MAC) or Remote(linux))
#system = "Darwin" # Mac
system = "Linux"
if system == "Darwin":
    data_dir = "/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data"
    fsl_dir = "/usr/local/fsl"
elif system == "Linux":
    data_dir = "/data"
    fsl_dir = "/usr/share/fsl/5.0"

def nan_filler(row):
    if row.type == 1:
        if row.MLE_Rank == row.MLE_Rank: #nan does not equal itself
            return row.MLE_Rank
        else:
            return row.est_value
    else:
        return row.MLE_Rank

"""
==============
MEAT & POTATOS
==============
""" 

# Value max/min
# If the value of the Item1, Item2 or the combined-option is more than the control option
# The subjects will consider the lease valuable of those three
# If the value of the Item1, Item2, and the combined option are all less than the control option
# The subject will onlt consider the most valuable. 
def valueBuilder(row):
    if np.nanmax([row.Item1Value, row.Item2Value]) > row.FixedValue:
        return np.nanmax([row.Item1Value, row.Item2Value])
    else:
        return row.ComOptValue


for subjectID in subject_list:
#   load the trial by trial data for this subject
    trialByTrial = pandas.DataFrame.from_csv(data_dir + '/RawData/' + subjectID + '/DataFrames/trialByTrial.csv', index_col = 'OnsetTime')
    optionValues = pandas.DataFrame.from_csv(data_dir + '/RawData/' + subjectID + '/DataFrames/optionValue.csv')
    optionValues.reset_index(inplace=True)
    optionValues.set_index('rank', drop=False, inplace=True)
    # slect Value model
    # Fill in the missing values for singleton options
    # remove the nans
    optionValues.sort('MLEValueS', inplace = True, ascending = False)
    optionValues['MLE_Rank'] = np.linspace(1, -1, optionValues.shape[0])
    regressable = optionValues[(optionValues['MLE_Rank'] == optionValues['MLE_Rank']) & (optionValues['type'] == 1)]
    # compute a regression
    model_solution = stats.linregress(regressable[['rank', 'MLE_Rank']])
    
    optionValues['est_value'] = (model_solution.slope * optionValues['rank']) + model_solution.intercept
    
    optionValues['final_value'] = optionValues.apply(nan_filler, 1)
    
    # Join the data frames
    #join trialbytrial and optionvalue on option number so that trailbytrial now has a column for value
    # Which value model should be used?
    values1 = optionValues[['final_value']]
    # add the value for the screen option
    values1.columns = ['ComOptValue']
    trialByTrial = trialByTrial.merge(values1, how = 'left', left_on = 'Opt1Code', right_index = True)
    # add the value for the fixed option
    values1.columns = ['FixedValue']
    trialByTrial = trialByTrial.merge(values1, how = 'left', left_on = 'Opt2Code', right_index = True)
    
    # add columns for the value of Item 1 and the value of Item2
    singleItemOptionValues = optionValues[optionValues['item2']==0]
    singleItemValues = singleItemOptionValues[['item1', 'final_value']]
    # add the value for the first item of the onscreen option
    singleItemValues.columns = ['Opt1Item1', 'Item1Value']
    trialByTrial = trialByTrial.reset_index().merge(singleItemValues, how = 'left', left_on = 'Opt1Item1', right_on = 'Opt1Item1', sort=False).set_index('OnsetTime')
    # add the value for the second item of the onscreen option
    singleItemValues.columns = ['Opt1Item2', 'Item2Value']
    trialByTrial = trialByTrial.reset_index().merge(singleItemValues, how = 'left', left_on = 'Opt1Item2', right_on = 'Opt1Item2', sort=False).set_index('OnsetTime')
    
    trialByTrial['OptValue'] = trialByTrial.apply(valueBuilder, axis = 1)
    
    # Add a column of ones to the dataframe (this is usefull for creating the three column files)        
    trialByTrial['ones'] = 1
    
    # Create the diff column
    # subtract the control option value from the value vector to make a vector for diff
    trialByTrial['OptValueDiff'] = abs(trialByTrial['OptValue'] - trialByTrial['FixedValue'])

#%% make the event files for each run
    print(subjectID)
    runs = [1,2,3,4,5]
    for run in runs:
#       make the event files for each run seperately.  
#       make the three column format eventfile [onsetTime, Durration, Magnitude]
            # to remove nans, test if a number equals itself
        control3Col = trialByTrial[(trialByTrial.Opt1Type == 1) & (trialByTrial.Run  == run)][['ReactionTime','ones']]
        controlValue3Col = trialByTrial[(trialByTrial.Opt1Type == 1) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['ReactionTime','OptValue']]
        
        scaling3Col = trialByTrial[(trialByTrial.Opt1Type == 2) & (trialByTrial.Run  == run)][['ReactionTime','ones']]
        scalingValue3Col = trialByTrial[(trialByTrial.Opt1Type == 2) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['ReactionTime','OptValue']]
        
        bundling3Col = trialByTrial[(trialByTrial.Opt1Type == 3) & (trialByTrial.Run  == run)][['ReactionTime','ones']]
        bundlingValue3Col = trialByTrial[(trialByTrial.Opt1Type == 3) & (trialByTrial.Run  == run) & (trialByTrial.OptValue  == trialByTrial.OptValue)][['ReactionTime','OptValue']]

#       De-Mean the parametric pregressors
        controlValue3Col['OptValue'] = controlValue3Col['OptValue'] - controlValue3Col['OptValue'].mean()

        scalingValue3Col['OptValue'] = scalingValue3Col['OptValue'] - scalingValue3Col['OptValue'].mean()
        
        bundlingValue3Col['OptValue'] = bundlingValue3Col['OptValue'] - bundlingValue3Col['OptValue'].mean()
        

#       Name and open the destinations for event files
        controlDir            = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/Control.run00'+ str(run) +'.txt')
        controlValueDir       = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/ControlValue.run00'+ str(run) +'.txt')

        scalingDir            = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/Scaling.run00'+ str(run) +'.txt')
        scalingValueDir       = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/ScalingValue.run00'+ str(run) +'.txt')

        bundlingDir           = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/Bundling.run00'+ str(run) +'.txt')
        bundlingValueDir      = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/BundlingValue.run00'+ str(run) +'.txt')

#       write each 3-column event file as a tab dilimited csv
        control3Col.to_csv(controlDir, sep ='\t', header = False)
        controlValue3Col.to_csv(controlValueDir, sep ='\t', header = False)

        scaling3Col.to_csv(scalingDir, sep ='\t', header = False)
        scalingValue3Col.to_csv(scalingValueDir, sep ='\t', header = False)

        bundling3Col.to_csv(bundlingDir, sep ='\t', header = False)
        bundlingValue3Col.to_csv(bundlingValueDir, sep ='\t', header = False)
#       Be Tidy! Close all of those open files! 
        controlDir.close()
        controlValueDir.close()

        scalingDir.close()
        scalingValueDir.close()

        bundlingDir.close()
        bundlingValueDir.close()


contrasts_dir = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/contrasts.json')
Contrasts.contrasts
json.dump(Contrasts.contrasts, contrasts_dir)
contrasts_dir.close()
