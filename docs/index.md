
This repository provides convience wrapper code for the **segmentation of cells and nuclei**. 

!!! example "Example of **nuclear segmentation** and **cytoplasmic segmentation**"
    ![segmentation__nuclei](img/segmentation__nuclei.png)
    ![segmentation__cells](img/segmentation__cells.png)

__How to get started:__

1. Read this documentation.
2. Install the ImJoy plugin engine (we explain what this is just a bit further down).
3. Install the FISH-quant plugins.
4. Try to analyze the provided test data.

## Python? ImJoy? Plugin engine?

For new users it might be a bit confusing how the different software packages work together. We hence provide here a small overview of hwo the different pieces work together. 

There are three  essential parts

![fq-get-version.gif](img/segmentation-overview.png){: style="width:500px"}

* **Python**: Python code performing the actual analysis in two essential parts
  1. The actual **segmentation** is performed with the [**Cellpose package**](https://github.com/mouseland/cellpose).
  2. We provide additional Python code allow to pre/post process images, and perform batch processing:
     * We provide **convenient wrappers** to apply this approach in batch mode to a large number of images.
     * We provide **pre- and post-processing** routines to prepare images for segmentation and extract further information, e.g. distance measurements for objects.  

* **ImJoy**: ImJoy is a plugin powered computing platform to deploy advanced image analysis tools. Here, we provide as a set of such plugins. Plugins can be installed with a simple installation link. More details about ImJoy and how it can be installed, can be found in the decicated overview section.
* **Plugin Engine**: the ImJoy app is running in your webbrowser (prefereably Chrome). In order to perform computations, you have to install a 
so-called plugin engine. ImJoy can connect to such an engine, and launch data processing tasks. Importantly, this engine can run locally or remotely, but the ImJoy interface will always be the same. YOu have to install this engine once. Each time you want to use FISH-quant, you have to launch it and connect ImJoy to this engine.


## Reporting bugs

If you encounter a bug, best is to create a [**GitHub issue**](https://github.com/fish-quant/segmentation/issues). This would allow other users to see 
reported bugs and proposed solutions. If possible, please provide the following information

1. **How** can bug be produced?
2. Which **browser** and version are you using?
3. **Complete plugin log**. Can be obtained by clicking on the `i` next to the FISH-QUANT plugin. Please copy to a text file. This will also contain the version of the plugin and the used code
    ```
    Loading plugin SegmentCellsNuclei_i862g1602770955978 (TAG=stable,  WORKSPACE=fq-segmentation)
    ENGINE_URL=http://127.0.0.1:9527/
    Setting up plugin.

    Plugin SegmentCellsNuclei initialized
    * plugin version: 0.1.11
    * segwrap version: 0.1.7
    * utils_cellpose location: c:\users\muellerf\miniconda3\envs\fq-segmentation\lib\site-packages\segwrap\utils_cellpose.py
    ```
4. **Console log**. The console log of the browser provides further details that can help for debugging. To acces the console log in **Chrome**:

      1. In the ImJoy app mouse-right-click.
      2. Select `Inspect`.
      3. This will open a new interface on the right size of your browser windows. Select the panel `Console` and copy the entire content, and paste it to a file.  

## Development team

* Florian Mueller. [Github](https://github.com/muellerflorian).
