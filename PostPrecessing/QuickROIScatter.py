# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 09:54:48 2014

@author: Dalton
"""

import os
import nibabel as nib
import numpy as np
import seaborn as sns
import pandas as p

lAGScaling = nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model1/MFX_Results/DLPFC_ROI/_con_3/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..lAG.nii.gz/_DLPFC_ROI0/zstat1_masked.nii.gz')
lIPSScaling = nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model1/MFX_Results/ROIs/_con_1/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..mOFC.nii.gz/_ROIs0/zstat1_masked.nii.gz')
rIPSScaling = nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model1/MFX_Results/DLPFC_ROI/_con_3/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..rIPS.nii.gz/_DLPFC_ROI0/zstat1_masked.nii.gz')
rLingualScaling = nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model1/MFX_Results/DLPFC_ROI/_con_3/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..rLingual.nii.gz/_DLPFC_ROI0/zstat1_masked.nii.gz')

lAGBundling = nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model1/MFX_Results/DLPFC_ROI/_con_4/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..lAG.nii.gz/_DLPFC_ROI0/zstat1_masked.nii.gz')
lIPSBundling = nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model1/MFX_Results/DLPFC_ROI/_con_4/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..lIPS.nii.gz/_DLPFC_ROI0/zstat1_masked.nii.gz')
rIPSBundling = nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model1/MFX_Results/DLPFC_ROI/_con_4/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..rIPS.nii.gz/_DLPFC_ROI0/zstat1_masked.nii.gz')
rLingualBundling = nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model1/MFX_Results/DLPFC_ROI/_con_4/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..rLingual.nii.gz/_DLPFC_ROI0/zstat1_masked.nii.gz')


ROIs = [
        lAGScaling,
        lIPSScaling,
        rIPSScaling,
        rLingualScaling,
        lAGBundling,
        lIPSBundling,
        rIPSBundling,
        rLingualBundling
        ]
        
names = [
        'lAGScaling',
        'lIPSScaling',
        'rIPSScaling',
        'rLingualScaling',
        'lAGBundling',
        'lIPSBundling',
        'rIPSBundling',
        'rLingualBundling'
        ]

df = p.DataFrame(data = {'num':np.zeros(81)})
i=0
for ROI in ROIs:
    
    rawData = ROI.get_data()
    
    # Reshape in to array with only one dimention
    red1 = np.reshape(rawData,-1) 
    
    # Remove Zeros
    nonZeros = red1[red1!=0]
    
    df[names[i]]=nonZeros
    i=i+1



sns.jointplot(df['rIPSScaling'],df['rIPSBundling'])