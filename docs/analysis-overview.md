
## Typical workflows
For most purposes, the segmentation will consist of two steps. Each of these steps is described in a 
dedicated section. In this section you can also find a recommended workflow, which allows you to also
process the test data. 

1. **Pre-processing** of the data: segmentation is performed on 2D images. If your images are 3D, you have to either split them, or project them into 2D images. This can be done with the [pre-processing workflow](analysis-preprocessing.md).
2. **Actual segmentation** of your images. We provide different plugins to [**segment**](analysis-segmentation.md). one type of structure, e.g. nuclei or cells, or two, e.g. cells and nuclei.

Each **workflow** is documented in a dedicated section. We provide

* **Installation links**.
* Detailed explanations of the different **parameters**.
* A **Recommended workflow** for how to set the parameters following the recommended data organization.  

## ImJoy plugins
Most of the workflows are implemented as **ImJoy plugins**, with a simple interface to
specify the different workflow parameters. We describe in a dedicated [sections] how to [**use**](imjoy-overview.md) and  [**install**](imjoy-installation.md) the **Plugin engine** to run these plugins. 

Once a plugin is installed, it will be available for later use in the ImJoy **workspace `fq-segmentation`** as explained [here](imjoy-overview.md#opening-a-workspace). 

!!! abstract "Quick summary for how to connect ImJoy to Jupyter engine"
    1. Open **anaconda terminal**. 
    2. **Activate environment**: `conda activate fq-segmentation`
    3. **Start Jupyter engine**: `imjoy --jupyter`
    4. **Connect** ImJoy to Jupyter Engine with 🚀 button.

We also provide **Jupyter notebooks** for these workflows, which we recommend only for more experienced Python users. 

