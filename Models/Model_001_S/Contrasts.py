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
cont1 = ['Value','T', ['Value'],[1]]
cont2 = ['Difficulty','T', ['Difficulty'],[1]]
cont3 = ['Scaling','T', ['Scaling'],[1]]
cont4 = ['Bundling','T', ['Bundling'],[1]]
cont5 = ['Scaling>Control','T', ['Scaling','Control'],[1,-1]]
cont6 = ['Bundling>Control','T', ['Bundling','Control'],[1,-1]]
cont7 = ['Bundling>Scaling','T', ['Bundling','Scaling'],[1,-1]]
cont8 = ['Scaling>Bundling','T', ['Scaling','Bundling'],[1,-1]]
cont9 = ['Scaling+Bundling>Control','T', ['Scaling','Bundling','Control'],[.5,.5,-1]]
contrasts = [cont0,cont1,cont2,cont3,cont4,cont5,cont6,cont7,cont8,cont9]
