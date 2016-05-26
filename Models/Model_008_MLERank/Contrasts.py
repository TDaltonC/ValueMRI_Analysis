# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 14:06:38 2014

@author: Dalton
"""

"""
=========
Contrasts
=========
"""

# Contrasts
cont0 = ['Control',    'T', ['Control'],    [1]]
cont1 = ['ScalingSIS', 'T', ['ScalingSIS'], [1]]
cont2 = ['ScalingCV',  'T', ['ScalingCV'],  [1]]
cont3 = ['BundlingSIS','T', ['BundlingSIS'],[1]]
cont4 = ['BundlingCV', 'T', ['BundlingCV'], [1]]

cont5 = ['ControlValue',    'T', ['ControlValue'],    [1]]
cont6 = ['ScalingSISValue', 'T', ['ScalingSISValue'], [1]]
cont7 = ['ScalingCVValue',  'T', ['ScalingCVValue'],  [1]]
cont8 = ['BundlingSISValue','T', ['BundlingSISValue'],[1]]
cont9 = ['BundlingCVValue', 'T', ['BundlingCVValue'], [1]]

cont10= ['ControlEase',    'T', ['ControlDifficulty'],    [1]]
cont11= ['ScalingSISEase', 'T', ['ScalingSISDifficulty'], [1]]
cont12= ['ScalingCVEase',  'T', ['ScalingCVDifficulty'],  [1]]
cont13= ['BundlingSISEase','T', ['BundlingSISDifficulty'],[1]]
cont14= ['BundlingCVEase', 'T', ['BundlingCVDifficulty'], [1]]

cont15= ['ControlDifficulty',    'T', ['ControlDifficulty'],    [-1]]
cont16= ['ScalingSISDifficulty', 'T', ['ScalingSISDifficulty'], [-1]]
cont17= ['ScalingCVDifficulty',  'T', ['ScalingCVDifficulty'],  [-1]]
cont18= ['BundlingSISDifficulty','T', ['BundlingSISDifficulty'],[-1]]
cont19= ['BundlingCVDifficulty', 'T', ['BundlingCVDifficulty'], [-1]]

cont20= ['Control<ScalingSIS', 'T', ['Control','ScalingSIS'], [-1,1]]
cont21= ['Control>ScalingSIS', 'T', ['Control','ScalingSIS'], [1,-1]]
cont22= ['Control<ScalingCV',  'T', ['Control','ScalingCV'],  [-1,1]]
cont23= ['Control>ScalingCV',  'T', ['Control','ScalingCV'],  [1,-1]]
cont24= ['Control<BundlingSIS','T', ['Control','BundlingSIS'],[-1,1]]
cont25= ['Control>BundlingSIS','T', ['Control','BundlingSIS'],[1,-1]]
cont26= ['Control<BundlingCV', 'T', ['Control','BundlingCV'], [-1,1]]
cont27= ['Control>BundlingCV', 'T', ['Control','BundlingCV'], [1,-1]]

cont28= ['ScalingCV<ScalingSIS','T', ['ScalingCV','ScalingSIS'],[-1,1]]
cont29= ['ScalingCV>ScalingSIS','T', ['ScalingCV','ScalingSIS'],[1,-1]]

cont30= ['BundlingCV<BundlingSIS','T', ['BundlingCV','BundlingSIS'],[-1,1]]
cont31= ['BundlingCV>BundlingSIS','T', ['BundlingCV','BundlingSIS'],[1,-1]]

cont32= ['ScalingCV<BundlingCV','T', ['ScalingCV','BundlingCV'],[-1,1]]
cont33= ['ScalingCV>BundlingCV','T', ['ScalingCV','BundlingCV'],[1,-1]]

cont34= ['ScalingSIS<BundlingSIS','T', ['ScalingSIS','BundlingSIS'],[-1,1]]
cont35= ['ScalingSIS>BundlingSIS','T', ['ScalingSIS','BundlingSIS'],[1,-1]]

cont36= ['ControlValue<ScalingSISValue', 'T', ['ControlValue','ScalingSISValue'], [-1,1]]
cont37= ['ControlValue>ScalingSISValue', 'T', ['ControlValue','ScalingSISValue'], [1,-1]]
cont38= ['ControlValue<ScalingCVValue',  'T', ['ControlValue','ScalingCVValue'],  [-1,1]]
cont39= ['ControlValue>ScalingCVValue',  'T', ['ControlValue','ScalingCVValue'],  [1,-1]]
cont40= ['ControlValue<BundlingSISValue','T', ['ControlValue','BundlingSISValue'],[-1,1]]
cont41= ['ControlValue>BundlingSISValue','T', ['ControlValue','BundlingSISValue'],[1,-1]]
cont42= ['ControlValue<BundlingCVValue', 'T', ['ControlValue','BundlingCVValue'], [-1,1]]
cont43= ['ControlValue>BundlingCVValue', 'T', ['ControlValue','BundlingCVValue'], [1,-1]]

cont44= ['ScalingCVValue<ScalingSISValue','T', ['ScalingCVValue','ScalingSISValue'],[-1,1]]
cont45= ['ScalingCVValue>ScalingSISValue','T', ['ScalingCVValue','ScalingSISValue'],[1,-1]]

cont46= ['BundlingCVValue<BundlingSISValue','T', ['BundlingCVValue','BundlingSISValue'],[-1,1]]
cont47= ['BundlingCVValue>BundlingSISValue','T', ['BundlingCVValue','BundlingSISValue'],[1,-1]]

cont48= ['ScalingCVValue<BundlingCVValue','T', ['ScalingCVValue','BundlingCVValue'],[-1,1]]
cont49= ['ScalingCVValue>BundlingCVValue','T', ['ScalingCVValue','BundlingCVValue'],[1,-1]]

cont50= ['ScalingSISValue<BundlingSISValue','T', ['ScalingSISValue','BundlingSISValue'],[-1,1]]
cont51= ['ScalingSISValue>BundlingSISValue','T', ['ScalingSISValue','BundlingSISValue'],[1,-1]]

cont52= ['ControlDifficulty<ScalingSISDifficulty', 'T', ['ControlDifficulty','ScalingSISDifficulty'], [-1,1]]
cont53= ['ControlDifficulty>ScalingSISDifficulty', 'T', ['ControlDifficulty','ScalingSISDifficulty'], [1,-1]]
cont54= ['ControlDifficulty<ScalingCVDifficulty',  'T', ['ControlDifficulty','ScalingCVDifficulty'],  [-1,1]]
cont55= ['ControlDifficulty>ScalingCVDifficulty',  'T', ['ControlDifficulty','ScalingCVDifficulty'],  [1,-1]]
cont56= ['ControlDifficulty<BundlingSISDifficulty','T', ['ControlDifficulty','BundlingSISDifficulty'],[-1,1]]
cont57= ['ControlDifficulty>BundlingSISDifficulty','T', ['ControlDifficulty','BundlingSISDifficulty'],[1,-1]]
cont58= ['ControlDifficulty<BundlingCVDifficulty', 'T', ['ControlDifficulty','BundlingCVDifficulty'], [-1,1]]
cont59= ['ControlDifficulty>BundlingCVDifficulty', 'T', ['ControlDifficulty','BundlingCVDifficulty'], [1,-1]]

cont60= ['ScalingCVDifficulty<ScalingSISDifficulty','T', ['ScalingCVDifficulty','ScalingSISDifficulty'],[-1,1]]
cont61= ['ScalingCVDifficulty>ScalingSISDifficulty','T', ['ScalingCVDifficulty','ScalingSISDifficulty'],[1,-1]]

cont62= ['BundlingCVDifficulty<BundlingSISDifficulty','T', ['BundlingCVDifficulty','BundlingSISDifficulty'],[-1,1]]
cont63= ['BundlingCVDifficulty>BundlingSISDifficulty','T', ['BundlingCVDifficulty','BundlingSISDifficulty'],[1,-1]]

cont64= ['ScalingCVDifficulty<BundlingCVDifficulty','T', ['ScalingCVDifficulty','BundlingCVDifficulty'],[-1,1]]
cont65= ['ScalingCVDifficulty>BundlingCVDifficulty','T', ['ScalingCVDifficulty','BundlingCVDifficulty'],[1,-1]]

cont66= ['ScalingSISDifficulty<BundlingSISDifficulty','T', ['ScalingSISDifficulty','BundlingSISDifficulty'],[-1,1]]
cont67= ['ScalingSISDifficulty>BundlingSISDifficulty','T', ['ScalingSISDifficulty','BundlingSISDifficulty'],[1,-1]]


contrasts = [ cont0, cont1, cont2, cont3, cont4, cont5, cont6, cont7, cont8, cont9,
             cont10,cont11,cont12,cont13,cont14,cont15,cont16,cont17,cont18,cont19,
             cont20,cont21,cont22,cont23,cont24,cont25,cont26,cont27,cont28,cont29,
             cont30,cont31,cont32,cont33,cont34,cont35,cont36,cont37,cont38,cont39,
             cont40,cont41,cont42,cont43,cont44,cont45,cont46,cont47,cont48,cont49,
             cont50,cont51,cont52,cont53,cont54,cont55,cont56,cont57,cont58,cont59,
             cont60,cont61,cont62,cont63,cont64,cont65,cont66,cont67]
