#!/usr/bin/python3

import sys
import numpy as np
import argparse
import os
import subprocess
import slicer 






def load(filenames):
    for filename in filenames:
        
        sequenceNode = slicer.util.loadNodeFromFile(filename, "SequenceFile", {"show": True})
        browserNode = slicer.modules.sequences.logic().GetFirstBrowserNodeForSequenceNode(sequenceNode)        
        volumeNode = browserNode.GetProxyNode(sequenceNode)
        disp = volumeNode.GetDisplayNode()
        disp.SetAndObserveColorNodeID("vtkMRMLColorTableNodeFileColdToHotRainbow.txt")
        disp.SetAutoWindowLevel(0)
        disp.SetWindowLevelMinMax(0,20)

    # Show sequence browser toolbar
    slicer.modules.sequences.showSequenceBrowser(browserNode)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script so useful.')
    parser.add_argument("-f", type=str, nargs="+", help="Indicate filepaths to be converted (seperated with a ' ' if many).")
    parser.add_argument("-d", type=str,  help="Indicate path folder where file will be converted.")
    parser.add_argument("-s", type=str, nargs="+",  help="Key words to select specific files to convert in a directory. Logical function between keywords : AND.")

    args = parser.parse_args()
    opt_file = args.f
    opt_dir = args.d
    opt_select = args.s
    filenames = []
    
    if opt_file:
        for file in opt_file:
            if file.endswith(".nrrd"):
                filenames.append(file)


    if opt_dir:
        for file in os.listdir(opt_dir):
            if file.endswith(".nrrd"):
                if opt_select:
                    if all(selection in file for selection in opt_select):
                        filenames.append(opt_dir+file)
                else:
                    filenames.append(opt_dir+file)

                
            
    if filenames:
        load(filenames)
        
