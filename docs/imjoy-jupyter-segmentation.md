
# Segmentation of cells and nuclei

**Resizing to speed up prediction**: segmentation speed depends on the image size. In our experience, resizing the images
can lead to a substantial speed-up. In case you resize the images, we implemented a post-processing
routine that will resize the predicted masks back to the original image size. 


This is done with the jupyter notebook `segmentation_cells_nuclei.ipynb`

1. Running the first code cell will import the user-interface.
   
2. Running the second code cell will display the user-interface. 
   
   ![](images/segmentation-interface.png "segmentation-ui")

   Here the following parameters can be set: 

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

3. Pressing the button `Segment data` will start the segmentation. When using CellPose for the first time, 
   the models for nuclear and cytoplasmic segmentations are downloaded. 
   
   The actual segmentation can take a while, depending on the numberof images that should be segmented 
   (and their size). Progress can be monitored in the tab `Log`.

   ![](images/segmentation-log.png "segmentation-log")

4. Once the segmentation is finished, results can be inspected in the lower part of the interface. 
   The dropdown menus allow to inspect the results for cell and nuclear segmentation. 

   ![](images/segmentation-results.png "segmentation-results") 
   
5. **Results** will be saved in the specified folder. For each image the following files, results files 
    with different suffices are created: 
    *  `flow_...`: these are the predicted distance maps of CellPose. They are an intermediate result, and
       not needed for most end-users. 
    *  `mask_...`: these contain the actual segmentation results. Each segmented cell or nuclei is a filled 
        object with a constant pixel value. If the images were resized during segmentation, the mask is scaled
        back up to the original image size. The actually obtained (smaller) mask is saved under the name `mask__rescale_...`.  
    *  `segmentation_...`: summary plot showing the input image, the predicted distance map, and the segmented
       objects. This plot is also shown in the interface. 