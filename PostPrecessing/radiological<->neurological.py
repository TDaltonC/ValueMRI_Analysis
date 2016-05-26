# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 11:57:10 2016

@author: Dalton
"""

import os
import nibabel as nib
import numpy as np

# flip a MRI image from research to medical coordinates or vise versa. 

img_str = '/Users/Dalton/Documents/Projects/neurosynth/calculation/sacc-calc/consistency_z_FDR_0.01.nii.gz'

image_nii=nib.load(img_str)
#make the top row of the affine matrix neagive
image_nii.affine[0] = -image_nii.affine[0] 
#image_nii.affine[::] = newaffine
#Multiply by [-1,1,1,1]

#image_nii.affine = np.diag((-x,y,z,1))

nib.save(image_nii, img_str)