# -*- coding: utf-8 -*-
"""
Created on JAN 1 2016

@author: Dalton
"""

"""
=========
Imports
=========
"""
import os
import errno
import numpy as np
import json
import Contrasts
import subprocess
import glob # for using wildcards in file paths
import pandas 

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
modelName = "PPI_001_vmPFC_Kahnt6"


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

"""
==============
MEAT & POTATOS
==============
""" 
for subjectID in subject_list:
    # load the trial by trial data for this subject
    trialByTrial = pandas.DataFrame.from_csv(data_dir + '/RawData/' + subjectID + '/DataFrames/trialByTrial.csv', index_col = 'OnsetTime')

    # Add a column of ones to the dataframe (this is usefull for creating the three column files)        
    trialByTrial['ones'] = 1
    
    print(subjectID)

    runs = [1,2,3,4,5]
    for run in runs:
    # """
    # ===================
    # Sub-Task Regressors
    # ===================
    # """
#       make the event files for each run seperately.  
#       make the three column format eventfile [onsetTime, Durration, Magnitude]
        control3Col = trialByTrial[(trialByTrial.Opt1Type == 1) & (trialByTrial.Run  == run)][['ReactionTime','ones']]
        scaling3Col = trialByTrial[(trialByTrial.Opt1Type == 2) & (trialByTrial.Run  == run)][['ReactionTime','ones']]
        bundling3Col= trialByTrial[(trialByTrial.Opt1Type == 3) & (trialByTrial.Run  == run)][['ReactionTime','ones']]
        
#       Name and open the destinations for event files
        controlDir  =    safe_open_w(data_dir + '/Models/' + modelName + '/PreEventFiles/' + subjectID + '/RUN' + str(run) + '/Control.run00'+ str(run) +'.txt')
        scalingDir  =    safe_open_w(data_dir + '/Models/' + modelName + '/PreEventFiles/' + subjectID + '/RUN' + str(run) + '/Scaling.run00'+ str(run) +'.txt')
        BundlingDir =    safe_open_w(data_dir + '/Models/' + modelName + '/PreEventFiles/' + subjectID + '/RUN' + str(run) + '/Bundling.run00'+ str(run) +'.txt')

#       write each 3-column event file as a tab dilimited csv
        control3Col.to_csv(controlDir, sep ='\t', header = False)
        scaling3Col.to_csv(scalingDir, sep ='\t', header = False)
        bundling3Col.to_csv(BundlingDir, sep ='\t', header = False)
#       Be Tidy! Close all of those open files!
        controlDir.close()
        scalingDir.close()
        BundlingDir.close()
#       Convolve the event files with the HDR
        for pre_event_file in ["Control", "Scaling", "Bundling"]:
        # Create the convolved directory if it doesn't exist
            if not os.path.exists(data_dir + "/Models/" + modelName + "/convolved/" + subjectID + "/RUN" + str(run) + "/" + pre_event_file):
                os.makedirs(data_dir + "/Models/" + modelName + "/convolved/" + subjectID + "/RUN" + str(run) + "/" + pre_event_file)
        # Run the convolution
            p = subprocess.Popen(
                [
                    "/usr/lib/afni/bin/3dDeconvolve",
                    "-nodata", "167", "2",
                    "-num_stimts", "1",
                    "-stim_times_FSL", "1", data_dir + "/Models/" + modelName + "/PreEventFiles/" + subjectID + "/RUN" + str(run) + "/" + pre_event_file + ".run00" + str(run) + ".txt", "dmBLOCK",
                    "-x1D", data_dir + "/Models/" + modelName + "/convolved/" + subjectID + "/RUN" + str(run) + "/" + pre_event_file + ".run00" + str(run) + ".txt"],
                stdout=subprocess.PIPE)
            output, err = p.communicate()
            print(output)
#       Open the saved convolved matrix files

#       Save the regresor as a 3 column file

        
contrasts_dir = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/contrasts.json')
Contrasts.contrasts
json.dump(Contrasts.contrasts, contrasts_dir)
contrasts_dir.close()
