# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 16:08:50 2014

@author: Dalton
"""

## From MNI to 2mm voxel space

MNIx = 52
MNIy = -59
MNIz = -2

# X coordinate
Vx = (MNIx-90)/(-2)

# Y coordinate
Vy = (MNIy + 126)/2

# Z coordinate
Vz = (MNIz+72)/2

print Vx
print Vy
print Vz

