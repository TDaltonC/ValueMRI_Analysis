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
options = pd.DataFrame.from_csv(dataDir + '/RawData/Group/optionValue.csv', index_col=False)
responses = pd.DataFrame.from_csv(dataDir + '/RawData/Group/trialByTrial.csv', index_col=False)
responses = responses[responses['SubjID'] != 3304]     
#%%fill in missing data 
options = options.groupby('SubjID').apply(get_used_options)
options.reset_index(drop = True, inplace = True)
optionsByUser = options.groupby('SubjID').apply(nan_filler)
options[valueModel] = optionsByUser.reset_index(drop = True)

#%%
# Add item values
single_item_options = options[options['item2'] == 0]
itemValues = single_item_options.loc[:,['item1', valueModel, 'SubjID']].copy()
# add the value for option1Item1
itemValues.columns = ['Rank', 'Opt1Item1Value', 'SubjID']
responses_with_one_item_values = responses.merge(itemValues, how = 'left', left_on = ['Opt1Item1', 'SubjID'], right_on = ['Rank', 'SubjID'])
# add the value for option1Item2
itemValues.columns = ['Rank', 'Opt1Item2Value', 'SubjID']
responses_with_two_item_values = responses_with_one_item_values.merge(itemValues, how = 'left', left_on = ['Opt1Item2', 'SubjID'], right_on = ['Rank', 'SubjID'])

itemValues.columns = ['Rank', 'Opt2Item1Value', 'SubjID']
responses_with_three_item_values = responses_with_two_item_values.merge(itemValues, how = 'left', left_on = ['Opt2Item1', 'SubjID'], right_on = ['Rank', 'SubjID'])
# add the value for option1Item2
itemValues.columns = ['Rank', 'Opt2Item2Value', 'SubjID']
responses_with_four_item_values = responses_with_three_item_values.merge(itemValues, how = 'left', left_on = ['Opt2Item2', 'SubjID'], right_on = ['Rank', 'SubjID'])

responses_with_item_values = responses_with_four_item_values

# Add item Ranks
options_for_rank = options[options[valueModel]==options[valueModel]]
options_for_rank['MLERank'] = options_for_rank.sort(valueModel).groupby('SubjID')[valueModel].transform(lambda score: np.arange(1, len(score)+1, 1))
single_item_options = options_for_rank[options_for_rank['item2'] == 0]
itemValues = single_item_options.loc[:,['item1', 'MLERank', 'SubjID']].copy()
# add the value for option1Item1
itemValues.columns = ['Rank', 'Opt1Item1Rank', 'SubjID']
responses_with_one_item_ranks = responses_with_item_values.merge(itemValues, how = 'left', left_on = ['Opt1Item1', 'SubjID'], right_on = ['Rank', 'SubjID'])
# add the value for option1Item2
itemValues.columns = ['Rank', 'Opt1Item2Rank', 'SubjID']
responses_with_two_item_ranks = responses_with_one_item_ranks.merge(itemValues, how = 'left', left_on = ['Opt1Item2', 'SubjID'], right_on = ['Rank', 'SubjID'])

itemValues.columns = ['Rank', 'Opt2Item1Rank', 'SubjID']
responses_with_three_item_ranks = responses_with_two_item_ranks.merge(itemValues, how = 'left', left_on = ['Opt2Item1', 'SubjID'], right_on = ['Rank', 'SubjID'])
# add the value for option1Item2
itemValues.columns = ['Rank', 'Opt2Item2Rank', 'SubjID']
responses_with_four_item_ranks = responses_with_three_item_ranks.merge(itemValues, how = 'left', left_on = ['Opt2Item2', 'SubjID'], right_on = ['Rank', 'SubjID'])

responses_with_item_ranks = responses_with_four_item_ranks

# Add option Values
optValues = options.loc[:,['rank', valueModel, 'SubjID']].copy()
# add the value for the screen option
optValues.columns = ['Rank', 'Opt1Value', 'SubjID']
responses_with_one_opt_value = responses_with_item_ranks.merge(optValues, how = 'left', left_on = ['Opt1Code', 'SubjID'], right_on = ['Rank', 'SubjID'])
# add the value for the fixed option
optValues.columns = ['Rank', 'Opt2Value', 'SubjID']
responses_with_two_opt_value = responses_with_one_opt_value.merge(optValues, how = 'left', left_on = ['Opt2Code', 'SubjID'], right_on = ['Rank', 'SubjID'])
responses_with_two_opt_value['ValueDiff'] = responses_with_two_opt_value['Opt1Value'] - responses_with_two_opt_value['Opt2Value']

# Add option Ranks
optValues = options_for_rank.loc[:,['rank', 'MLERank', 'SubjID']].copy()
# add the value for the screen option
optValues.columns = ['Rank', 'Opt1Rank', 'SubjID']
responses_with_one_opt_rank = responses_with_two_opt_value.merge(optValues, how = 'left', left_on = ['Opt1Code', 'SubjID'], right_on = ['Rank', 'SubjID'])
# add the value for the fixed option
optValues.columns = ['Rank', 'Opt2Rank', 'SubjID']
responses_with_two_opt_rank = responses_with_one_opt_rank.merge(optValues, how = 'left', left_on = ['Opt2Code', 'SubjID'], right_on = ['Rank', 'SubjID'])
responses_with_two_opt_rank['ValueDiff'] = responses_with_two_opt_rank['Opt1Value'] - responses_with_two_opt_value['Opt2Value']

responses_wide = responses_with_two_opt_rank
# Remove null trials
# Remember: nan != nan
responses_wide = responses_wide.loc[(responses_wide['Opt1Value'] == responses_wide['Opt1Value']),:].copy()
responses_wide.drop(['Unnamed: 0', 'Unnamed: 0.1','Rank', 'Rank_x', 'Rank_y'],1, inplace = True)
# Filter by task
scannerResponses = responses_wide[responses_wide.Run > 0].copy()
postScannerResponses = responses_wide[responses_wide.Run == 0].copy()

# Z-score Raction Time
scannerResponses['ZReactionTime'] = scannerResponses.groupby('SubjID')['ReactionTime'].transform(sp.stats.zscore)
postScannerResponses['ZReactionTime'] = postScannerResponses.groupby('SubjID')['ReactionTime'].transform(sp.stats.zscore)

# Z-score Value Diff
scannerResponses['ZValueDiff'] = scannerResponses.groupby('SubjID')['ValueDiff'].transform(sp.stats.zscore)
postScannerResponses['ZValueDiff'] = postScannerResponses.groupby('SubjID')['ValueDiff'].transform(sp.stats.zscore)

#%%
options_used = scannerResponses.drop_duplicates(['SubjID', 'Opt1Code'])
options_used = options_used.loc[:,['SubjID', 'Item1Value', 'Item2Value', 'Opt1Value', 'Opt2Value', 'Opt1Code']]
options_used['used'] = 1

options_used = pd.merge(options, options_used, left_on = ['SubjID', 'rank'], right_on = ['SubjID', 'Opt1Code'], how = 'right')
options_used['sis'] = options_used.apply(one_item_sufficient, 1)


 #%% plot the distribution of value of each of the five

def from_3type_to_5type(row):
    if row.type == 1:
        return 1
    elif row.type == 2:
        if row.sis ==0:
            return 2
        elif row.sis ==1:
            return 3
    elif row.type == 3:
        if row.sis == 0:
            return 4
        elif row.sis == 1:
            return 5

def value_dist_plot(data, **kwargs):
    sb.kdeplot(data.loc[data[:, 'Opt1Value']], **kwargs)
    
def cumm_plot(data, **kwargs):
#    data.sort('Opt1Value', inplace = True)
#    data['rank'] = data.sort('Opt1Value')['Opt1Value'].transform(lambda score: np.linspace(0, 1, len(score)))    
    data['order'] = data.sort('Opt1Value').groupby(['new_type'])['Opt1Value'].transform(lambda score: np.linspace(0, 1, len(score)))
    data.sort('new_type', inplace = True)
    
    sb.pointplot('Opt1Value', 'order', data = data, hue = 'new_type', **kwargs)

options_used['new_type'] = options_used.apply(from_3type_to_5type, 1)
options_used.fillna(0, inplace = True)
plt.figure()
g = sb.FacetGrid(options_used, col="SubjID", col_wrap = 5)
g = g.map_dataframe(cumm_plot)
#g.savefig('/Users/Dalton/Documents/Projects/BundledOptionsExp/Summary/Figures/ValueDistribution.svg', format =  'svg') 
#%%
options_used['rank'] = options_used.sort('Opt1Value').groupby(['SubjID'])['Opt1Value'].transform(lambda score: np.linspace(0, 1, len(score)))
options_used['order'] = options_used.sort('Opt1Code').groupby(['new_type', 'SubjID'])['Opt1Value'].transform(lambda score: np.linspace(0, 1, len(score)))
   
g = sb.lmplot(
    x = 'Opt1Code', 
    y = 'order', 
    col = 'SubjID', 
    col_wrap = 6, 
    hue = 'new_type', 
    data = options_used, 
    scatter_kws={"s": 100},
#    linestyles='-',
#    lowess= True
#    fit_reg = False
    )
g = g.set(xlim=(0, 60), ylim=(0, 1))

g.savefig('/Users/Dalton/Documents/Projects/BundledOptionsExp/Summary/Figures/ValueDistribution.svg', format =  'svg') 

#%%

option_counts = pd.pivot_table(options_used, values = 'Opt1Value', index = 'SubjID', columns = 'new_type', aggfunc = np.count_nonzero)
