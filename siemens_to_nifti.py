#!/usr/bin/python3

import sys
import numpy as np
import nibabel as nb
import argparse
import os
import subprocess






def convert(filenames):
    for filename in filenames:
        root_ext = os.path.splitext(filename)
        if os.path.isfile(root_ext[0] + ".h5"): 
            os.remove(root_ext[0] + ".h5")
            
        print(root_ext[0])
        bashCommand = "siemens_to_ismrmrd -f "+ filename + "   -z 2 \
            -m IsmrmrdParameterMap_Siemens.xml \
            -x IsmrmrdParameterMap_Siemens_EPI_PF_PreZeros.xsl \
                -o " + root_ext[0] + ".h5"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        
        bashCommand = "gadgetron_ismrmrd_client -f "+root_ext[0] + ".h5 -c Generic_Cartesian_Grappa_EPI_Thermo_5.0_simu.xml -o "+root_ext[0]+"out.h5"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        
        output_tmp = '/tmp/gadgetron/thermo/'
        files = []
        for i in os.listdir(output_tmp):
            if os.path.isfile(os.path.join(output_tmp,i)) and 'buffer' in i and '.img' in i:
                files.append(i)
                
        #analyse (.img/ .hdr) to nifti         
        for file in files:
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
    parser = argparse.ArgumentParser(description='Script so useful.')
    parser.add_argument("-f", type=str)
    parser.add_argument("-d", type=str)

    args = parser.parse_args()
    opt_file = args.f
    opt_dir = args.d
    filenames = []
    
    if opt_file:
        if opt_file.endswith(".dat"):
            filenames.append(opt_file)
            print("File to convert : " + opt_file)

            

    if opt_dir:
        for file in os.listdir(opt_dir):
            if file.endswith(".dat") and not '3D' in file:
                filenames.append(opt_dir+file)
                
        if filenames:
            print("\n\nIn folder : "+ os.path.dirname(filenames[0])+ "\n\nFound " + str(len(filenames))+ " files to convert :\n   ")
            print(*[os.path.split(i)[1] for i in filenames], sep="\n    ")
            
    if filenames:
        convert(filenames)
        
    print("\nFinished conversion.")
