


# Overview
This repository provides wrapper code to use the generalist cell/nuclei segmentation package [**Cellpose**](https://github.com/mouseland/cellpose). 

Two main functionalities are provided:
1. Prepare z-stacks for segmentation by performing z-stack projections.
2. Provide convenient interface to batch segment a large number of images.


- [Overview](#overview)
- [Installation](#installation)
  - [Pyton with Miniconda](#pyton-with-miniconda)
  - [Create dedicated environment to run Cellpose](#create-dedicated-environment-to-run-cellpose)
  - [Installing cellpose](#installing-cellpose)
  - [Installing this package](#installing-this-package)
- [Data](#data)
  - [Data organization](#data-organization)
  - [Test data](#test-data)
- [Usage](#usage)
  - [Resizing can help to speed up prediction.](#resizing-can-help-to-speed-up-prediction)
  - [Working with Jupyter notebooks](#working-with-jupyter-notebooks)
  - [Preprocessing](#preprocessing)
  - [Performing segmentation of cells and nuclei](#performing-segmentation-of-cells-and-nuclei)


# Installation
The installation consists of the following steps

1. **Python**. Recommended with Miniconda:
0. Create a **dedicated environment** with Jupyter to run your code
0. Install **Jupyter lab** to run your code interactively.
0. Install **CellPose**
0. Install our code to provide wrappers to easily use CellPose.  
   

## Pyton with Miniconda
We recommend installing an [Miniconda distribution of Python](https://docs.conda.io/en/latest/miniconda.html): choose Python 3.7 and your operating system. 

We then recommend using the annoconda prompt that is availabel to excecute the different commands listed below. 
This guarantees that the necessary terminal scripts are available. 

## Create dedicated environment to run Cellpose
We recommend creating a dedicated environment to run Cellpose. To create an environment called `cellpose`, open an anaconda prompt and type. Note that you will also install jupyter, which will allow 
to run the jupyter notebooks for easier execution (confirm with `y` when asked if you want to proceed): 

```
conda create --name cellpose python=3.7 jupyter
```

Then activate your environment (Note you will always have to run conda activate cellpose before you run cellpose):
```
conda activate cellpose --upgrade
```


## Installing cellpose
From your `cellpose` environment, install Cellpose and its dependencies with
```
pip install cellpose
```

## Installing this package
TODO create setup.py

From your `cellpose` environment, install this package its dependencies with
TODO: update to master branch once committed.
```
pip install git+https://github.com/muellerflorian/segmentation/develop --upgrade
```

# Data

## Data organization
We strongly recommend the following data-organization on which this workflow has been tested.
1. Images are store as single-channel multi-z-stack tif files, e.g on tif per position and channel.
2. All raw 3D images are stored in a folder `acquisition`
3. All analysis results are stored in subfolder `analysis`, where each analysis step has a separate subfolder.

The organization of the provided test data is the following

```
├─ example_data/
│  ├─ acquisition                 # Folder with raw data
│  │  ├─ test_pos001_cy3.tif
│  │  ├─ test_pos002_dapi.tif
│  │  ├─ test_pos002_cy3.tif
│  │  ├─ test_pos002_dapi.tif
│  ├─ analysis                    # Folder with all analysis results
│  │  ├─ for-segmentation         # Folder with projected images for segmentation 
│  │  │  ├─ img-prop__test_pos001_cy3.json   # json file with image properties
│  │  │  ├─ test_pos001_cy3.png              # Projected image
│  │  │  ├─ ....
│  │  ├─ segmentation             # Folder with segmentation results 
│  │  │  ├─ test_pos001_cy3.tif
│  │  │  ├─ test_pos001_cy3.tif
│  │  │  ├─ test_pos001_cy3.tif
│  │  │  ├─ ....
```

## Test data

# Usage

## Resizing can help to speed up prediction. 
Segmentation speed depends on the size of images. In our experience, resizing the images
can lead to a substantial speed-up. In case you resize the images, we implemented a post-processing
routine that will resize the predicted masks back to the original image size. 

## Working with Jupyter notebooks
Jupyter notebooks provide a convenient way to execute code with minimal user input. 
We further provide notebooks with interactive control, to faciliate ussage. 

Code is divided into code-cells (two in the example below). 
The currently enabled cell (the first one in the example below) is shown with a blue frame. 
It can be execude by pressing `SHIFT+ENTER`

![](images/jupyer-code-cell.png "jupyter-code-cell")


## Preprocessing
Segmentation is done on 2D images. In this step, 3D images are transformed into
2D images by applying a projection. 

This is done with the jupyter notebook `preprocessing.ipynb`

1. Running the first code cell will import the user-interface.
   
2. Running the second code cell will display the user-interface. 
   
   Note that you have to perform this projection for each channel-type. This allows
   to use different projection methods for a channel.

   Here the following parameters can be set: 

    ![](images/preprocess-ui.png "preprocess-ui")

    Option           | Type | Default     | Description
    ---------------- | ---- | ----------- | -----------
    `Data path`    | str  |  | Full path to folder containing data to be segmented.
    `Results path` | str  |  | Full path to folder where results should be stored.
    `Channel str`    | str  |  dapi | Unique string to identify channel that should be processed.
    `Projection`    | str  |  mean | Different projection types: mean, max, indiv. Indiv implies that z-stack is split into individual slices. 


3. Pressing the button `Pre-process data` will start the segpre-processing. Progress 
    can be monitored in the tab `Log`.

4. Once the segmentation is finished, results can be inspected in the lower part of the interface. 
   The dropdown menus allow to inspect the results for cell and nuclear segmentation. 

    ![](images/preprocess-result.png "preprocess-result")


5. **Results** will be saved in the specified folder. For each image a json file with 
    basic properties of the file, and an image with the same name as the original one will be saved. 



## Performing segmentation of cells and nuclei
This is done with the jupyter notebook `segmentation_cells_nuclei.ipynb`

1. Running the first code cell will import the user-interface.
   
2. Running the second code cell will display the user-interface. 
   Here the following parameters can be set: 

    ![](images/segmentation-interface.png "segmentation-ui")

    Option           | Type | Default     | Description
    ---------------- | ---- | ----------- | -----------
    `Data path`    | str  |  | Full path to folder containing data to be segmented.
    `Results path` | str  |  | Full path to folder where results should be stored.
    `String cells`    | str  |  cy3 | Unique identifier for images of cytoplasmic stain.
    `String nuclei`    | str  |  dapi | Unique identifier for images of nuclear stain.
    `New size`     | str  | 512, 512 | String to specify new size of image. No resizing if empty.
    `Image ext`     | str  | .png | File extension of images that should be segmented.
    `Size cells`     | int  | 100 | Typical size of a cell (in resized image).
    `Size nuclei`     | int  | 50 | Typical size of a nucleus (in resized image).

3. Pressing the button `Segment data` will start the segmentation. Depending on the number
    of images that should be segmented (and their size), this can take a while. Progress 
    can be monitored in the tab `Log`.

    ![](images/segmentation-log.png "segmentation-log")

4. Once the segmentation is finished, results can be inspected in the lower part of the interface. 
   The dropdown menus allow to inspect the results for cell and nuclear segmentation. 

    ![](images/segmentation-results.png "segmentation-results") 
   
5. **Results** will be saved in the specified folder. For each image the following files, results files 
    with different suffices are created: 
    *  `flow_...`: these are the predicted distance maps of CellPose. They are an intermediate result, and
       not needed for most end-users. 
    *  `flow_...`: these contain the actual segmentation results. Each segmented cell or nuclei is a filled 
        object with a constant pixel value.
    *  `segmentation_...`: summary plot showing the input image, the predicted distance map, and the segmented
       objects. This plot is also shown in the interface. 
