# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 21:09:03 2016

@author: Dalton
"""

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

#%%

def get_used_options(group):
    valuedOptions = group[group[valueModel]==group[valueModel]]
    valuedOptionItems = np.concatenate((valuedOptions['item1'], valuedOptions['item2']),axis = 0)
    group = group[group['item1'].isin(valuedOptionItems)]
    return group

def fill_with_est_value(row):
    if row.type == 1:
        if row[valueModel] == row[valueModel]: #nan does not equal itself
            return row[valueModel]
        else: # if row.MLEValueS == nan
            return row['est_value']
    else:
        return row[valueModel]
    
def nan_filler(group):
    # remove the nans
    regressable = group[(group[valueModel] == group[valueModel]) & (group['type'] == 1)]
    # compute a regression
    slope, intercept, r_value, p_value, std_err = sp.stats.linregress(regressable[['rank', valueModel]])
    # Solve for the estomated value
    group['est_value'] = (slope * group['rank']) + intercept
    # fill in the blanks with estimated value
    group['filled_value'] = group.apply(fill_with_est_value, 1)
    return group['filled_value']

def one_item_sufficient(row):
    if np.nanmax([row.Item1Value, row.Item2Value]) > row.Opt2Value:
        return 1
    else:
        return 0

def valueBuilder(row):
    if np.nanmax([row.Item1Value, row.Item2Value]) > row.FixedValue:
        return np.nanmax([row.Item1Value, row.Item2Value])
    else:
        return row.ComOptValue
        
#%% import data        
#options = pd.DataFrame.from_csv(dataDir + '/RawData/Group/optionValue.csv', index_col=False)
responses = pd.DataFrame.from_csv(dataDir + '/RawData/Group/responses_with_value_and_rank.csv', index_col=False)
responses = responses[responses['SubjID'] != 3304] 

#%%

responses['should_choose'] = responses['Opt1Value'] > responses['Opt2Value']

responses['consistent'] = responses['should_choose'] == (responses['Choice']-1)

grouped = responses.groupby('SubjID').agg(np.mean)


