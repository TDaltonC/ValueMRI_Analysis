# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 09:54:48 2014

@author: Dalton
"""

import os
import nibabel as nib
import numpy as np
import seaborn as sns

ROI = nib.load('/Users/Dalton/Documents/Projects/ValuePilot/Workflows/WholeBrainGLM/Model_Complex1/MFX_Results/DLPFC_ROI/_con_1/_DLPFC_ROI0/zstat1_masked.nii.gz')

rawData = ROI.get_data()

# Reshape in to array with only one dimention
red1 = np.reshape(rawData,-1) 

# Remove Zeros
nonZeros = red1[red1!=0]

sns.kdeplot(nonZeros)