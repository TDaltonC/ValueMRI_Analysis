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

cont10= ['Control<ScalingSIS', 'T', ['Control','ScalingSIS'], [-1,1]]
cont11= ['Control>ScalingSIS', 'T', ['Control','ScalingSIS'], [1,-1]]
cont12= ['Control<ScalingCV',  'T', ['Control','ScalingCV'],  [-1,1]]
cont13= ['Control>ScalingCV',  'T', ['Control','ScalingCV'],  [1,-1]]
cont14= ['Control<BundlingSIS','T', ['Control','BundlingSIS'],[-1,1]]
cont15= ['Control>BundlingSIS','T', ['Control','BundlingSIS'],[1,-1]]
cont16= ['Control<BundlingCV', 'T', ['Control','BundlingCV'], [-1,1]]
cont17= ['Control>BundlingCV', 'T', ['Control','BundlingCV'], [1,-1]]

cont18= ['ScalingCV<ScalingSIS','T', ['ScalingCV','ScalingSIS'],[-1,1]]
cont19= ['ScalingCV>ScalingSIS','T', ['ScalingCV','ScalingSIS'],[1,-1]]

cont20= ['BundlingCV<BundlingSIS','T', ['BundlingCV','BundlingSIS'],[-1,1]]
cont21= ['BundlingCV>BundlingSIS','T', ['BundlingCV','BundlingSIS'],[1,-1]]

cont22= ['ScalingCV<BundlingCV','T', ['ScalingCV','BundlingCV'],[-1,1]]
cont23= ['ScalingCV>BundlingCV','T', ['ScalingCV','BundlingCV'],[1,-1]]

cont24= ['ScalingSIS<BundlingSIS','T', ['ScalingSIS','BundlingSIS'],[-1,1]]
cont25= ['ScalingSIS>BundlingSIS','T', ['ScalingSIS','BundlingSIS'],[1,-1]]

cont26= ['ControlValue<ScalingSISValue', 'T', ['ControlValue','ScalingSISValue'], [-1,1]]
cont27= ['ControlValue>ScalingSISValue', 'T', ['ControlValue','ScalingSISValue'], [1,-1]]
cont28= ['ControlValue<ScalingCVValue',  'T', ['ControlValue','ScalingCVValue'],  [-1,1]]
cont29= ['ControlValue>ScalingCVValue',  'T', ['ControlValue','ScalingCVValue'],  [1,-1]]
cont30= ['ControlValue<BundlingSISValue','T', ['ControlValue','BundlingSISValue'],[-1,1]]
cont31= ['ControlValue>BundlingSISValue','T', ['ControlValue','BundlingSISValue'],[1,-1]]
cont32= ['ControlValue<BundlingCVValue', 'T', ['ControlValue','BundlingCVValue'], [-1,1]]
cont33= ['ControlValue>BundlingCVValue', 'T', ['ControlValue','BundlingCVValue'], [1,-1]]

cont34= ['ScalingCVValue<ScalingSISValue','T', ['ScalingCVValue','ScalingSISValue'],[-1,1]]
cont35= ['ScalingCVValue>ScalingSISValue','T', ['ScalingCVValue','ScalingSISValue'],[1,-1]]

cont36= ['BundlingCVValue<BundlingSISValue','T', ['BundlingCVValue','BundlingSISValue'],[-1,1]]
cont37= ['BundlingCVValue>BundlingSISValue','T', ['BundlingCVValue','BundlingSISValue'],[1,-1]]

cont38= ['ScalingCVValue<BundlingCVValue','T', ['ScalingCVValue','BundlingCVValue'],[-1,1]]
cont39= ['ScalingCVValue>BundlingCVValue','T', ['ScalingCVValue','BundlingCVValue'],[1,-1]]

cont40= ['ScalingSISValue<BundlingSISValue','T', ['ScalingSISValue','BundlingSISValue'],[-1,1]]
cont41= ['ScalingSISValue>BundlingSISValue','T', ['ScalingSISValue','BundlingSISValue'],[1,-1]]

contrasts = [ cont0, cont1, cont2, cont3, cont4, cont5, cont6, cont7, cont8, cont9,
             cont10,cont11,cont12,cont13,cont14,cont15,cont16,cont17,cont18,cont19,
             cont20,cont21,cont22,cont23,cont24,cont25,cont26,cont27,cont28,cont29,
             cont30,cont31,cont32,cont33,cont34,cont35,cont36,cont37,cont38,cont39,
             cont40,cont41]
