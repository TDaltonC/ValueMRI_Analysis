# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 09:47:11 2016

@author: Dalton
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 08:57:30 2016

@author: Dalton
"""

import os
import nibabel as nib
import numpy as np
import seaborn as sb
import scipy.stats as stats
import matplotlib.pyplot as plt
import random
#%% Config
HO_frontal = [1, 25, 29, 8]
HO_mid_post= [30, 31, 32, 47, 24]
HO_lat_post= [22]
#%% Load data
model = 'Model_001v_MLERank'
contrast = '10'

#stat = 'raw_t_stat'
stat = 'raw_z_stat'
#stat = 'thresh_z_stat'
#stat = 'p_corr_t_stat'

dm_net_nii  = nib.load('/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/ROIs/DMnet.nii.gz')
fp_net_nii= nib.load('/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/ROIs/FPnet.nii.gz')

HO_nii = nib.load('/usr/local/fsl/data/atlases/HarvardOxford/HarvardOxford-cort-maxprob-thr0-2mm.nii.gz')

if stat == 'raw_t_stat':
    test_con_nii= nib.load('/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/Models/' + model + '/MFX_Results/tstats/_con_' + contrast + '/contrast0/tstat1.nii.gz')
elif stat == 'raw_z_stat':
    test_con_nii= nib.load('/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/Models/' + model + '/MFX_Results/zstats/_con_' + contrast + '/contrast0/zstat1.nii.gz')
elif stat == 'thresh_z_stat':
    test_con_nii= nib.load('/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/Models/' + model + '/MFX_Results/thresholdedCombined/_con_' + contrast + '/_thresholdCombined0/zstat1_thresh_maths.nii.gz')
elif stat == 'p_corr_t_stat':
    test_con_nii= nib.load('/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/Models/' + model + '/MFX_Results/t_corrected_p_files/_con_' + contrast + '/tbss__tfce_corrp_tstat1.nii.gz')

dm_net_raw = dm_net_nii.get_data()
fp_net_raw = fp_net_nii.get_data()

HO_raw= HO_nii.get_data()

test_con_raw= test_con_nii.get_data()

#%% reshape
dm_net_1d = np.reshape(dm_net_raw,-1) 
fp_net_1d = np.reshape(fp_net_raw,-1)

HO_1d = np.reshape(HO_raw,-1)

test_con_1d = np.reshape(test_con_raw,-1)

#%% Combine 

opposition_1d = dm_net_1d - fp_net_1d

#%% Trimm
#For non-zero voxels
trim_rule = (fp_net_1d != 0)&(test_con_1d!=0)
# For Non-zero voxels in a hot spot
#trim_rule = (dm_net_1d > 3)&(test_con_1d!=0)&(np.in1d(HO_1d, HO_frontal))
# For non-zero voxels outside of a hotspot
#trim_rule = (dm_net_1d < 3)&(dm_net_1d != 0)&(test_con_1d!=0)&(np.in1d(HO_1d, HO_lat_post, invert = True))

dm_net_1d_trimmed = dm_net_1d[trim_rule]
fp_net_1d_trimmed = fp_net_1d[trim_rule]
opposition_1d_trimmed = opposition_1d[trim_rule]

test_con_1d_trimmed = test_con_1d[trim_rule]

#%% Choose what to use
x = dm_net_1d_trimmed
y = test_con_1d_trimmed

#%% plot
try:    
    Random_sample = random.sample(range(0, x.size), x.size/10)
except:
    Random_sample = range(0, x.size)

fig1 = plt.figure()
dots = sb.regplot(x[Random_sample], y[Random_sample])
dots.axes.set_ylim(-6,6)
dots.axes.set_xlim(-5,15)
topo = sb.kdeplot(x[Random_sample], y[Random_sample])
#topo.axes.set_ylim(-6,4)
#topo.axes.set_xlim(-5,15)

fig1.savefig('/Users/Dalton/Documents/Projects/BundledOptionsExp/Summary/Figures/DM_corr.pdf', format =  'pdf')

#%% Corr starts

print(stats.pearsonr(x, y))
#%% print bash command

#This prints a string that can br paised in to a terminal to get a pearsons rho form FSL 

dm_net_str = '/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/ROIs/DMnet.nii.gz'
fp_net_str = '/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/ROIs/FPnet.nii.gz'

if stat == 'raw_t_stat':
    test_str = '/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/Models/' + model + '/MFX_Results/tstats/_con_' + contrast + '/contrast0/tstat1.nii.gz'
elif stat == 'raw_z_stat':
    test_str = '/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/Models/' + model + '/MFX_Results/zstats/_con_' + contrast + '/contrast0/zstat1.nii.gz'
elif stat == 'thresh_z_stat':
    test_str = '/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/Models/' + model + '/MFX_Results/thresholdedCombined/_con_' + contrast + '/_thresholdCombined0/zstat1_thresh_maths.nii.gz'
elif stat == 'p_corr_t_stat':
    test_str = '/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/Models/' + model + '/MFX_Results/t_corrected_p_files/_con_' + contrast + '/tbss__tfce_corrp_tstat1.nii.gz'

output_str = '/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/temp/fslcc_output.txt'

command = "fslcc " + dm_net_str + ' ' + test_str + ' >> ' + output_str

print (command)
