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

cont3 = ['Control_connectivity','T', ['Control_connectivity'],[1]]
cont4 = ['Scaling_connectivity','T', ['Scaling_connectivity'],[1]]
cont5 = ['Bundling_connectivity','T', ['Bundling_connectivity'],[1]]

cont6 = ['Scaling>Control', 'T', ['Control','Scaling'],[-1,1]]
cont7 = ['Bundling>Control','T', ['Control','Bundling'],[-1,1]]
cont8 = ['Bundling>Scaling','T', ['Scaling','Bundling'],[-1,1]]

cont9 = ['Scaling_connectivity>Control_connectivity', 'T', ['Control_connectivity','Scaling_connectivity'], [-1,1]]
cont10= ['Bundling_connectivity>Control_connectivity','T', ['Control_connectivity','Bundling_connectivity'],[-1,1]]
cont11= ['Bundling_connectivity>Scaling_connectivity','T', ['Scaling_connectivity','Bundling_connectivity'],[-1,1]]

contrasts = [cont0,cont1, cont2, cont3,
             cont4,cont5, cont6, cont7,
             cont8,cont9,cont10,cont11]
