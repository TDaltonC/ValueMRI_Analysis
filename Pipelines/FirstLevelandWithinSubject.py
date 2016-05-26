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
import nipype.algorithms.modelgen as model   # model generation
import nipype.algorithms.rapidart as ra      # artifact detection
from nipype import LooseVersion              # for simplifying versions
import json
import PipelineConfig as PC
# These two lines enable debug mode
from nipype import config
config.enable_debug_mode()

"""
==============
Configurations
==============
"""

# Get the FSL version code
version = 0
if fsl.Info.version() and \
    LooseVersion(fsl.Info.version()) > LooseVersion('5.0.6'):
    version = 507

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

def within_subj_Dir(model_name):
    withinSubjectResults_dir = '/data/Models/' + model_name + "/FFX_Results/"
    return withinSubjectResults_dir

def contrast_decode(cont_file):
  import json
  cont_string = open(cont_file)
  cont = json.load(cont_string)
  return cont

"""
======================
Configure  Directoriess
======================
"""

model_name = PC.models[0]

model_folder = model_name + "/"

# Bring in the path names from the configureation file
data_dir                 = PC.data_dir
workingdir               = PC.data_dir + PC.working_folder
crashRecordsDir          = workingdir  + PC.crash_report_folder


# from Contrasts import contrasts


"""
======================
model fitting workflow
======================

NODES
"""
#Master Node
modelfit = pe.Workflow(name='modelfit')

#generate design information
modelspec = pe.Node(interface=model.SpecifyModel(input_units = PC.input_units,
                                                 time_repetition = PC.TR,
                                                 high_pass_filter_cutoff = PC.hpcutoff),
                    name="modelspec")

#generate a run specific fsf file for analysis
level1design = pe.Node(interface=fsl.Level1Design(interscan_interval = PC.TR,
                                                  bases = {'dgamma':{'derivs': False}},
                                                  # contrasts = contrasts,
                                                  model_serial_correlations = True),
                       name="level1design")

#generate a run specific mat file for use by FILMGLS
modelgen = pe.MapNode(interface=fsl.FEATModel(), name='modelgen',
                      iterfield = ['fsf_file', 'ev_files'])


if version < 507:
    #estomate Model
    modelestimate = pe.MapNode(interface=fsl.FILMGLS(smooth_autocorr=True,
                                                     mask_size=5,
                                                     threshold=1000),
                                                     name='modelestimate',
                                                     iterfield = ['design_file',
                                                                  'in_file'])

    #estimate contrasts
    conestimate = pe.MapNode(interface=fsl.ContrastMgr(), name='conestimate',
                             iterfield = ['tcon_file','param_estimates',
                                          'sigmasquareds', 'corrections',
                                          'dof_file'])
else:
    #estomate Model and Contrasts
    modelestimate = pe.MapNode(interface=fsl.FILMGLS(smooth_autocorr=True,
                                                     mask_size=5,
                                                     threshold=1000),
                                                     name='modelestimate',
                                                     iterfield = ['design_file',
                                                                  'in_file',
                                                                  'tcon_file'])

'''
CONNECTIONS
'''
if version < 507:
    modelfit.connect([
       (modelspec,level1design,[('session_info','session_info')]),
       (level1design,modelgen,[('fsf_files', 'fsf_file'),
                               ('ev_files', 'ev_files')]),
       (modelgen,modelestimate,[('design_file','design_file')]),
       (modelgen,conestimate,[('con_file','tcon_file')]),
       (modelestimate,conestimate,[('param_estimates','param_estimates'),
                                   ('sigmasquareds', 'sigmasquareds'),
                                   ('corrections','corrections'),
                                   ('dof_file','dof_file')]),
       ])
else:
    modelfit.connect([
       (modelspec,level1design,[('session_info','session_info')]),
       (level1design,modelgen,[('fsf_files', 'fsf_file'),
                               ('ev_files', 'ev_files')]),
       (modelgen,modelestimate,[('design_file','design_file'),
                                ('con_file','tcon_file')]),
       ])    

"""
======================
fixed-effects workflow
======================

NODES
"""
# Master Node
fixed_fx = pe.Workflow(name='fixedfx')

#merge the copes and varcopes for each condition
copemerge    = pe.MapNode(interface=fsl.Merge(dimension='t'),
                          iterfield=['in_files'],
                          name="copemerge")
varcopemerge = pe.MapNode(interface=fsl.Merge(dimension='t'),
                       iterfield=['in_files'],
                       name="varcopemerge")

#level 2 model design files (there's one for each condition of each subject)
level2model = pe.Node(interface=fsl.L2Model(),
                      name='l2model')

#estimate a second level model
flameo = pe.MapNode(interface=fsl.FLAMEO(run_mode='fe',
                                         mask_file = PC.mniMask), name="flameo",
                    iterfield=['cope_file','var_cope_file'])
# ROI maskes
ROIs = pe.MapNode(interface = fsl.ApplyMask(),
                       name ='ROIs',
                       iterfield=['in_file'],
                       iterables = ('mask_file',PC.ROI_Masks))

'''
Connections
'''
fixed_fx.connect([(copemerge,flameo,[('merged_file','cope_file')]),
                  (varcopemerge,flameo,[('merged_file','var_cope_file')]),
                  (level2model,flameo, [('design_mat','design_file'),
                                        ('design_con','t_con_file'),
                                        ('design_grp','cov_split_file')]),
                  (flameo, ROIs, [('tstats', 'in_file')]),
                  ])


"""
=======================
Within-Subject workflow
=======================

NODES
"""
#Master NODE
withinSubject = pe.Workflow(name='withinSubject')

"""
CONNECTIONS
"""
if version < 507:
    withinSubject.connect([(modelfit, fixed_fx,[(('conestimate.copes', sort_copes),'copemerge.in_files'),
                                                (('conestimate.varcopes', sort_copes),'varcopemerge.in_files'),
                                                (('conestimate.copes', num_copes),'l2model.num_copes'),
                                               ])
                        ])
else:
    withinSubject.connect([(modelfit, fixed_fx,[(('modelestimate.copes', sort_copes),'copemerge.in_files'),
                                                (('modelestimate.varcopes', sort_copes),'varcopemerge.in_files'),
                                                (('modelestimate.copes', num_copes),'l2model.num_copes'),
                                               ])
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
modle_subj_source = pe.Node(interface=util.IdentityInterface(fields=['model_name', 'subject_id']),
                     name="modle_subj_source")
modle_subj_source.iterables = [('subject_id', PC.subject_list),
                               ('model_name', PC.models)]

# The datagrabber finds all of the files that need to be run and makes sure that
# they get to the right nodes at the begining of the protocol.
datasource = pe.Node(interface=nio.DataGrabber(infields=['model_name', 'subject_id'],
                                               outfields=['func', 'art', 'evs', 'cont']),
                     name = 'datasource')
datasource.inputs.base_directory = data_dir
datasource.inputs.template = '*'
datasource.inputs.field_template= dict(func=  'PreProcessed/%s/func2MNI/out_file/_subject_id_%s/*/*.nii*',
                                       art =  'PreProcessed/%s/art/outlier_files/_subject_id_%s/*/*.txt',
                                       evs =  'Models/%s/EventFiles/%s/RUN%d/*.txt',
                                       cont=  'Models/%s/EventFiles/contrasts.json'
                                       )
datasource.inputs.template_args = dict(func=  [['subject_id', 'subject_id']],
                                       art =  [['subject_id', 'subject_id']],
                                       evs =  [['model_name', 'subject_id', PC.func_scan]],
                                       cont=  [['model_name']])
datasource.inputs.sort_filelist = True




#DataSink  --- stores important outputs
datasink = pe.Node(interface=nio.DataSink(parameterization = True), # This line keeps the DataSink from adding an aditional level to the directory, I have no Idea why this works.                   
                      name="datasink")
datasink.inputs.substitutions = [('_subject_id_', ''),
                                 ('_flameo', 'contrast')]


"""
CONNECTIONS
"""

masterpipeline.connect([(modle_subj_source, datasource, [('subject_id', 'subject_id'),
                                                         ('model_name', 'model_name')]),
                    (datasource, withinSubject, [('evs',  'modelfit.modelspec.event_files'),
                                                 ('func', 'modelfit.modelspec.functional_runs'),
                                                 ('func', 'modelfit.modelestimate.in_file'),
                                                 ('art',  'modelfit.modelspec.outlier_files'),
                                                 (('cont', contrast_decode), 'modelfit.level1design.contrasts')
                                                ]),
                    (modle_subj_source, datasink, [('subject_id', 'container'),
                                                   (('model_name', within_subj_Dir),'base_directory')]),
                    # (modle_subj_source, masterpipeline, [(('model_name', working_Dir),'base_dir'),
                    #                                      (('model_name', crash_Dir),'config')])
                    ])

#DataSink Connections -- These are put with the meta flow becuase the dataSink 
                       # reaches in to a lot of deep places, but it is not of 
                       # those places; hence META.
withinSubject.connect([(modelfit,datasink,[('modelestimate.param_estimates','regressorEstimates')]),
                       (modelfit,datasink,[('level1design.fsf_files', 'fsf_file')]),
                       (fixed_fx,datasink,[('flameo.tstats','tstats'),
                                          ('flameo.copes','copes'),
                                          ('flameo.var_copes','varcopes'),
                                          ]),
                       (ROIs, datasink,[('out_file','ROIs')])
                       ])


"""
====================
Execute the pipeline
====================
"""

if __name__ == '__main__':
    # Plot a network visualization of the pipline
    masterpipeline.write_graph(graph2use='hierarchical')
    # modelfit.write_graph(graph2use='exec')

    # Run the paipline using 1 CPUs
    # outgraph = masterpipeline.run()    
    # Run the paipline using multi-Core
    outgraph = masterpipeline.run(plugin='MultiProc', plugin_args={'n_procs': PC.CPU_Count})



