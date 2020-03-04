
## Preprocessing
Segmentation is done on 2D images. In this step, 3D images are transformed into
2D images by applying a projection. 

Preprocessing is done with the ImJoy plugin `PreProcess`. 
<a href="https://imjoy.io/#/app?w=cellpose&plugin=muellerflorian/segmentation:PreProcess@stable&upgrade=1" target="_blank">**Install from here.**</a>. 

1. Before running the plugin, you have to specify a few parameters. Note that you have to perform this 
   projection for each channel-type. This allows to use different projection methods for a channel. This can be set in the plugin interface, avaible after clicking on the arrow down next to the plugin name.

    <img src="img\imjoy-preprocess-ui.png" width="600px"></img>

    Here the following parameters can be set. 

    Option           | Type | Default     | Description
    ---------------- | ---- | ----------- | -----------
    `Path DATA`    | str  |  | Full path to folder containing data to be segmented.
    `Path SAVE` | str  |  | Full path to folder where results should be stored.
    `Channel string`    | str  |  dapi | Unique string to identify channel that should be processed.
    `Projection type`    | str  |  mean | Different projection types: `max`, `mean`, `indiv`. The option `indiv` implies that a z-stack is split into individual slices, stored in subfolder for each image. 


0. Pressing the button `PreProcess` will **start the pre-processing**. Progress 
    can be monitored in the plugin log, available by pressing on the `i` next to the plugin name.

0. **Results** will be saved in the specified folder. For each image a json file with 
    basic properties of the file, and an image with the same name as the original one will be saved. 
