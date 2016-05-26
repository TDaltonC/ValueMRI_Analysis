# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 09:45:39 2016

@author: Dalton
"""

import os
import nibabel as nib

#%% Load
l_fp_net_nii= nib.load('/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/ROIs/lFPnet.nii.gz')
r_fp_net_nii= nib.load('/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/ROIs/rFPnet.nii.gz')

l_fp_net_raw = l_fp_net_nii.get_data()
r_fp_net_raw = r_fp_net_nii.get_data()

#%% Combine
fp_net_raw = l_fp_net_raw + r_fp_net_raw

#%% Saving
affine = l_fp_net_nii.affine
fp_net_nii = nib.Nifti1Image(fp_net_raw, affine)

#savepath = '/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/ROIs/' 
#if not os.path.exists(savepath):
#    os.makedirs(savepath)
    
nib.save(fp_net_nii, '/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/ROIs/FPnet.nii.gz')