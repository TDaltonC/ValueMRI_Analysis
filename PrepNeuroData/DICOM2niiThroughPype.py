# -*- coding: utf-8 -*-
"""
Created on Thu May  8 09:40:31 2014

@author: Dalton
"""
from nipype import config #These two lines turn on the debugger
config.enable_debug_mode()

import os
import nipype.interfaces.utility as util #import the utility interface
import nipype.interfaces.io as nio
import nipype.pipeline.engine as pe         # the workflow and node wrappers
from nipype.interfaces.dcm2nii import Dcm2nii

#converter = Dcm2nii()
#converter.inputs.source_names = "/Users/Dalton/Documents/FSL/playingWithDICOM/DICOM/SID710/DICOMDIR"
#converter.inputs.output_dir = "/Users/Dalton/Documents/FSL/playingWithDICOM/niis"
#converter.inputs.args = "-d n"
#converter.run()

experiment_dir = '/Users/Dalton/Documents/python'
WorkingDir     = experiment_dir + '/workingdir_prepareflow'
dataDir        = '/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data'

#initiate the infosource node
infosource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']),
                     name="infosource")
#define the list of subjects your pipeline should be executed on
infosource.iterables = ('subject_id', ['SID3301'])

# Build DICOM scourse Direciry
def sourceFinder(subjectname):
    import os
    path_to_subject = '/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/SubjectData'
    path_to_dicomdir = 'Scans/DICOMDIR'
    return os.path.join(path_to_subject, subjectname, path_to_dicomdir)
    
    
def outputFinder(subjectname):
    import os
    path_to_subject = '/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/SubjectData'
    path_to_dicomdir = 'niis'
    return os.path.join(path_to_subject, subjectname, path_to_dicomdir)
    

converter = pe.Node(Dcm2nii(),name="converter")
converter.inputs.args = "-d n"




#Initiation of the preparation pipeline
prepareflow = pe.Workflow(name="prepareflow")

#Define where the workingdir of the all_consuming_workflow should be stored at
prepareflow.base_dir = WorkingDir


prepareflow.connect([(infosource, converter,[(('subject_id',sourceFinder), 'source_names'),
                                             (('subject_id',outputFinder), 'output_dir')])
                     ])
                     
# prepareflow.write_graph(graph2use='orig')
prepareflow.run()
# prepareflow.run(plugin='MultiProc', plugin_args={'n_procs':8})