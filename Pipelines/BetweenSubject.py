"""
Created on Tue Aug 12 10:38:27 2014

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
import nipype.pipeline.engine as pe          # pypeline engine

from nipype import config
config.enable_debug_mode()

"""
==============
Configurations
==============
"""

#This should be the only thing you have to set
modelName = "Model_002_LB_DiffOnly"

from PipelineConfig import *
# Bring in the path names from the configureation file
data_dir, preProcDir, ev_dir, withinSubjectResults_dir, betweenSubjectResults_dir, workingdir,crashRecordsDir = configPaths(modelName)


# This needs to point to the code directory Let's see if the ~ works in this context
sys.path.append("../Models/" + modelName)
from Contrasts import *

"""
=========
Functions
=========
"""
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



'''
==============
META NODES
==============
'''
# MASTER node
masterpipeline = pe.Workflow(name= "MasterWorkfow")
masterpipeline.base_dir = workingdir + '/MFX'
masterpipeline.config = {"execution": {"crashdump_dir":crashRecordsDir}}



# 2nd level dataGrabber
contrast_ids = range(0,len(contrasts))
l2source = pe.Node(nio.DataGrabber(infields=['con'],
                                   outfields=['copes','varcopes']),
                   name="l2source")

l2source.inputs.base_directory = withinSubjectResults_dir
l2source.inputs.template = '*'
l2source.inputs.field_template= dict(copes=     '%s/copes/%s/contrast%d/cope1.nii.gz',
                                     varcopes=  '%s/varcopes/%s/contrast%d/varcope1.nii.gz')
l2source.inputs.template_args = dict(copes=     [[subject_list,subject_list,'con']],
                                     varcopes=  [[subject_list,subject_list,'con']]
                                     )
# iterate over all contrast images
l2source.iterables = [('con',contrast_ids)]
l2source.inputs.sort_filelist = True

# DataSink
#DataSink  --- stores important outputs
MFXdatasink = pe.Node(interface=nio.DataSink(base_directory= betweenSubjectResults_dir,
                                          parameterization = True # This line keeps the DataSink from adding an aditional level to the directory, I have no Idea why this works.
                                          ),
                   name="datasink")
MFXdatasink.inputs.substitutions = [('_subject_id_', ''),
                                 ('_flameo', 'contrast')]


'''
==================
Second Level Nodes
==================
'''

#merge the copes and varcopes for each condition
copemerge    = pe.Node(interface=fsl.Merge(dimension='t'),
                           name="copemerge")
varcopemerge = pe.Node(interface=fsl.Merge(dimension='t'),
                           name="varcopemerge")

#level 2 model design files (there's one for each contrast)
level2model = pe.Node(interface=fsl.L2Model(),
                      name='l2model')

#estimate a Random-FX level model
flameo = pe.MapNode(interface=fsl.FLAMEO(run_mode='flame1',
                                         mask_file = mniMask),
                    name="flameo",
                    iterfield=['cope_file','var_cope_file'])
                    
thresholdPositive = pe.MapNode(interface=fsl.Threshold(thresh = 1.645,
                                               direction = 'below'),
                     name = 'thresholdPositive',
                     iterfield=['in_file'])
                     
thresholdNegative = pe.MapNode(interface=fsl.Threshold(thresh = -1.645,
                                               direction = 'above'),
                     name = 'thresholdNegative',
                     iterfield=['in_file'])
                     
thresholdCombined = pe.MapNode(interface=fsl.BinaryMaths(operation = 'add'),
                               name = 'thresholdCombined',
                               iterfield=['in_file', 'operand_file'])

ROIs = pe.MapNode(interface = fsl.ApplyMask(),
                       name ='ROIs',
                       iterfield=['in_file'],
                       iterables = ('mask_file',ROI_Masks))

'''
===========
Connections
===========
'''


masterpipeline.connect([(l2source,copemerge,[('copes','in_files')]),
                        (l2source,level2model,[(('copes', num_copes),'num_copes')]),
                        (l2source,varcopemerge,[('varcopes','in_files')])
                        ])
                        
                        
masterpipeline.connect([(copemerge,flameo,[('merged_file','cope_file')]),
                        (varcopemerge,flameo,[('merged_file','var_cope_file')]),
                        (level2model,flameo, [('design_mat','design_file'),
                                              ('design_con','t_con_file'),
                                              ('design_grp','cov_split_file')]),
                        ])  
                        
masterpipeline.connect([(flameo,thresholdPositive,[('zstats','in_file')]),
                        (flameo,thresholdNegative,[('zstats','in_file')]),
                        (thresholdPositive,thresholdCombined,[('out_file','in_file')]),
                        (thresholdNegative,thresholdCombined,[('out_file','operand_file')]),
                        (flameo,ROIs,[('zstats','in_file')])])

masterpipeline.connect([(flameo,MFXdatasink,[('copes','copes'),
                                             ('tstats','tstats'),
                                             ('var_copes','var_copes'),
                                             ('zstats','zstats'),
                                             ]),
                         (thresholdPositive,MFXdatasink,[('out_file','thresholdedPositive')]),
                         (thresholdNegative,MFXdatasink,[('out_file','thresholdedNegative')]),
                         (thresholdCombined,MFXdatasink,[('out_file','thresholdedCombined')]),
                         (ROIs,MFXdatasink,[('out_file','ROIs')])
                         ])
        
if __name__ == '__main__':
#    masterpipeline.write_graph(graph2use='hierarchical')    
    # masterpipeline.run()
    outgraph = masterpipeline.run(plugin='MultiProc', plugin_args={'n_procs':20})

