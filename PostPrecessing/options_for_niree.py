# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 12:18:58 2016

@author: Dalton
"""

import pandas as pd
import seaborn as sb
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.figure as figure
import nibabel as nib
from matplotlib.colors import LinearSegmentedColormap
import glob # for using wildcards in file paths

#%%
#dataDir = '/data' # on Linux
dataDir = "/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data" # on MAC
valueModel = 'MLEValueS'

#%% import data        
options = pd.DataFrame.from_csv(dataDir + '/RawData/Group/NireeOptionValue.csv', index_col=False)
#responses = responses[responses['SubjID'] != 3304] 

#%% 

single_item_options = options[options['type'] == 1]
single_item_options = single_item_options[['SubjID', 'item1', 'MLEValueS']].copy()

single_item_options.columns = ['SubjID', 'item1', 'item1value']

options1 = pd.merge(options, single_item_options, on = ['SubjID', 'item1'], how = 'left')
single_item_options.columns = ['SubjID', 'item2', 'item2value']
options2 = pd.merge(options1, single_item_options, on = ['SubjID', 'item2'], how = 'left')