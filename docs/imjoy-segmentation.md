
# Segmentation of cells and nuclei

Preprocessing is done with the ImJoy plugin `SegmentCellsNuclei`. 
<a href="https://imjoy.io/#/app?w=cellpose&plugin=muellerflorian/segmentation:SegmentCellsNuclei@stable&upgrade=1" target="_blank">**Install from here.**</a>. 


**Resizing to speed up prediction**: segmentation speed depends on the image size. In our experience, resizing the images
can lead to a substantial speed-up. In case you resize the images, we implemented a post-processing
routine that will resize the predicted masks back to the original image size. 

   
1. Before running the plugin, you have to specify a few parameters. This can be done in the plugin interface, 
   avaible after clicking on the arrow down next to the plugin name.. 
   
   <img src="img\imjoy-segment-cells-nuclei-ui.png" width="600px"></img>

   Here the following parameters can be set: 

    Option           | Type | Default     | Description
    ---------------- | ---- | ----------- | -----------
    `Path DATA`    | str  |  | Full path to folder containing data to be segmented.
    `Path SAVE` | str  |  | Full path to folder where results should be stored.
    `String CELLS`    | str  |  cy3 | Unique identifier for images of cytoplasmic stain.
    `String NUCLEI`    | str  |  dapi | Unique identifier for images of nuclear stain.
    `String img ext`     | str  | .png | File extension of images that should be segmented.
    `Size CELLS`     | int  | 100 | Typical size of a cell (in resized image).
    `Size NUCLEI`     | int  | 50 | Typical size of a nucleus (in resized image).
   `New size`     | str  | 512, 512 | String to specify new size of image. No resizing if empty.

0. Pressing on the plugin name `SegmentCellsNuclei` will start the segmentation. 
   When using CellPose for the first time, the models for nuclear and cytoplasmic segmentations are downloaded. 
   
   The actual segmentation can take a while, depending on the numberof images that should be segmented 
   (and their size). Progress will be displayed in the ImJoy status bar, and more details provided in the
   plugin log available by pressing on the `i` next to the plugin name. 

   Once a image is segmented, the results will be saved (see below). So you can monitor the result folder 
   to verify on the fly if the segmentation works. 

   
0. **Results** will be saved in the specified folder. For each image the following files, results files 
    with different suffices are created: 
    *  `flow_...`: these are the predicted distance maps of CellPose. They are an intermediate result, and
       not needed for most end-users. 
    *  `mask_...`: these contain the actual segmentation results. Each segmented cell or nuclei is a filled 
        object with a constant pixel value. If the images were resized during segmentation, the mask is scaled
        back up to the original image size. The actually obtained (smaller) mask is saved under the name `mask__rescale_...`.  
    *  `segmentation_...`: summary plot showing the input image, the predicted distance map, and the segmented
       objects. This plot is also shown in the interface. 