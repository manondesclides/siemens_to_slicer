#!/usr/bin/python3

import sys
import numpy as np
import nibabel as nb
import argparse
import os
import subprocess

from numpy.lib.npyio import loads
import functions as f
import config



def convert(filenames, opt_load, opt_rewrite, opt_select):
    for filename in filenames:
        root_ext = os.path.splitext(filename)
        if not(os.path.isfile(root_ext[0] + ".h5") and not opt_rewrite): 
            if os.path.isfile(root_ext[0] + ".h5") and opt_rewrite: 
                os.remove(root_ext[0] + ".h5")
        
            bashCommand = "siemens_to_ismrmrd -f "+ filename + " -z 2 \
                -m " + config.SIEMENS_TO_ISMRMRD_CONFIG_NAME + " \
                -x " + config.SIEMENS_TO_ISMRMRD_PARAMETER_MAP_NAME + " \
                -o " + root_ext[0] + ".h5" 
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        
        bashCommand="gnome-terminal --tab -- gadgetron"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        
        bashCommand = "gadgetron_ismrmrd_client -f "+root_ext[0] + ".h5 -c " +config.GADGETRON_XML_NAME + " -o "+root_ext[0]+"out.h5"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        
        output_tmp = '/tmp/gadgetron/thermo/'
        files = []
        for i in os.listdir(output_tmp):
            if os.path.isfile(os.path.join(output_tmp,i)) and 'buffer' in i and '.img' in i:
                files.append(i)
                
                
        #analyse (.img/ .hdr) to nifti         
        for file in files:
            filename = file.replace('buffer', '')
            filename=root_ext[0]+filename 
            if not(os.path.isfile(filename.replace('.img', '.nii')) and not opt_rewrite):
                img = nb.load(output_tmp+file)
                dat = img.get_fdata()
                squeezed_dat = np.squeeze(dat)
                squeezed_dat.shape
                new_h = img.header.copy()
                new_nifti = nb.nifti1.Nifti1Image(squeezed_dat, None, header=new_h)
                filename = file.replace('buffer', '')
                filename=root_ext[0]+filename 
                nb.save(new_nifti, filename.replace('.img', '.nii'))
            
 
        



if __name__ == "__main__":

    
    parser = argparse.ArgumentParser(description='Convert .dat to .nrrd and load in 3DSlicer in option.')
    parser.add_argument("-f", type=str, nargs="+", help="Indicate filepaths to be converted (seperated with a ' ' if many).")
    parser.add_argument("-d", type=str, help="Indicate path folder where file will be converted.")
    parser.add_argument("--load", dest='opt_load',action='store_true',  help="Flag to indicate if .nrrd will be loaded in 3DSlicer at the end of the conversion.")
    parser.add_argument("--rewrite", dest='opt_rewrite',action='store_true', help="Flag to indicate if conversion will rewrite already converted files.")
    parser.add_argument("-s", type=str, nargs="+",  help="Key words to select specific files to convert in a directory. Logical function between keywords : AND.")

    args = parser.parse_args()
    opt_file = args.f
    opt_dir = args.d
    opt_select = args.s
    filenames = []
    
    if opt_file:
        for file in opt_file:
            if file.endswith(".dat") and not '3D' in file:
                filenames.append(file)
                print("File to convert : " + file)
                opt_select.append(os.path.splitext(os.path.basename(file)))


    if opt_dir:
        for file in os.listdir(opt_dir):
            if file.endswith(".dat") and not '3D' in file:
                filenames.append(opt_dir+file)
                
        if filenames:
            print("\n\nIn folder : "+ os.path.dirname(filenames[0])+ "\n\nFound " + str(len(filenames))+ " files to convert :\n   ")
            print(*[os.path.split(i)[1] for i in filenames], sep="\n    ")
            
    if filenames:
        convert(filenames, args.opt_load, args.opt_rewrite, opt_select)

    #convert nifti to nrrd and load nrrd in slicer or not depending on option opt_load
    if opt_select:
        bashCommand = config.SLICER_EXECUTABLE_PATH + " --no-main-window --python-script " + os.path.join(os.getcwd(),"functions/nifti_to_nrrd.py")+ " -d " + os.path.split(filenames[0])[0]+'/' + " -s "+" ".join(opt_select) 
    else:
        bashCommand = config.SLICER_EXECUTABLE_PATH + " --no-main-window --python-script " + os.path.join(os.getcwd(),"functions/nifti_to_nrrd.py")+ " -d " + os.path.split(filenames[0])[0]+'/' 
    if args.opt_load:
        bashCommand = bashCommand+" --load "  
    
  
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
        
    print("\nFinished conversion.")
