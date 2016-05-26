# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 08:57:30 2016

@author: Dalton
"""

import os
import nibabel as nib
import numpy as np
import seaborn as sns

#%% Load data
model = 'Model_002v_MLERank'
critical_value = 0.8 # for p = .01
#critical_value = 1.314 # for p = .001

control_nii= nib.load('/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/Models/' + model + '/MFX_Results/tstats/_con_3/contrast0/tstat1.nii.gz')
scaling_nii= nib.load('/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/Models/' + model + '/MFX_Results/tstats/_con_4/contrast0/tstat1.nii.gz')
bundling_nii=nib.load('/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/Models/' + model + '/MFX_Results/tstats/_con_5/contrast0/tstat1.nii.gz')
control_raw = control_nii.get_data()
scaling_raw = scaling_nii.get_data()
bundling_raw= bundling_nii.get_data()

#%% Thresholding

#Threshold each of the images at the critical t-stat (0 if below, 1 if above)
control_raw[control_raw >= critical_value] = 1 
scaling_raw[scaling_raw >= critical_value] = 1 
bundling_raw[bundling_raw >= critical_value] = 1 

#%% Conjoining 

conjoined_raw = control_raw.copy()
conjoined_raw[:,:,:] = 0
conjoined_raw[(control_raw == 1) & (scaling_raw == 1) & (bundling_raw == 1)] = 1

#Set each voxel in a new image = to 1 if that same voxel in all other images == 1


#%% Saving
affine = control_nii.affine
conjoined_nii = nib.Nifti1Image(conjoined_raw, affine)

savepath = '/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/Models/' + model + '/MFX_Results/valueConjunction' 
if not os.path.exists(savepath):
    os.makedirs(savepath)
    
nib.save(conjoined_nii, '/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/Models/' + model + '/MFX_Results/valueConjunction/tstat1.nii.gz')