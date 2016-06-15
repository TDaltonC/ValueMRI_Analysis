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
    CPU_Count = 26

preproc_folder = "PreProcessed/"
models_folder = "Models/"

event_file_folder = "EventFiles/"
within_subj_results_folder = "FFX_Results/"
between_subj_results_folder = "MFX_Results/"

working_folder = "WorkingDir/"
crash_report_folder = "crashdumps/"

models = [
          # "Model_001_MLERank",
          # "Model_001_Rank",
          # "Model_001_Rank_Offset",
          # "Model_001_Rank_Offset_Split",
          # "Model_001_S",
          # "Model_001_S_RT",
          # "Model_001v_MLERank",
          "Model_001v_MLERank_Chosen",
          # "Model_001v_Rank",
          # "Model_001v_S",
          # "Model_001v_S_Chosen",
          # "Model_002_MLERank",
          "Model_002_MLERank_Chosen",
          # "Model_002_MLERank_last500ms",
          # "Model_002_MLERank_Offset",
          # "Model_002_MLERank_Offset_Split",
          # "Model_002_Rank",
          # "Model_002_Rank_Offset",
          # "Model_002_Rank_Offset_ChoiceSplit",
          # "Model_002_Rank_Offset_Split",
          # "Model_002_S",
          # "Model_002_S_last500ms",
          # "Model_002_S_RT",
          # "Model_002d_S",
          # "Model_002RT",
          # "Model_002v_MLERank",
          # "Model_002v_Rank",
          "Model_002v_MLERank_Chosen",
          # "Model_002v_S",
          # "Model_002v_S_Chosen",
          # "Model_003_S",
          # "Model_004_S",
          # "Model_004_MLERank",
          # "Model_004v_MLERank",
          # "Model_004v_S",
          # "Model_008_MLERank",
          # "Model_008_S",
          # "Model_008v_MLERank",
          # "Model_008v_S",
          # "Model_009_MLERank",
          # "Model_009_S",
          # "Model_009v_MLERank",
          # "Model_009v_S",
          # "Model_009v_S",
          "Model_010",
          # "Model_hand_localizer",
          # "Model_001v_MLERank_hand_localizer",
          # "PPI_001_mOFC_Arana",
          # "PPI_001_mOFC_Fitz",
          # "PPI_001_mOFC_Plass",
          # "PPI_001_vmPFC",
          # "PPI_001_vmPFC_big",
          # "PPI_001_vmPFC_Chib",
          # "PPI_001_vmPFC_Combs",
          # "PPI_001_vmPFC_Combs1",
          # "PPI_001_vmPFC_Combs2",
          # "PPI_001_vmPFC_Combs3",
          # "PPI_001_vmPFC_Combs4",
          # "PPI_001_vmPFC_Combs5",
          # "PPI_001_vmPFC_Kahnt",
          # "PPI_001_vmPFC_Kahnt1",
          # "PPI_001_vmPFC_Kahnt2",
          # "PPI_001_vmPFC_Kahnt3",
          # "PPI_001_vmPFC_Kahnt4",
          # "PPI_001_vmPFC_Kahnt5",
          # "PPI_001_vmPFC_Kahnt6",
          # "PPI_001_vmPFC_Kahnt7",
          # "PPI_001_vmPFC_Kahnt8",
          # "PPI_001_vmPFC_Kahnt_anti",
          # "PPI_001_vmPFC_Kim",
          # "PPI_001_vmPFC_Levy",
          # "PPI_001_vmPFC_Lim",
          # "PPI_001_vmPFC_McClure",
          # "PPI_001_vmPFC_ODoher",
          # "PPI_002_mOFC_Arana",
          # "PPI_002_mOFC_Fitz",
          # "PPI_002_mOFC_Plass",
          # "PPI_002_vmPFC",
          # "PPI_002_vmPFC_big",
          # "PPI_002_vmPFC_Chib",
          # "PPI_002_vmPFC_Kahnt",
          # "PPI_002_vmPFC_Kahnt1",
          # "PPI_002_vmPFC_Kahnt_anti",
          # "PPI_002_vmPFC_Kim",
          # "PPI_002_vmPFC_Levy",
          # "PPI_002_vmPFC_Lim",
          # "PPI_002_vmPFC_McClure",
          # "PPI_002_vmPFC_ODoher",
          ]

# Templates
mfxTemplateBrain        = fsl_dir + '/data/standard/MNI152_T1_2mm.nii.gz'
strippedmfxTemplateBrain= fsl_dir + '/data/standard/MNI152_T1_2mm_brain.nii.gz'
mniConfig               = fsl_dir + '/etc/flirtsch/T1_2_MNI152_2mm.cnf'
mniMask                 = fsl_dir + '/data/standard/MNI152_T1_2mm_brain_mask_dil.nii.gz'

#List of functional scans
func_scan= [1,2,3,4,5]

# subject directories
subject_list = [
                'SID3301',
                'SID3303', 
                # 'SID3304', #Duplicate values in the EV files and varcope = 0 errors
                'SID3306', 
                'SID3308', #Cant be used in PPI_002_* or model*_8_MLERank or model*_8_S
                'SID3309', 
                'SID3310', 
                'SID3312', 
                'SID3313', 
                'SID3314',
                'SID3316', 
                'SID3318', #Cant be used in PPI_002_* or model*_8_MLERank or model*_8_S
                'SID3319', 
                'SID3320', #Cant be used in PPI_002_X or model*_8MLERank or model*_8_S
                'SID3321', 
                'SID3325', 
                'SID3326', 
                # 'SID3328', Presses 2 every time
                'SID3329', #Cant be used in model*_8_MLERank
                'SID3330', 
                'SID3331', 
                'SID3332', #Cant be used in PPI_002_X or model*_8_MLERank or model*_8_S
                'SID3333', 
                'SID3334', 
                'SID3335', 
                'SID3336'
                ]
# subject_list = ['SID3301', 'SID3303', 'SID3306', 'SID3309', 'SID3312', 'SID3313', 'SID3314']
# subject_list = ['SID3335']



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
    


#ModelSettings
input_units = 'secs'
hpcutoff = 120.
TR = 2.

# ROI Masks
ROI_Masks = [
             # data_dir + '/ROIs/HOMiddleFrontalGyrus.nii.gz',
             # data_dir + '/ROIs/lAG.nii.gz',
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


