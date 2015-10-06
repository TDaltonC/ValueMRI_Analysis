# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 14:06:38 2014

@author: Dalton
"""

"""
=========
Imports
=========
"""
import os                                    # system functions

import nipype.interfaces.fsl as fsl          # fsl

"""
==============
Configurations
==============
"""
# for calcualting core-count
# CPU_Count = 2

#set output file format to compressed NIFTI.
fsl.FSLCommand.set_default_output_type('NIFTI_GZ')


# System Setting (Local(MAC) or Remote(linux))
# system = "Darwin" # Mac
system = "Linux"
if system == "Darwin":
    data_dir = "/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data"
    fsl_dir = "/usr/local/fsl"
    CPU_Count = 2
elif system == "Linux":
    data_dir = "/vol"
    fsl_dir = "/usr/share/fsl/5.0"
    CPU_Count = 16

# Paths
def configPaths(modelName = "PreProcessing",data_dir = data_dir):

    # Wthere the input data comes from
    preProcDir =               data_dir + "/PreProcessed"
    ev_dir     =               data_dir + "/Models/" + modelName + "/EventFiles"
    # Where the outputs goes
    withinSubjectResults_dir = data_dir + "/Models/" + modelName + "/FFX_Results"
    betweenSubjectResults_dir= data_dir + "/Models/" + modelName + "/MFX_Results"
    # Working Directory
    workingdir =               data_dir + "/WorkingDir/" + modelName
    # Crash Records
    crashRecordsDir =          workingdir + "/crashdumps"
    return data_dir, preProcDir, ev_dir, withinSubjectResults_dir, betweenSubjectResults_dir, workingdir,crashRecordsDir
    

# Templates
mfxTemplateBrain        = fsl_dir + '/data/standard/MNI152_T1_2mm.nii.gz'
strippedmfxTemplateBrain= fsl_dir + '/data/standard/MNI152_T1_2mm_brain.nii.gz'
mniConfig               = fsl_dir + '/etc/flirtsch/T1_2_MNI152_2mm.cnf'
mniMask                 = fsl_dir + '/data/standard/MNI152_T1_2mm_brain_mask_dil.nii.gz'

#List of functional scans
func_scan= [1,2,3,4,5]

# subject directories
subject_list = ['SID3301', 'SID3303', 'SID3304', 'SID3306', 'SID3308', 'SID3309', 'SID3310']

#ModelSettings
input_units = 'secs'
hpcutoff = 120
TR = 2.

# ROI Masks
ROI_Masks = [data_dir + '/ROIs/HOMiddleFrontalGyrus.nii.gz',
             data_dir + '/ROIs/lAG.nii.gz',
             data_dir + '/ROIs/lIPS.nii.gz',
             data_dir + '/ROIs/rIPS.nii.gz',
             data_dir + '/ROIs/rLingual.nii.gz',
             data_dir + '/ROIs/ACC.nii.gz',
             data_dir + '/ROIs/lIFG.nii.gz',
             data_dir + '/ROIs/lpITG.nii.gz',
             data_dir + '/ROIs/lSFG1.nii.gz',
             data_dir + '/ROIs/lSFG2.nii.gz',
             data_dir + '/ROIs/mOFC.nii.gz',
             data_dir + '/ROIs/Perc.nii.gz',
             data_dir + '/ROIs/rIFG.nii.gz',
             data_dir + '/ROIs/rPCG.nii.gz',
             data_dir + '/ROIs/rpITG.nii.gz',
             data_dir + '/ROIs/rSFG.nii.gz',
             data_dir + '/ROIs/vmPFC.nii.gz']


