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
    data_dir = "/data/"
    fsl_dir = "/usr/share/fsl/5.0"
    CPU_Count = 20

preproc_folder = "PreProcessed/"
models_folder = "Models/"  

event_file_folder = "EventFiles/"
within_subj_results_folder = "FFX_Results/"
between_subj_results_folder = "MFX_Results/"

working_folder = "WorkingDir/"
crash_report_folder = "crashdumps/"

models = ["Model_002_LB"]

# Templates
mfxTemplateBrain        = fsl_dir + '/data/standard/MNI152_T1_2mm.nii.gz'
strippedmfxTemplateBrain= fsl_dir + '/data/standard/MNI152_T1_2mm_brain.nii.gz'
mniConfig               = fsl_dir + '/etc/flirtsch/T1_2_MNI152_2mm.cnf'
mniMask                 = fsl_dir + '/data/standard/MNI152_T1_2mm_brain_mask_dil.nii.gz'

#List of functional scans
func_scan= [1,2,3,4,5]

# subject directories
# subject_list = ['SID3301', 'SID3303', 'SID3304', 'SID3306', 'SID3308', 'SID3309', 'SID3310', 'SID3312', 'SID3313', 'SID3314']
# subject_list = ['SID3301', 'SID3303', 'SID3306', 'SID3309', 'SID3312', 'SID3313', 'SID3314']
subject_list = ['SID3312', 'SID3313']


#ModelSettings
input_units = 'secs'
hpcutoff = 120.
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
             data_dir + '/ROIs/vmPFC.nii.gz',
             # data_dir + '/ROIs/R-dAI.nii',
             # data_dir + '/ROIs/R-PI.nii',
             # data_dir + '/ROIs/R-vAI.nii',
             # data_dir + '/ROIs/L-dAI.nii',
             # data_dir + '/ROIs/L-PI.nii',
             # data_dir + '/ROIs/L-vAI.nii'
             ]


