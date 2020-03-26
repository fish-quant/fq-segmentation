
This repository provides wrapper code for the **segmentation of cells and nuclei**. 

* The actual **segmentation** is performed with the [**Cellpose package**](https://github.com/mouseland/cellpose).
* We provide **convenient wrappers** to apply this approach in batch mode to a large number of images.
* We provide **pre- and post-processing** routines to prepare images for segmentation and extract further information, e.g. distance measurements for objects.  

!!! example "Example of **nuclear segmentation** and **cytoplasmic segmentation**"
    ![segmentation__nuclei](img/segmentation__nuclei.png)
    ![segmentation__cells](img/segmentation__cells.png)




