To convert raw data .dat into .h5/.img..nii and.nrrd 

**/!\ Nifti conversion doesn't take care of orientation and position (need to be done)**

# Dependencies :
slicer 
nibabel
numpy
argparse
siemens_to_ismrmrd
gadgetron : the pipeline uses gadgetron to reconstruct images


#Paths to indicate in config.py :
GADGETRON_XML_NAME : name of the gadegtron xml config used for reconstruction
SIEMENS_TO_ISMRMRD_CONFIG_NAME  : name of siemens_to_ismrmrd confid (.xml) (ex: "IsmrmrdParameterMap_Siemens.xml")
SIEMENS_TO_ISMRMRD_PARAMETER_MAP_NAME : name of siemens_to_ismrmrd paramater map (.xsl) (ex: "IsmrmrdParameterMap_Siemens_EPI_PF_PreZeros.")
SLICER_EXECUTABLE_PATH  :  path to slicer (ex : "/home/manondesclides/Dev/Slicer-4.11.20210226-linux-amd64/Slicer")



# To convert from .dat to .nrrd
- In terminal : go to the folder conversion_thermo
- $ python3 siemens_to_nrrd.py  -d DIRECTORY_PATH_TO_CONVERT 
				-f FILE(S)_PATH(S)_TO_CONVERT
				-s KEY WORDS to select specific files to load  in slicer
				--load option if you want your data to ba loaded in slicer after conversion
				--rewrite if you want to erase exsiting converted files and write new ones (it doesn't rewrite if not specified)

# To convert from .dat to .nii 
You can do te same thing with the file siemens_to_nifti.py 
but may have some bugs

# To convert .nii to .nrrd 
Use the file nifti_to_nrdd.py and follow instructions

# To convert .img/.hdr (analyze format) to nifti:
use analyze_to_nifti.py

#TO LOAD .nrrd SEQUENCES in SLICER in a folder and with PRE-DISPLAY PARAMETERS for THERMO
launch : load_nrrd_slicer.py in terminal indicated your folder path with -d or your files paths with -f and select specific data like thermo to display



**Example of usage**

In 'conversion_thermo' folder :

$ python3 siemens_to_ismrmrd.py -d /home/manon/Data/test --load -s temperature_all 

In this case, all data in test folder are converted, an only .nrrd file containing 'temperature_all' in their name are load automatically in 3Dslicer 


$ python3 load_nrrd_slicer.py -d /home/manon/Data/test -s temperature_all 

In this case, only .nrrd file in test folder containing 'temperature_all' in their name are load automatically in 3Dslicer 



$ python3 load_nrrd_slicer.py -f /home/manon/Data/test/thermo_test_1_temperature_all.nrrd /home/manon/Data/test/thermo_test_2_temperature_all.nrrd 

In this case,  thermo_test_1_temperature_all.nrrd and thermo_test_2_temperature_all file are load automatically in 3Dslicer 
