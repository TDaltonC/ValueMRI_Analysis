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
cont0 = ['Control','T', ['Control'],[1]]
cont1 = ['Scaling','T', ['Scaling'],[1]]
cont2 = ['Bundling','T', ['Bundling'],[1]]

cont3 = ['ControlValue','T', ['ControlValue'],[1]]
cont4 = ['ScalingValue','T', ['ScalingValue'],[1]]
cont5 = ['BundlingValue','T', ['BundlingValue'],[1]]

cont6 = ['ControlValue>ScalingValue','T', ['ControlValue','ScalingValue'],[1,-1]]
cont7 = ['ControlValue>BundlingValue','T', ['ControlValue','BundlingValue'],[1,-1]]
cont8 = ['ScalingValue>BundlingValue','T', ['ScalingValue','BundlingValue'],[1,-1]]

cont9 = ['Control>Scaling','T', ['Control','Scaling'],[1,-1]]
cont10= ['Control>Bundling','T', ['Control','Bundling'],[1,-1]]
cont11= ['Scaling>Bundling','T', ['Scaling','Bundling'],[1,-1]]
cont12= ['Control>Scaling+Bundling','T', ['Control','Scaling','Bundling'],[1,-.5,-.5]]
contrasts = [cont0,cont1,cont2,cont3,
             cont4,cont5,cont6,cont7,
             cont8,cont9,cont10,cont11,
             cont12]
