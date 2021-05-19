# Segmentation

We provide different plugins for different segmentation tasks:

* Install plugin `SegmentObjects` to segment cells OR nuclei <a href="https://imjoy.io/#/app?w=fq-segmentation&plugin=fish-quant/fq-segmentation:SegmentObjects@stable&upgrade=1" target="_blank">**from here.**</a>
* Install plugin  `SegmentCellsNuclei` to segment cells AND nuclei <a href="https://imjoy.io/#/app?w=fq-segmentation&plugin=fish-quant/fq-segmentation:SegmentCellsNuclei@stable&upgrade=1" target="_blank">**from here.**</a>

## General behavior

### Recursive search

The plugins will search [**recursively**](analysis-general-behavior.md#recursive-search-for-data) the provided subfolder for images to segment.

By default, all images matching the naming scheme will be processed. An optional parameter allows to specify
in which subfolder the images have to be in order to be segmented. This allows to process nested folder
hierachies and only segmenting images in the relevant subfolders.

As an example, in the provided data we could specif the folder `example_data\analysis` as the data folder. 
This would then scan this folder and all subfolders and potentially find inappropriate files for segmentation.
By defining the `Input subfolder` to be `segmentation-input`, the analysis will be restricted to this folder. 

### Results

Results will be saved in the specified folder. For each image the following files, results files with different prefixes are created:

* `flow_ ...`: these are the predicted distance maps of CellPose. They are an intermediate result, and
     not needed for most end-users.
* `mask_ ...`: these contain the actual segmentation results. Each segmented object is a filled 
      object with a constant pixel value. If the images were resized during segmentation, the mask is scaled
      back up to the original image size. The actually obtained (smaller) mask is saved under the name `mask__rescale_...`.  
* `seg_...`: summary plot showing the input image, the predicted distance map, and the segmented
     objects. This plot is also shown in the interface.

![segmentation__nuclei](img/segmentation__nuclei.png)

## Recommended workflow

The default settings of the plugins allow to quickly perform the recommended workflow. You only have 
to paste your data folder.  

1. 2D images are stored in a subfolder  `segmentation-input`
2. Segmentation results will be stored in a subfolder `segmentation-results`, this can be achieved by setting
    the save path to the string replacement  `segmentation-input>>segmentation-results`

## Segmentation of nuclei OR cells

![imjoy-segment-objects-ui](img/imjoy-segment-objects-ui.png){: style="width:300px"}

1. Before running the plugin, you have to **specify a few parameters**. This can be done in the plugin interface, 
    avaible after clicking on the arrow down next to the plugin name.

    Here the following parameters can be set:

    Option           | Type | Default     | Description
    ---------------- | ---- | ----------- | -----------
    `Path DATA`    | str  |  | Full path to folder containing data to be segmented.
    `Input subfolder`    | str  |  | Name of the subfolder containing the images that should be segmented.
    `Path SAVE` | str  |  | Several options exist. See dedicated section [below](analysis-general-behavior.md#specify-folder-to-save-your-data) for more details.
    `String channel`    | str  |  `dapi` | Unique identifier to identify channel.
    `Object name`    | str  |  `nuclei` | How the object is called.
    `Cellpose model`    | str  |  `nuclei` | Cellpose model for segmentation: `cyto` or `nuclei`. Note that for dense nuclei, the cytoplasmic model might work better. 
    `Object diameter`     | int  | 50 | Typical diameter of the object. Better to be set a bit to small.
    `Net Average`     | Bool  | False | Can improve segmentation accuracy, but is slower (Runs the 4 built-in networks and averages them).
    `Resample`     | Bool  | False | Gives more accurate boundaries, but can be very slow (Runs dynamics at original image size).
    `String img ext`     | str  | `.png` | File extension of images that should be segmented.

2. Pressing on the plugin name `SegmentObjects` will start the segmentation.
    When using CellPose for the first time, the models for nuclear and cytoplasmic segmentations are downloaded. 

    The actual segmentation can take a while, depending on the numberof images that should be segmented 
    (and their size). Progress will be displayed in the ImJoy status bar, and more details provided in the
    plugin log available by pressing on the `i` next to the plugin name.

    Once a image is segmented, the results will be saved (see below). So you can monitor the result folder 
    to verify on the fly if the segmentation works.

## Segmentation of cells AND nuclei

![imjoy-segment-cells-nuclei-ui](img/imjoy-segment-cells-nuclei-ui.png){: style="width:300px"}

1. Before running the plugin, you have to **specify a few parameters**. This can be done in the plugin interface, 
    avaible after clicking on the arrow down next to the plugin name.

    Here the following parameters can be set:

    Option           | Type | Default     | Description
    ---------------- | ---- | ----------- | -----------
    `Path DATA`    | str  |  | Full path to folder containing data to be segmented.
    `Input subfolder`    | str  |  | Name of the subfolder containing the images that should be segmented.
    `Path SAVE` | str  |  | Path to folder where results should be stored (for more details see above).
    `String CELLS`    | str  |  `cy3` | Unique identifier for images of cytoplasmic stain.
    `String NUCLEI`    | str  |  `dapi` | Unique identifier for images of nuclear stain.
    `String img ext`     | str  | `.png` | File extension of images that should be segmented.
    `Size CELLS`     | int  | 100 | Typical size of a cell (in resized image).
    `Size NUCLEI`     | int  | 50 | Typical size of a nucleus (in resized image).
    `Net Average`     | Bool  | False | Can improve segmentation accuracy, but is slower (Runs the 4 built-in networks and averages them).
    `Resample`     | Bool  | False | Gives more accurate boundaries, but can be very slow (Runs dynamics at original image size).
    `String img ext`     | str  | `.png` | File extension of images that should be segmented.

2. Pressing on the plugin name `SegmentCellsNuclei` will start the segmentation. 
    When using CellPose for the first time, the models for nuclear and cytoplasmic segmentations are downloaded.

    The actual segmentation can take a while, depending on the numberof images that should be segmented 
    (and their size). Progress will be displayed in the ImJoy status bar, and more details provided in the
    plugin log available by pressing on the `i` next to the plugin name.

    Once a image is segmented, the results will be saved (see below). So you can monitor the result folder 
    to verify on the fly if the segmentation works.
