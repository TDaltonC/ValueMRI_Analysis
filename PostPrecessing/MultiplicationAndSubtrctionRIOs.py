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
import scipy as sp

ROIsMult = []
ROIsSub = []
multNet = []
subNet  = []
model = "Model_Complex8"
contrast = "_con_5" # Bundling>Scaling

# Add all of the ROIs you want to plot to the ROIs list

#Multiplcation > Subtraction
ROIsMult.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/'+ model + '/MFX_Results/ROIs/' + contrast + '/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..lAG.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
#ROIsMult.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/'+ model + '/MFX_Results/ROIs/' + contrast + '/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..lSFG1.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
ROIsMult.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/'+ model + '/MFX_Results/ROIs/' + contrast + '/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..rLingual.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
#ROIsMult.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/'+ model + '/MFX_Results/ROIs/' + contrast + '/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..rPCG.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
#ROIsMult.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/'+ model + '/MFX_Results/ROIs/' + contrast + '/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..ACC.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
#ROIsMult.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/'+ model + '/MFX_Results/ROIs/' + contrast + '/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..Perc.nii.gz/_ROIs0/zstat1_masked.nii.gz'))

#Subtraction > Multiplcation
ROIsSub.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/'+ model + '/MFX_Results/ROIs/' + contrast + '/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..lIPS.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
#ROIsSub.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/'+ model + '/MFX_Results/ROIs/' + contrast + '/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..lSFG2.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
#ROIsSub.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/'+ model + '/MFX_Results/ROIs/' + contrast + '/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..lIFG.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
ROIsSub.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/'+ model + '/MFX_Results/ROIs/' + contrast + '/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..lpITG.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
ROIsSub.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/'+ model + '/MFX_Results/ROIs/' + contrast + '/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..rIPS.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
#ROIsSub.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/'+ model + '/MFX_Results/ROIs/' + contrast + '/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..rSFG.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
#ROIsSub.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/'+ model + '/MFX_Results/ROIs/' + contrast + '/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..rIFG.nii.gz/_ROIs0/zstat1_masked.nii.gz'))
ROIsSub.append(nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/'+ model + '/MFX_Results/ROIs/' + contrast + '/_mask_file_..Users..Dalton..Documents..Projects..ValuePilot..Workflows..WholeBrainGLM..ROIs..rpITG.nii.gz/_ROIs0/zstat1_masked.nii.gz'))

df = p.DataFrame(data = {'num':np.zeros(81)})
i=0
for ROI in ROIsMult:
    
    rawData = ROI.get_data()
    
    # Reshape in to array with only one dimention
    red1 = np.reshape(rawData,-1) 
    
    # Remove Zeros
    nonZeros = red1[red1!=0]
    
    #add to DF
    df[str(i)]=nonZeros
    i=i+1
    sns.kdeplot(nonZeros, color = "red")
    
for ROI in ROIsSub:
    
    rawData = ROI.get_data()
    
    # Reshape in to array with only one dimention
    red1 = np.reshape(rawData,-1) 
    
    # Remove Zeros
    nonZeros = red1[red1!=0]
        
            
    #add to DF
    df[str(i)]=nonZeros
    i=i+1
    
    sns.kdeplot(nonZeros, color = "yellow")
    
sp.stats.ttest_ind(df['0'], df['1'], equal_var=False)