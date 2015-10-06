# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 09:54:48 2014

@author: Dalton
"""

import os
import nibabel as nib
import numpy as np
import seaborn as sns

ROIs = []


# Add all of the ROIs you want to plot to the ROIs list
ROIs.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model0/MFX_Results/ROIs/_con_1/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..mOFC.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
ROIs.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model1/MFX_Results/ROIs/_con_1/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..mOFC.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
ROIs.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model3/MFX_Results/ROIs/_con_1/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..mOFC.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
ROIs.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model5/MFX_Results/ROIs/_con_1/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..mOFC.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
ROIs.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model6/MFX_Results/ROIs/_con_1/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..mOFC.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
#ROIs.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model6exp/MFX_Results/ROIs/_con_1/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..mOFC.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
ROIs.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model7/MFX_Results/ROIs/_con_1/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..mOFC.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
ROIs.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model8/MFX_Results/ROIs/_con_1/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..mOFC.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
#ROIs.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model8exp/MFX_Results/ROIs/_con_1/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..mOFC.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
#ROIs.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model8ln/MFX_Results/ROIs/_con_1/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..mOFC.nii.gz/_ROIs0/zstat1_masked.nii.gz'))


for ROI in ROIs:
    
    rawData = ROI.get_data()
    
    # Reshape in to array with only one dimention
    red1 = np.reshape(rawData,-1) 
    
    # Remove Zeros
    nonZeros = red1[red1!=0]
        
    
    sns.kdeplot(nonZeros)