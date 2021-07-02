#!/usr/bin/python3

import sys
import numpy as np
import nibabel as nb
import argparse
import os


def convert(filename):
    img = nb.load(filename)
    dat = img.get_fdata()
    squeezed_dat = np.squeeze(dat)
    squeezed_dat.shape
    new_h = img.header.copy()
    new_nifti = nb.nifti1.Nifti1Image(squeezed_dat, None, header=new_h)
    nb.save(new_nifti, filename.replace('.img', '.nii'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script so useful.')
    parser.add_argument("-f", type=str, help="Indicate filepaths to be converted (seperated with a ' ' if many).")
    parser.add_argument("-d", type=str)

    args = parser.parse_args()
    opt_file = args.f
    opt_dir = args.d

    if opt_file:
        if opt_file.endswith(".img"):
            convert(opt_file)
            print(opt_file + " converted.")

    if opt_dir:
        print(opt_dir)
        for file in os.listdir(opt_dir):
            if file.endswith(".img"):
                convert(opt_dir+file)
                print(opt_dir+file + " converted.")

    print("Finished conversion from ALANYZE to NIFTI.")
