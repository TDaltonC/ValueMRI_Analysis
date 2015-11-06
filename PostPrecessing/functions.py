import os
import nibabel as nib
import numpy as np
import seaborn as sns


# System Setting (Local(MAC) or Remote(linux))
# system = "Darwin" # Mac
system = "Linux"
if system == "Darwin":
    data_dir = "/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data"
    fsl_dir = "/usr/local/fsl"
    CPU_Count = 2
elif system == "Linux":
    data_dir = "/vol"
    fsl_dir = "/usr/share/fsl/5.0"
    CPU_Count = 16

def ROIdata(model, contrast, ROI, dataDir = data_dir):
    ROI = nib.load( dataDir + 'Models/' +
     model + '/MFX_Results/ROIs/_' +
     contrast + '/_mask_file_..vol..RIOs..' +
     ROI + 'nii.gz/_ROIs0/zstat1_masked.nii.gz')

    rawData = ROI.get_data()

    # Reshape in to array with only one dimention
    red1 = np.reshape(rawData,-1) 

    # Remove Zeros
    nonZeros = red1[red1!=0]
    return nonZeros