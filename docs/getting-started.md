# Getting started

## Data
Please note that we recommend a **data organization**, described [here](data.md), to facilitate the usage of these tools. 
We provide test data, which allows you to inspect how the data is organized, but then also run a local installation
of these tools to see if everything works correctly.

## Typical workflow
For most purposes, the segmentation will consist of two steps. Each of these steps is described in a 
dedicated section. In this section you can also find a recommended workflow, which allows you to also
process the test data. 

1. **Pre-processing** of the data: segmentation is performed on 2D images. If your images are 3D, you have to either split them, or project them into 2D images. This can be done with the [pre-processing workflow](imjoy-preprocessing.md).
2. **Actual segmentation** of your images. We provide different plugins to segment one type of structure, e.g. nuclei or cells, or two, e.g. cells and nuclei.

## ImJoy plugins
Most of the workflows are implemented as **ImJoy plugins**, with a simple interface to
specify the different workflow parameters. Below we describe how to **use ImJoy** and the
**Plugin engine** to run these plugins. 

!!! abstract "Quick summary for how to connect ImJoy to Jupyter engine"
    1. Open **anaconda terminal**. 
    2. **Activate environment**: `conda activate fq-segmentation`
    3. **Start Jupyter engine**: `imjoy --jupyter`
    4. **Connect** ImJoy to Jupyter Engine with 🚀 button.

We also provide **Jupyter notebooks** for these workflows, which we recommend only for more experienced Python users. 