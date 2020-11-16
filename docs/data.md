# Data

Please note that we recommend a **data organization**, described below, to facilitate the usage of these tools. 

We provide test data, which allows you to inspect how the data is organized, but then also run a local installation
of these tools to see if everything works correctly.

## Test data
Already processed test data can be downloaded from [**Dropbox**](https://www.dropbox.com/sh/yr1s5olqwkvyx0i/AADH0QQtdNuWWq7z9wgQpLiOa?dl=0). With these data, you can verify if the different analysis steps are properly executed.

## Data organization
We strongly recommend the following data-organization on which this workflow has been tested.

1. Images are store as single-channel multi-z-stack tif files, e.g on tif per position and channel. If your data are not single-channel, see the section on how to split channels with [Fiji](workflows-fiji-split-channels.md).
2. All raw 3D images are stored in a folder `acquisition`
3. All analysis results are stored in subfolder `analysis`, where each analysis step has a separate subfolder.

The organization of the provided test data is the following

```
├─ example_data/
│  ├─ acquisition                          # Folder with raw data
│  │  ├─ test_pos001_cy3.tif
│  │  ├─ test_pos002_dapi.tif
│  │  ├─ test_pos002_cy3.tif
│  │  ├─ test_pos002_dapi.tif
│  ├─ analysis                              # Folder with all analysis results
│  │  ├─ segmentation-input                 # Folder with projected images for segmentation 
│  │  │  ├─ img-prop__test_pos001_cy3.json  # json file with image properties
│  │  │  ├─ test_pos001_cy3.png             # Projected image
│  │  │  ├─ ....
│  │  ├─ segmentation-results               # Folder with segmentation results 
│  │  │  ├─ test_pos001_cy3.tif
│  │  │  ├─ test_pos001_cy3.tif
│  │  │  ├─ test_pos001_cy3.tif
│  │  │  ├─ ....
│  │  ├─ ....
│  │  ├─ FQ_outline                         # [Optional] FQ outlines 
│  │  │  ├─ test_pos001_cy3_outline.txt
│  │  │  ├─ ....
```

