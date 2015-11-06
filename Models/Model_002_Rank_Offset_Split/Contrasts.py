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

cont3 = ['ControlPosValue','T', ['ControlPosValue'],[1]]
cont4 = ['ScalingPosValue','T', ['ScalingPosValue'],[1]]
cont5 = ['BundlingPosValue','T', ['BundlingPosValue'],[1]]

cont6 = ['ControlPosValue>ScalingPosValue','T', ['ControlPosValue','ScalingPosValue'],[1,-1]]
cont7 = ['ControlPosValue>BundlingPosValue','T', ['ControlPosValue','BundlingPosValue'],[1,-1]]
cont8 = ['ScalingPosValue>BundlingPosValue','T', ['ScalingPosValue','BundlingPosValue'],[1,-1]]

cont9 = ['ControlNegValue','T', ['ControlNegValue'],[1]]
cont10= ['ScalingNegValue','T', ['ScalingNegValue'],[1]]
cont11= ['BundlingNegValue','T', ['BundlingNegValue'],[1]]

cont12= ['ControlNegValue>ScalingNegValue','T', ['ControlNegValue','ScalingNegValue'],[1,-1]]
cont13= ['ControlNegValue>BundlingNegValue','T', ['ControlNegValue','BundlingNegValue'],[1,-1]]
cont14= ['ScalingNegValue>BundlingNegValue','T', ['ScalingNegValue','BundlingNegValue'],[1,-1]]

cont15= ['Control>Scaling','T', ['Control','Scaling'],[1,-1]]
cont16= ['Control>Bundling','T', ['Control','Bundling'],[1,-1]]
cont17= ['Scaling>Bundling','T', ['Scaling','Bundling'],[1,-1]]
cont18= ['Control>Scaling+Bundling','T', ['Control','Scaling','Bundling'],[1,-.5,-.5]]
contrasts = [cont0,cont1,cont2,cont3,
             cont4,cont5,cont6,cont7,
             cont8,cont9,cont10,cont11,
             cont12,cont13,cont14,cont15,
             cont16,cont17,cont18]
