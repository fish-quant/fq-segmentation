


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
  - [Working with Jupyter notebooks](#working-with-jupyter-notebooks)
  - [Preprocessing](#preprocessing)
  - [Performing segmentation of cells and nuclei](#performing-segmentation-of-cells-and-nuclei)
  - [IPWYDGETS](#ipwydgets)


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
to run the jupyter notebooks for easier execution: 

```
conda create --name cellpose python=3.7 jupyter
```

Then activate your environment (Note you will always have to run conda activate cellpose before you run cellpose):
```
conda activate cellpose
```


## Installing cellpose
From your `cellpose` environment, install Cellpose and its dependencies with
```
pip install cellpose
```

## Installing this package
TODO create setup.py

From your `cellpose` environment, install this package its dependencies with
```
pip install cellpose
```

# Data

## Data organization

```
├─ data_for_expression_gradient/
│  ├─ Sample_1
│  │  ├─ annotation.json
│  │  ├─ sample_1_green_outline_spots_181018.txt
│  │  ├─ sample_1_green.tif
│  │  ├─ sample_1_red.tif
│  ├─ Sample_2
│  │  ├─ ...
```

## Test data

# Usage

TODO: Resize can help

## Working with Jupyter notebooks

* Running cell: SHIFT+ENTER


## Preprocessing
Segmentation is done on 2D images. In this step, 3D images are transformed into
2D images by applying a projection. 



## Performing segmentation of cells and nuclei
This is done with the jupyter notebook `segmentation_cells_nuclei.ipynb`

1. Running the first code cell will import the user-interface.
   
2. Running the second code cell will display the user-interface. Here the following parameters can be
    set: 

    ![](images/segmentation-interface.png "segmentation-ui")

    Option           | Type | Default     | Description
    ---------------- | ---- | ----------- | -----------
    `Data path`    | str  |  | Full path to folder containing data to be segmented.
    `Results path` | str  |  | Full path to folder where results should be stored.
    `String cells`    | str  |  w3Cy3 | Unique identifier for images of cytoplasmic stain.
    `String nuclei`    | str  |  we2Hoechst | Unique identifier for images of nuclear stain.
    `New size`     | str  | 1024, 1024 | String to specify new size of image. No resizing if empty.
    `Image ext`     | str  | .png | File extension of images that should be segmented.
    `Size cells`     | int  | 100 | Typical size of a cell (in resized image).
    `Size nuclei`     | int  | 100 | Typical size of a nucleus (in resized image).

3. Pressing the button `Segment data` will start the segmentation. Depending on the number
    of images that should be segmented (and their size), this can take a while. Progress 
    can be monitored in the tab `Log`.

    ![](images/segmentation-log.png "segmentation-log")

4. Once the segmentation is finished, results can be inspected in the lower part of the interface. 
   The dropdown menus allow to inspect the results for cell and nuclear segmentation. 

    ![](images/segmentation-log.png "segmentation-results")

5. **Results** will be saved in the specified folder. For each image the following files, results files 
    with different suffices are created: 
    *  `flow_...`: these are the predicted distance maps of CellPose. They are an intermediate result, and
       not needed for most end-users. 
    *  `flow_...`: these contain the actual segmentation results. Each segmented cell or nuclei is a filled 
        object with a constant pixel value.
    *  `segmentation_...`: summary plot showing the input image, the predicted distance map, and the segmented
       objects. This plot is also shown in the interface. 
   

## IPWYDGETS
https://ipython-books.github.io/33-mastering-widgets-in-the-jupyter-notebook/


The ipywidgets package should be installed by default in Anaconda, but you can also install it manually with conda install ipywidgets.

Alternatively, you can install ipywidgets with pip install ipywidgets, but then you also need to type the following command in order to enable the extension in the Jupyter Notebook:

jupyter nbextension enable --py --sys-prefix widgetsnbextension

