# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 11:56:25 2015

@author: Dalton
"""

import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt

options = pd.DataFrame.from_csv('../records/options.csv', index_col = 'index')
responses = pd.DataFrame.from_csv('../records/responses.csv', index_col = 'index')
#randomResponses = pd.DataFrame.from_csv('../records/RandomResponses.csv', index_col = 'index')
#%% Population level plot

heatMapData = pd.pivot_table(responses,index='opt2Code', columns='opt1Code', values='chosenOpt')
mask=heatMapData.isnull()
plt.figure(figsize=(18, 12))
sb.heatmap(heatMapData, cmap='jet', square=True, mask=heatMapData.isnull())

#%%
for subject in np.unique(options.SID):
    subjOpt = options[options.SID   == subject]
    subjResp= responses[responses.SID==subject]
    #%%
    sb.pairplot(subjOpt[['elicitedRank','valueLBUBSUM','valueLBUB','valueLB','value']],
    #            kind = 'reg'
                )

    #%% Heatmaps
    
    # Reduce to only singleton options
    responses_Singleton = subjResp[(subjResp.opt1item2 == 0) & (subjResp.opt2item2 == 0)]    
    heatMapData_Singleton = pd.pivot_table(responses_Singleton,index='opt2Code', columns='opt1Code', values='chosenOpt')
    plt.figure(figsize=(18, 12))
    sb.heatmap(heatMapData_Singleton,square=True,mask=heatMapData_Singleton.isnull())


    #responses = responses[['opt1Code','opt2Code','chosenOpt']]
    
    heatMapData = pd.pivot_table(subjResp,index='opt2Code', columns='opt1Code', values='chosenOpt')
    mask=heatMapData.isnull()
    plt.figure(figsize=(18, 12))
    sb.heatmap(heatMapData, cmap='rainbow', square=True, mask=heatMapData.isnull())

    plt.figure(figsize=(1, 20))
    subjOpt.sort(['elicitedRank'],inplace = True)
    sb.heatmap(subjOpt[['type','itemCount']],cmap = 'rainbow')
#    
    plt.figure()
    sb.lmplot('elicitedRank','value',subjOpt,hue='type',fit_reg=False)

#%% Can rank predict choices?

responses['rankDistance'] = abs(responses['opt1Rank']-responses['opt2Rank'])
responses['valueDistance'] = abs(responses['opt1Value']-responses['opt2Value'])


rankPredictionByRankDistance = pd.pivot_table(responses,index = ['SID','rankDistance'], values = ['chosenOpt','value'])

rankPredictionByRankDistance['accuracy'] = abs(rankPredictionByRankDistance['chosenOpt']-2)

rankPredictionByRankDistance.reset_index(inplace = True)
groupedBySID = rankPredictionByRankDistance.groupby('SID')
rankPredictionByRankDistance['accuracyNormed'] = groupedBySID['accuracy'].apply(lambda x: (x-min(x))/(max(x)-min(x)))
sb.lmplot('rankDistance','accuracy',rankPredictionByRankDistance, x_jitter = .1)
sb.lmplot('rankDistance','accuracyNormed',rankPredictionByRankDistance, x_jitter = .1)

#%% Are the contradictions from preference changes or confussion?
contradictions = pd.pivot_table(responses, index = ['SID','opt1Code','opt2Code'], values=['chosenOpt','rankDistance'])
contradictions.reset_index(inplace = True)
contradictions['reversal'] = contradictions['chosenOpt']
contPoltData = contradictions.groupby('SID').agg({'chosenOpt': lambda x: np.sum(x-1)/np.count_nonzero(x),
                                                  'reversal':  lambda y: np.float(np.sum(y==2))/np.float(len(y))})

sb.lmplot('chosenOpt','reversal',contPoltData)
