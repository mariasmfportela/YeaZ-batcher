This script is used to analyse yeast fluorescent microscopy images by performing segmentation, fluorescence value extraction and plotting results.

The segmentation code is adapted from https://github.com/rahi-lab/YeaZ-GUI, but code was cleaned-up to remove the GUI components and use only the CNN segmentation model.

INSTALLATION
Create an environment using the provided environment.yml file (https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file). 

Alternativelly create a virtual environment in the command line with python 3.9 (conda create -n myenv python=3.9), then activate the environment (conda activate myenv) and install the necessary packages from the requirements.txt file (pip install -r requirements.txt).

DIRECTORY STRUCTURE
The code assumes the following directory structure:

├── root
    ├── analysis_scripts
    |   ├── disk
    |   ├── unet
    |   ├── utils
    |   ├── microscopy_analysis.ipynb
    |   ├── readme.txt
    ├── replicate1
    |   ├── sample1-bright.tif
    |   ├── sample1-BFP.tif
    |   ├── sample1-GFP.tif
    |   ├── sample1-RFP.tif
    |   ├── (etc. for other samples)
    ├── (etc. for other replicates)
    
    
The .tif files containing each image channel can be generated with the ImageJ macro "split_and_save".
Important: ensure that comparable samples in different replicate folders have exactly the same file names!

