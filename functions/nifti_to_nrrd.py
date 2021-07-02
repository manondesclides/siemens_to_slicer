#!/usr/bin/python3
import os.path
import numpy as np
import os
import glob
import sys
import subprocess
import argparse
import slicer 
import MultiVolumeImporter
import config


def convert(importer,filename,opt_rewrite):
    mvNode1 = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMultiVolumeNode')
  
    slicer.mrmlScene.AddNode(mvNode1)
    filename_NIFTI = filename
    if filename_NIFTI.endswith(".nii"):
        filename_NRRD = filename_NIFTI.replace(".nii", ".nrrd")
    elif filename_NIFTI.endswith(".nii.gz"):
        filename_NRRD = filename_NIFTI.replace(".nii.gz", ".nrrd")
        
    if opt_rewrite or not os.path.exists(filename_NRRD):
        importer.read4DNIfTI(mvNode1, filename_NIFTI)
        slicer.util.saveNode(mvNode1, filename_NRRD)
        print(filename_NIFTI + " converted.")
    slicer.mrmlScene.RemoveNode(mvNode1)
    return filename_NRRD
    
    

   
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script so useful.')
    parser.add_argument("-f", type=str, nargs="+", help="Indicate filepaths to be converted (seperated with a ' ' if many).") 
    parser.add_argument("-d", type=str, help="Indicate path folder where file will be converted.")
    parser.add_argument("-s", type=str, nargs="+", help="Key words to select specific files to convert in a directory. Logical function between keywords : AND.")
    parser.add_argument("--load", dest='opt_load',action='store_true', help="Flag to indicate if .nrrd will be loaded in 3DSlicer at the end of the conversion.")
    parser.add_argument("--rewrite",dest='opt_rewrite', action='store_true' , help="Flag to indicate if conversion will rewrite already converted files.")

    args = parser.parse_args()
    opt_file = args.f
    opt_dir = args.d
    opt_select = args.s
    
    filenames_nrdd = []

            
    importer = MultiVolumeImporter.MultiVolumeImporterWidget()

    
    
    
    if opt_file:
        for file in opt_file:
            if file.endswith(".nii") or file.endswith(".nii.gz"):
                filenames_nrdd.append(convert(importer, file, args.opt_rewrite))
        bashCommand = config.SLICER_EXECUTABLE_PATH + " --python-script " + os.path.join(os.getcwd(),"functions/load_nrrd_slicer.py") + "-f "+ " ".join(filenames_nrdd)
    if opt_dir:
        for file in os.listdir(opt_dir):
            if (file.endswith(".nii") or file.endswith(".nii.gz")): 
                if opt_select and  all(selection in file for selection in opt_select):
                    convert(importer,opt_dir+file, args.opt_rewrite)
                else:
                    convert(importer,opt_dir+file, args.opt_rewrite)
        if opt_select:   
            bashCommand = config.SLICER_EXECUTABLE_PATH + " --python-script "  + os.path.join(os.getcwd(),"functions/load_nrrd_slicer.py") + " -d " + opt_dir + " -s "+" ".join(opt_select) 
        else:
            bashCommand = config.SLICER_EXECUTABLE_PATH + " --python-script "  + os.path.join(os.getcwd(),"functions/load_nrrd_slicer.py") + " -d " + opt_dir 
    
    slicer.mrmlScene.Clear(0)
    print("Finished conversion from NIFTI to NRRD.")
    if args.opt_load and bashCommand:
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
    else:
        exit()
