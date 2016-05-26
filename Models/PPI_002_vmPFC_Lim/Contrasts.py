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
cont1 = ['Scaling_1IS','T', ['Scaling_1IS'],[1]]
cont2 = ['Bundling_1IS','T', ['Bundling_1IS'],[1]]
cont3 = ['Scaling_CV','T', ['Scaling_CV'],[1]]
cont4 = ['Bundling_CV','T', ['Bundling_CV'],[1]]

cont5 = ['Control_connectivity','T', ['Control_connectivity'],[1]]
cont6 = ['Scaling_1IS_connectivity','T', ['Scaling_1IS_connectivity'],[1]]
cont7 = ['Bundling_1IS_connectivity','T', ['Bundling_1IS_connectivity'],[1]]
cont8 = ['Scaling_CV_connectivity','T', ['Scaling_CV_connectivity'],[1]]
cont9 = ['Bundling_CV_connectivity','T', ['Bundling_CV_connectivity'],[1]]

cont10= ['Scaling_1IS>Control', 'T',['Control','Scaling_1IS'], [-1,1]]
cont11= ['Bundling_1IS>Control','T',['Control','Bundling_1IS'],[-1,1]]
cont12= ['Scaling_CV>Control',  'T',['Control','Scaling_CV'],  [-1,1]]
cont13= ['Bundling_CV>Control', 'T',['Control','Bundling_CV'], [-1,1]]

cont14= ['Scaling_1IS>Scaling_CV',  'T',['Scaling_1IS','Scaling_CV'],  [-1,1]]
cont15= ['Bundling_1IS>Bundling_CV','T',['Bundling_1IS','Bundling_CV'],[-1,1]]

cont16= ['Scaling_1IS_connectivity>Control', 'T',['Control_connectivity','Scaling_1IS_connectivity'], [-1,1]]
cont17= ['Bundling_1IS_connectivity>Control','T',['Control_connectivity','Bundling_1IS_connectivity'],[-1,1]]
cont18= ['Scaling_CV_connectivity>Control',  'T',['Control_connectivity','Scaling_CV_connectivity'],  [-1,1]]
cont19= ['Bundling_CV_connectivity>Control', 'T',['Control_connectivity','Bundling_CV_connectivity'], [-1,1]]

cont20= ['Scaling_1IS_connectivity>Scaling_CV_connectivity',  'T',['Scaling_1IS_connectivity','Scaling_CV_connectivity'],  [1,-1]]
cont21= ['Bundling_1IS_connectivity>Bundling_CV_connectivity','T',['Bundling_1IS_connectivity','Bundling_CV_connectivity'],[1,-1]]

cont22= ['Scaling_CV_connectivity>Scaling_1IS_connectivity',  'T',['Scaling_CV_connectivity','Scaling_1IS_connectivity'],  [1,-1]]
cont23= ['Bundling_CV_connectivity>Bundling_1IS_connectivity','T',['Bundling_CV_connectivity','Bundling_1IS_connectivity'],[1,-1]]

contrasts = [cont0, cont1, cont2, cont3,
             cont4, cont5, cont6, cont7,
             cont8, cont9, cont10,cont11,
             cont12,cont13,cont14,cont15,
             cont16,cont17,cont18,cont19,
             cont20,cont21,cont22,cont23]
