# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 09:45:39 2016

@author: Dalton
"""

import os
import nibabel as nib

#%% Load
calc= nib.load('/Users/Dalton/Documents/Projects/neurosynth/calculation/calc-sacc/consistency_z_FDR_0.01.nii.gz')
sacc= nib.load('/Users/Dalton/Documents/Projects/neurosynth/calculation/sacc-calc/consistency_z_FDR_0.01.nii.gz')

calc_raw = calc.get_data()
sacc_raw = sacc.get_data()

#%% Combine
fuse_raw = calc_raw - sacc_raw

#%% Saving
affine = calc.affine
fuse_nii = nib.Nifti1Image(fuse_raw, affine)

#savepath = '/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/ROIs/' 
#if not os.path.exists(savepath):
#    os.makedirs(savepath)
    
nib.save(fuse_nii, '/Users/Dalton/Documents/Projects/neurosynth/calculation/fuse.nii.gz')