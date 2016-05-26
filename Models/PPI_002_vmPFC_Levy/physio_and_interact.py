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
import nipype.interfaces.fsl as fsl # fsl
import glob # for using wildcards in file paths

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
modelName = "PPI_002_vmPFC_Levy"
ROI_seed  = 'vmPFC_Levy'

# subject directories
subject_list = [
                'SID3301', 'SID3303', 'SID3304', 'SID3306', 
                # 'SID3308',
                'SID3309', 'SID3310', 'SID3312', 'SID3313', 'SID3314',
                'SID3316', 
                # 'SID3318', 
                'SID3319', 
                # 'SID3320', 
                'SID3321', 'SID3325', 'SID3326', 'SID3328', 'SID3329', 'SID3330', 'SID3331', 
                #'SID3332', 
                'SID3333', 'SID3334', 'SID3335', 'SID3336'
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
    print(subjectID)
    runs = [1,2,3,4,5]
    for run in runs:

        """
        ========================
        Physiological Regressors
        ========================
        """ 
        # Get the spatially average time series within an ROI
        single_time_series = fsl.ImageMeants()
        single_time_series.inputs.in_file = glob.glob(data_dir + "/PreProcessed/" + subjectID + "/func2MNI/out_file/_subject_id_" + subjectID + "/_func2MNI" + str(run-1)  + "/Scan*")[0]
        single_time_series.inputs.out_file = data_dir + '/Models/' + modelName + '/TS/' + subjectID + '/RUN' + str(run) + '.csv'
        single_time_series.inputs.mask = data_dir + '/ROIs/' + ROI_seed + '.nii.gz'
        single_time_series.inputs.eig= True
        # Create the destination directory
        if not os.path.exists(data_dir + '/Models/' + modelName + '/TS/' + subjectID):
            os.makedirs(data_dir + '/Models/' + modelName + '/TS/' + subjectID)        
        single_time_series.run()
        # Load masked ROI from functional scan
        ROI_TS = np.genfromtxt(data_dir + '/Models/' + modelName + '/TS/' + subjectID + '/RUN' + str(run) + '.csv')
        # save physiological regressor        
        physio3col = np.transpose(np.array([np.arange(len(ROI_TS)), np.ones(len(ROI_TS)), ROI_TS]))
        physio_dir  =      safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/Physio.run00'+ str(run) +'.txt')
        np.savetxt(physio_dir, physio3col, fmt = '%10.9f')
        physio_dir.close()
        """
        ======================
        Interaction Regressors
        ======================
        """ 
        for task_ev in ["Control", "Scaling_1IS", "Scaling_CV", "Bundling_1IS", "Bundling_CV"]:
    #       Open the convolved task EV files
            task_from_comvolve = np.genfromtxt(data_dir + "/Models/" + modelName + "/convolved/" + subjectID + "/RUN" + str(run) + "/" + task_ev + ".run00" + str(run) + ".txt.xmat.1D")
            task_reg = task_from_comvolve[:, 2]
    #       Compute the interactions bwtween the convolved ev and the physiological reg
            connectivity = ROI_TS * task_reg
    #       Consruct 3 col version of the event file
            task_reg3col = np.transpose(np.array([np.arange(len(task_reg)), np.ones(len(task_reg)), task_reg]))
            connectivity3col = np.transpose(np.array([np.arange(len(connectivity)), np.ones(len(connectivity)), connectivity]))
    #       write the event file to a folder in the right place
            #       Name and open the destinations for event files
            task_reg_dir = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/' + task_ev + '.run00'+ str(run) +'.txt')
            connectivity_dir = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/' + subjectID + '/RUN' + str(run) + '/' + task_ev + '_connectivity.run00'+ str(run) +'.txt')    
    ##       write each 3-column event file as a tab dilimited csv
            np.savetxt(task_reg_dir, task_reg3col, fmt = '%10.9f')
            np.savetxt(connectivity_dir, connectivity3col, fmt = '%10.9f')
    #       Be Tidy! Close all of those open files! 
            task_reg_dir.close()
            connectivity_dir.close()
        
contrasts_dir = safe_open_w(data_dir + '/Models/' + modelName + '/EventFiles/contrasts.json')
Contrasts.contrasts
json.dump(Contrasts.contrasts, contrasts_dir)
contrasts_dir.close()
