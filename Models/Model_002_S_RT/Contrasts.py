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
cont0 = ['Control', 'T', ['Control'], [1]]
cont1 = ['Scaling', 'T', ['Scaling'], [1]]
cont2 = ['Bundling','T', ['Bundling'],[1]]

cont3 = ['ControlValue', 'T', ['ControlValue'], [1]]
cont4 = ['ScalingValue', 'T', ['ScalingValue'], [1]]
cont5 = ['BundlingValue','T', ['BundlingValue'],[1]]

cont6 = ['ControlEase', 'T', ['ControlDifficulty'], [1]]
cont7 = ['ScalingEase', 'T', ['ScalingDifficulty'], [1]]
cont8 = ['BundlingEase','T', ['BundlingDifficulty'],[1]]

cont9 = ['ControlDifficulty', 'T', ['ControlDifficulty'], [-1]]
cont10= ['ScalingDifficulty', 'T', ['ScalingDifficulty'], [-1]]
cont11= ['BundlingDifficulty','T', ['BundlingDifficulty'],[-1]]

cont12= ['Control<Scaling', 'T', ['Control','Scaling'], [-1,1]]
cont13= ['Control<Bundling','T', ['Control','Bundling'],[-1,1]]
cont14= ['Scaling<Bundling','T', ['Scaling','Bundling'],[-1,1]]

cont15= ['Control>Scaling', 'T', ['Control','Scaling'], [1,-1]]
cont16= ['Control>Bundling','T', ['Control','Bundling'],[1,-1]]
cont17= ['Scaling>Bundling','T', ['Scaling','Bundling'],[1,-1]]

cont18= ['ControlValue<ScalingValue', 'T', ['ControlValue','ScalingValue'], [-1,1]]
cont19= ['ControlValue<BundlingValue','T', ['ControlValue','BundlingValue'],[-1,1]]
cont20= ['ScalingValue<BundlingValue','T', ['ScalingValue','BundlingValue'],[-1,1]]

cont21= ['ControlValue>ScalingValue', 'T', ['ControlValue','ScalingValue'], [1,-1]]
cont22= ['ControlValue>BundlingValue','T', ['ControlValue','BundlingValue'],[1,-1]]
cont23= ['ScalingValue>BundlingValue','T', ['ScalingValue','BundlingValue'],[1,-1]]

cont24= ['ControlDifficulty<ScalingDifficulty','T',  ['ControlDifficulty','ScalingDifficulty'], [-1,1]]
cont25= ['ControlDifficulty<BundlingDifficulty','T', ['ControlDifficulty','BundlingDifficulty'],[-1,1]]
cont26= ['ScalingDifficulty<BundlingDifficulty','T', ['ScalingDifficulty','BundlingDifficulty'],[-1,1]]

cont27= ['ControlDifficulty>ScalingDifficulty','T',  ['ControlDifficulty','ScalingDifficulty'], [1,-1]]
cont28= ['ControlDifficulty>BundlingDifficulty','T', ['ControlDifficulty','BundlingDifficulty'],[1,-1]]
cont29= ['ScalingDifficulty>BundlingDifficulty','T', ['ScalingDifficulty','BundlingDifficulty'],[1,-1]]

contrasts = [cont0, cont1, cont2, cont3,
             cont4, cont5, cont6, cont7,
             cont8, cont9, cont10,cont11,
             cont12,cont13,cont14,cont15,
             cont16,cont17,cont18,cont19,
             cont20,cont21,cont22,cont23,
             cont24,cont25,cont26,cont27,
             cont28,cont29]
