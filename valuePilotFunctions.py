# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 16:01:07 2014

@author: Dalton
"""
import os
import errno
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.image as mpimg
import matplotlib as mpl

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')
 
def num_itm_on_screen(trialType):
    if   trialType == 1:
        return 0
    elif trialType in (2, 3):
        return 1
    elif trialType in (4, 7):
        return 2
    elif trialType in (5, 8):
        return 3
    elif trialType in (6, 9):
        return 4

num_itm_on_screen_Vec = np.vectorize(num_itm_on_screen)


def simpleTrialType(trialType):
    if   trialType == 1:
        return "Fixation"
    elif trialType in (2, 3):
        return "Control"
    elif trialType in (4, 5, 6):
        return "Scaling"
    elif trialType in (7, 8, 9):
        return "Bundling"

simpleTrialType_Vec = np.vectorize(simpleTrialType)


def savePlotDisributionsByTT(trialbytrialDF,columnStr,DIR):
    trialbytrialDF = trialbytrialDF[(trialbytrialDF.linearValue  != 0)]
    trialbytrialDF["trialName"] = simpleTrialType_Vec(trialbytrialDF.trialType)
    trialbytrialDF["Numitem"] = num_itm_on_screen_Vec(trialbytrialDF.trialType)
    sb.kdeplot(trialbytrialDF[(trialbytrialDF.trialName  == "Control")][columnStr],label = "Control")
    sb.kdeplot(trialbytrialDF[(trialbytrialDF.trialName  == "Scaling")][columnStr],label = "Scaling")
    sb.kdeplot(trialbytrialDF[(trialbytrialDF.trialName  == "Bundling")][columnStr],label = "Bundling")
    mpl.pyplot.savefig(DIR + '/' + columnStr + '.svg')
    mpl.pyplot.clf()
#    mpimg.imsave(DIR+'/'+columnStr+' .png',plot)
def savePlotDisributionsByItemCount(trialbytrialDF,columnStr,DIR):
    trialbytrialDF = trialbytrialDF[(trialbytrialDF.linearValue  != 0)]
    trialbytrialDF["ItemCount"] = num_itm_on_screen_Vec(trialbytrialDF.trialType)
    sb.kdeplot(trialbytrialDF[(trialbytrialDF.ItemCount  == 1)][columnStr],label = "1_Item")
    sb.kdeplot(trialbytrialDF[(trialbytrialDF.ItemCount  == 2)][columnStr],label = "2_Item")
    sb.kdeplot(trialbytrialDF[(trialbytrialDF.ItemCount  == 3)][columnStr],label = "3_Item")
    sb.kdeplot(trialbytrialDF[(trialbytrialDF.ItemCount  == 4)][columnStr],label = "4_Item")
    mpl.pyplot.savefig(DIR + '/' + columnStr + 'ByItemCount.svg')
    mpl.pyplot.clf()