# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 12:42:49 2014

@author: Dalton
"""
#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
=========
Imports
=========
"""
import os                                    # system functions
import sys
import nipype.interfaces.io as nio           # Data i/o
import nipype.interfaces.fsl as fsl          # fsl
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
import nipype.algorithms.rapidart as ra      # artifact detection

# These two lines enable debug mode
#from nipype import config
#config.enable_debug_mode()

"""
==============
Configurations
==============
"""
from PipelineConfig import *
data_dir, preProcDir, ev_dir, withinSubjectResults_dir, betweenSubjectResults_dir, workingdir,crashRecordsDir = configPaths()

"""
=========
Functions
=========
"""
#function to pick the first file from a list of files
def pickfirst(files):
    if isinstance(files, list):
        return files[0]
    else:
        return files
        
#function to return the 1 based index of the middle volume
def getmiddlevolume(func):
    from nibabel import load
    funcfile = func
    if isinstance(func, list):
        funcfile = func[0]
    _,_,_,timepoints = load(funcfile).get_shape()
    return (timepoints/2)-1

#function to get the scaling factor for intensity normalization
def getinormscale(medianvals):
    return ['-mul %.10f'%(10000./val) for val in medianvals]

#function to get 10% of the intensity
def getthreshop(thresh):
    return '-thr %.10f -Tmin -bin'%(0.1*thresh[0][1])

#functions to get the brightness threshold for SUSAN
def getbtthresh(medianvals):
    return [0.75*val for val in medianvals]
    
def getusans(x):
    return [[tuple([val[0],0.75*val[1]])] for val in x]

#Function to Sort Copes
def sort_copes(files):
    numelements = len(files[0])
    outfiles = []
    for i in range(numelements):
        outfiles.insert(i,[])
        for j, elements in enumerate(files):
            outfiles[i].append(elements[i])
    return outfiles
    
def num_copes(files):
    return len(files)


"""
=======================
preprocessing workflow
=======================

NODES
"""
#Master node
preproc = pe.Workflow(name='preproc')

#inout utility node
inputnode = pe.Node(interface=util.IdentityInterface(fields=['func',
                                                             'struct',]),
                    name='inputspec')

#Convert functional images to floats.
#use a MapNode to paralelize
img2float = pe.MapNode(interface=fsl.ImageMaths(out_data_type='float',
                                             op_string = '',
                                             suffix='_dtype'),
                       iterfield=['in_file'],
                       name='img2float')

#Extract the middle volume of the first run as the reference
extract_ref = pe.Node(interface=fsl.ExtractROI(t_size=1),
                      name = 'extractref')

#Realign the functional runs to the middle volume of the first run
motion_correct = pe.MapNode(interface=fsl.MCFLIRT(save_mats = True,
                                                  save_plots = True),
                            name='motion_correct',
                            iterfield = ['in_file'])
                            
#Plot the estimated motion parameters
plot_motion = pe.MapNode(interface=fsl.PlotMotionParams(in_source='fsl'),
                        name='plot_motion',
                        iterfield=['in_file'])
plot_motion.iterables = ('plot_type', ['rotations', 'translations'])

#Extract the mean volume of the first functional run
meanfunc = pe.Node(interface=fsl.ImageMaths(op_string = '-Tmean',
                                            suffix='_mean'),
                   name='meanfunc')

#Strip the skull from the mean functional
meanfuncmask = pe.Node(interface=fsl.BET(mask = True,
                                         no_output=True,
                                         frac = 0.3,
                                         robust = True),
                       name = 'meanfuncmask')

#Mask the functional runs with the extracted mask
maskfunc = pe.MapNode(interface=fsl.ImageMaths(suffix='_bet',
                                               op_string='-mas'),
                      iterfield=['in_file'],
                      name = 'maskfunc')

#Determine the 2nd and 98th percentile intensities of each functional run
getthresh = pe.MapNode(interface=fsl.ImageStats(op_string='-p 2 -p 98'),
                       iterfield = ['in_file'],
                       name='getthreshold')
                       
#Threshold the first run of the functional data at 10% of the 98th percentile
threshold = pe.Node(interface=fsl.ImageMaths(out_data_type='char',
                                             suffix='_thresh'),
                    name='threshold')

#Determine the median value of the functional runs using the mask
medianval = pe.MapNode(interface=fsl.ImageStats(op_string='-k %s -p 50'),
                       iterfield = ['in_file'],
                       name='medianval')

#Dilate the mask
dilatemask = pe.Node(interface=fsl.ImageMaths(suffix='_dil',
                                              op_string='-dilF'),
                     name='dilatemask')

#Mask the motion corrected functional runs with the dilated mask
maskfunc2 = pe.MapNode(interface=fsl.ImageMaths(suffix='_mask',
                                                op_string='-mas'),
                       iterfield=['in_file'],
                       name='maskfunc2')
                       
#Determine the mean image from each functional run
meanfunc2 = pe.MapNode(interface=fsl.ImageMaths(op_string='-Tmean',
                                                suffix='_mean'),
                       iterfield=['in_file'],
                       name='meanfunc2')

#Merge the median values with the mean functional images into a coupled list
mergenode = pe.Node(interface=util.Merge(2, axis='hstack'),
                    name='merge')

#Smooth each run using SUSAN 
#brightness threshold set to xx% of the median value for each run by function 'getbtthresh'
#and a mask constituting the mean functional
smooth = pe.MapNode(interface=fsl.SUSAN(fwhm = 5.),
                    iterfield=['in_file', 'brightness_threshold','usans'],
                    name='smooth'
                    )

#Mask the smoothed data with the dilated mask
maskfunc3 = pe.MapNode(interface=fsl.ImageMaths(suffix='_mask',
                                                op_string='-mas'),
                       iterfield=['in_file'],
                       name='maskfunc3')

#Scale each volume of the run so that the median value of the run is set to 10000
intnorm = pe.MapNode(interface=fsl.ImageMaths(suffix='_intnorm'),
                     iterfield=['in_file','op_string'],
                     name='intnorm')

#Perform temporal highpass filtering on the data
highpass = pe.MapNode(interface=fsl.ImageMaths(suffix='_hpf',
                                               op_string = '-bptf %.10f -1'%(hpcutoff/TR)),
                      iterfield=['in_file'],
                      name='highpass')

#Skull Strip the structural image
nosestrip = pe.Node(interface=fsl.BET(frac=0.3),
                    name = 'nosestrip')
skullstrip = pe.Node(interface=fsl.BET(mask = True, robust = True),
                     name = 'stripstruct')

#register the mean functional image to the structural image
coregister = pe.MapNode(interface=fsl.FLIRT(dof=6),
                     iterfield=['in_file'],
                     name = 'coregister')

#Find outliers based on deviations in intensity and/or movement.
art = pe.MapNode(interface=ra.ArtifactDetect(use_differences = [True, False],
                                             use_norm = True,
                                             norm_threshold = 1,
                                             zintensity_threshold = 3,
                                             parameter_source = 'FSL',
                                             mask_type = 'file'),
                 iterfield=['realigned_files', 'realignment_parameters'],
                 name="art")
                
# Register structurals to a mni reference brain
# Use FLIRT first without skulls

mniFLIRT = pe.Node(interface=fsl.FLIRT(reference = strippedmfxTemplateBrain),
                   name = 'mniFLIRT')
                   
                
# THen leave the skulls on both brains 
# But apply the trasnformation to striped functionals later                                  
mniFNIRT = pe.Node(interface=fsl.FNIRT(ref_file=mfxTemplateBrain,
                                     config_file = mniConfig,
                                     field_file = True,
                                     fieldcoeff_file = True),
                 name = 'mniFNIRT')                 
                 
                         
func2MNI = pe.MapNode(interface = fsl.ApplyWarp(ref_file = mfxTemplateBrain),
                         iterfield=['in_file','premat'],
                         name = 'func2MNI')
                         
#Generate a mean functional (it's quicker to check a mean then a timesearies)
meanfunc3 = pe.MapNode(interface=fsl.ImageMaths(op_string='-Tmean',
                                                suffix='_mean'),
                       iterfield=['in_file'],
                       name='meanfunc3')
                       
#Generate a mean functional (it's quicker to check a mean then a timesearies)
meanfunc4 = pe.MapNode(interface=fsl.ImageMaths(op_string='-Tmean',
                                                suffix='_mean'),
                       iterfield=['in_file'],
                       name='meanfunc4')
                 
"""
Connections
"""
preproc.connect([(inputnode, img2float,[('func', 'in_file')]),
                 (img2float, extract_ref,[(('out_file', pickfirst), 'in_file')]),
                 (inputnode, extract_ref, [(('func', getmiddlevolume), 't_min')]),
                 (img2float, motion_correct, [('out_file', 'in_file')]),
                 (extract_ref, motion_correct, [('roi_file', 'ref_file')]),
                 (motion_correct, plot_motion, [('par_file', 'in_file')]),
                 (motion_correct, meanfunc, [(('out_file', pickfirst), 'in_file')]),
                 (meanfunc, meanfuncmask, [('out_file', 'in_file')]),
                 (motion_correct, maskfunc, [('out_file', 'in_file')]),
                 (meanfuncmask, maskfunc, [('mask_file', 'in_file2')]),
                 (maskfunc, getthresh, [('out_file', 'in_file')]),
                 (maskfunc, threshold, [(('out_file', pickfirst), 'in_file')]),
                 (getthresh, threshold, [(('out_stat', getthreshop), 'op_string')]),
                 (motion_correct, medianval, [('out_file', 'in_file')]),
                 (threshold, medianval, [('out_file', 'mask_file')]),
                 (threshold, dilatemask, [('out_file', 'in_file')]),
                 (motion_correct, maskfunc2, [('out_file', 'in_file')]),
                 (dilatemask, maskfunc2, [('out_file', 'in_file2')]),
                 (maskfunc2, meanfunc2, [('out_file', 'in_file')]),
                 (medianval, intnorm, [(('out_stat', getinormscale), 'op_string')]),
                 (meanfunc2, mergenode, [('out_file', 'in1')]),
                 (medianval, mergenode, [('out_stat', 'in2')]),
                 (maskfunc2, smooth, [('out_file', 'in_file')]),
                 (medianval, smooth, [(('out_stat', getbtthresh), 'brightness_threshold')]),
                 (mergenode, smooth, [(('out', getusans), 'usans')]),
                 (smooth, maskfunc3, [('smoothed_file', 'in_file')]),
                 (dilatemask, maskfunc3, [('out_file', 'in_file2')]),
                 (maskfunc3, intnorm, [('out_file', 'in_file')]),
                 (intnorm, highpass, [('out_file', 'in_file')]),
                 (inputnode, nosestrip,[('struct','in_file')]),
                 (nosestrip, skullstrip, [('out_file','in_file')]),
                 (skullstrip, coregister,[('out_file','reference')]),
                 (meanfunc2, coregister,[('out_file','in_file')]),
                 (motion_correct, art, [('par_file','realignment_parameters')]),
                 (maskfunc2, art, [('out_file','realigned_files')]),
                 (dilatemask, art, [('out_file', 'mask_file')]),
                 (skullstrip,mniFLIRT,[('out_file','in_file')]),
                 (mniFLIRT, mniFNIRT, [('out_matrix_file','affine_file')]),
                 (inputnode,mniFNIRT,[('struct','in_file')]),
                 (highpass,func2MNI,[('out_file','in_file')]),
                 (coregister,func2MNI,[('out_matrix_file','premat')]),
                 (mniFNIRT,func2MNI,[('fieldcoeff_file','field_file')]),
                 (func2MNI, meanfunc4, [('out_file', 'in_file')])
                 ])
                 
"""
=============
META workflow
=============

NODES
"""
# Master NODE
masterpipeline = pe.Workflow(name= "MasterWorkfow")
masterpipeline.base_dir = workingdir + '/FFX'
masterpipeline.config = {"execution": {"crashdump_dir":crashRecordsDir}}

# Set up inforsource to iterate over 'subject_id's
infosource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']),
                     name="infosource")
infosource.iterables = ('subject_id', subject_list)

# The datagrabber finds all of the files that need to be run and makes sure that
# they get to the right nodes at the benining of the protocol.
datasource = pe.Node(interface=nio.DataGrabber(infields=['subject_id'],
                                               outfields=['func', 'struct']),
                     name = 'datasource')
datasource.inputs.base_directory = data_dir
datasource.inputs.template = '*'
datasource.inputs.field_template= dict(func=  'RawData/%s/niis/Scan%d*.nii',
                                       struct='RawData/%s/niis/co%s*.nii')
datasource.inputs.template_args = dict(func=  [['subject_id', func_scan]],
                                       struct=[['subject_id','t1mprage']])
datasource.inputs.sort_filelist = True



#DataSink  --- stores important outputs
datasink = pe.Node(interface=nio.DataSink(base_directory= preProcDir,
                                          parameterization = True # This line keeps the DataSink from adding an aditional level to the directory, I have no Idea why this works.
                                          
                                          ),
                   name="datasink")


"""
CONNECTIONS
"""

masterpipeline.connect([(infosource, datasource, [('subject_id', 'subject_id')]),
                    (datasource, preproc, [('struct','inputspec.struct'),
                                              ('func', 'inputspec.func'),
                                              ]),
                    (infosource, datasink, [('subject_id', 'container')])
                    ])
                    
#DataSink Connections -- These are put with the meta flow becuase the dataSink 
                       # reaches in to a lot of deep places, but it is not of 
                       # those places; hence META.
masterpipeline.connect([(preproc, datasink,[('func2MNI.out_file','func2MNI.out_file'),
                                          ('art.outlier_files','art.outlier_files'),
                                          ('motion_correct.par_file','motion_correct.par_file'),
                                          ('mniFLIRT.out_file','struct_warped_to_MNI'),
                                          ('meanfunc4.out_file','func_mean_warped_to_MNI'),
                                          ('intnorm.out_file','mean_normed'),
                                          ('highpass.out_file','highpass')
                                          ]),
                       ])


"""
====================
Execute the pipeline
====================
"""

if __name__ == '__main__':
    # Plot a network visualization of the pipline
    # masterpipeline.write_graph(graph2use='hierarchical')
    # preproc.write_graph(graph2use='hierarchical')
    # modelfit.write_graph(graph2use='exec')
    # Run the paipline using 1 CPUs
  # outgraph = masterpipeline.run()    
#     Run the paipline using all CPUs
    outgraph = masterpipeline.run(plugin='MultiProc', plugin_args={'n_procs':((CPU_Count*2)-1)})
