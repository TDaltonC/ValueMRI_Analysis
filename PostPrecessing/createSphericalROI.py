# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 13:33:04 2014

@author: Dalton
"""

import os                                    # Operating system Functions
import nipype.interfaces.fsl as fsl          # fsl
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
import nipype.interfaces.io as nio           # Data i/o

from nipype import config
config.enable_debug_mode()

# System Setting (Local(MAC) or Remote(linux))
system = "Darwin" # Mac
# system = "Linux"
if system == "Darwin":
    data_dir = "/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data"
    fsl_dir = "/usr/local/fsl"
    CPU_Count = 2
elif system == "Linux":
    data_dir = "/data/"
    fsl_dir = "/usr/share/fsl/5.0"
    CPU_Count = 20


TemplateBrain = '/usr/local/fsl/data/standard/MNI152_T1_2mm.nii.gz'
ROIDir        = data_dir + '/ROIs/'
workingdir    = data_dir + '/WorkingDir/ROIs'

ROIs = []
## left border area between angular gyrus and supramarginal gyrus from table 2 Lee(2000)
#ROIs.append('-add 1 -roi 71 1 36 1 54 1 0 1')
# #
# # Left Superior frontal gyrus[1] from table 2 Lee(2000)
# ROIs.append('-add 1 -roi 57 1 83 1 56 1 0 1')
# #
# ## Right lingual Gyrus from table 2 Lee(2000)
# #ROIs.append('-add 1 -roi 38 1 24 1 40 1 0 1')
# #
# # Right Precentral gyrus from table 2 Lee(2000)
# ROIs.append('-add 1 -roi 16 1 60 1 46 1 0 1')
# #
# # Anterior cingulate gyrus from table 2 Lee(2000)
# ROIs.append('-add 1 -roi 43 1 91 1 39 1 0 1')
# #
# # Precuneus from table 2 Lee(2000)
# ROIs.append('-add 1 -roi 46 1 42 1 63 1 0 1')
# #
# ## Left interParietal Sulcus from table 2 Lee(2000)
# #ROIs.append('-add 1 -roi 61 1 38 1 64 1 0 1')
# #
# # Left Superior frontal gyrus [2]from table 2 Lee(2000)
# ROIs.append('-add 1 -roi 57 1 67 1 65 1 0 1')
# #
# # Left Inferior frontal gyrus from table 2 Lee(2000)
# ROIs.append('-add 1 -roi 69 1 70 1 50 1 0 1')
# #
# # Left Posterior ITG from table 2 Lee(2000)
# ROIs.append('-add 1 -roi 74 1 32 1 32 1 0 1')
# #
# ## Right interParietal Sulcus from table 2 Lee(2000)
# #ROIs.append('-add 1 -roi 29 1 37 1 65 1 0 1')
# #
# # Right Superior frontal gyrus from table 2 Lee(2000)
# ROIs.append('-add 1 -roi 31 1 67 1 63 1 0 1')
# #
# # Right Inferior frontal gyrus from table 2 Lee(2000)
# ROIs.append('-add 1 -roi 21 1 71 1 50 1 0 1')
# #
# # Right Posterior ITG from table 2 Lee(2000)
# ROIs.append('-add 1 -roi 19 1 33 1 35 1 0 1')
#
## vmPFC Big
#ROIs.append('-add 1 -roi 45 1 86 1 33 1 0 1')
#
## mOFC_Fitz
#ROIs.append('-add 1 -roi 52 1 78 1 33 1 0 1')
##
## mOFC_Arana
#ROIs.append('-add 1 -roi 49 1 85 1 26 1 0 1')
##
## mOFC_Plass
#ROIs.append('-add 1 -roi 42 1 78 1 27 1 0 1')
##
## vmPFC_Kahnt value region from Kahnt (2011)
#ROIs.append('-add 1 -roi 48 1 88 1 33 1 0 1')
#vmPFC_Kahnt_anti
#ROIs.append('-add 1 -roi 42 1 88 1 33 1 0 1')

## vmPFC_Chib Chib -- Doherty (2009)
#ROIs.append('-add 1 -roi 46 1 84 1 33 1 0 1')
#
## vmPFC_McClure
#ROIs.append('-add 1 -roi 41 1 93 1 36 1 0 1')
##
## vmPFC_ODoherty
#ROIs.append('-add 1 -roi 45 1 78 1 27 1 0 1')
##
## vmPFC_Kim
#ROIs.append('-add 1 -roi 48 1 76 1 28 1 0 1')
##
## vmPFC_Lim
#ROIs.append('-add 1 -roi 47 1 73 1 29 1 0 1')
##
# # vmPFC_Levy
# ROIs.append('-add 1 -roi 50 1 83 1 33 1 0 1')

# # vmPFC_Combs
# This ROI contains the peaks PFC activity (z-score) for control value using both MLE and MLErank

#MLERank -control Value
#z1= 3.8364@[47, 91, 33]
#ROIs.append('-add 1 -roi 47 1 91 1 33 1 0 1')
#z2= 3.7856@[44, 86, 28]
#ROIs.append('-add 1 -roi 44 1 86 1 28 1 0 1')
#MLE -control Value
#z3= 3.502 @[45, 90, 28] 
#ROIs.append('-add 1 -roi 45 1 90 1 28 1 0 1')
#Peak of activity in TFC correction in MLE (control value [45, 87, 28])
# z4
#ROIs.append('-add 1 -roi 45 1 87 1 28 1 0 1')
# Split the difference
#ROIs.append('-add 1 -roi 45 1 89 1 30 1 0 1')
# Combs5
#v1MLERank -Value
#[49, 84, 31]
ROIs.append('-add 1 -roi 49 1 84 1 31 1 0 1')

#
#

'''
#########
##Nodes##
#########
'''
sphericalROI = pe.Workflow(name = 'sphericalROI',
                           base_dir = workingdir)

#Zero the standard brain
zeroing = pe.Node(interface=fsl.BinaryMaths(in_file = TemplateBrain,
                                            operation = 'mul',
                                            operand_value = 0),
                       name='zeroing')
                       
                       
# Node for creating a point at the center of the ROI
addPoint = pe.Node(interface=fsl.maths.MathsCommand(# Find a way to RegEx this
#                                                    args = '-add 1 -roi 45 1 74 1 51 1 0 1'
                                                    ),
                       iterables = ('args',ROIs),
                       name='addPoint')

# node for expanding the point
dilatePoint = pe.Node(interface=fsl.DilateImage(operation = 'mean',
                                                kernel_shape = 'sphere',
                                                kernel_size = 3),
                       name='dilatePoint')
                       
#DataSink  --- stores important outputs
dataSink = pe.Node(interface=nio.DataSink(base_directory= ROIDir,
                                          parameterization = True # This line keeps the DataSink from adding an aditional level to the directory, I have no Idea why this works.
                                          
                                          ),
                   name="dataSink")
                       
                       
'''
###############
##Connections##
###############
'''

sphericalROI.connect([(zeroing, addPoint,[('out_file','in_file')]),
                      (addPoint, dilatePoint,[('out_file','in_file')]),
                      (dilatePoint,dataSink,[('out_file','ROI')]),
                      ])

sphericalROI.run()