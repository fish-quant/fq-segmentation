
# %% Imports 
from pathlib import Path
import utils_cellpose  # Either on sys path or pip installed


# %% Function call
importlib.reload(utils_cellpose)

# Parameters
path_scan = Path(r'paste-path-to-data')            # For example data: example_data\analysis\segmentation-input
path_save = Path(r'paste-path-to-save-results')    # For example data: example_data\analysis\segmentation-results
str_cyto = 'cy3'            # Identifier of channel for cytoplasmic segmentation
str_nuclei = 'dapi'         # Identifier of channel for nuclear segmentation
img_ext = '.png'            # Extension of images to be segmented
new_size = (512, 512)       # Size of images (when resize should be applied, empty tuple otherwise)

size_cells = 100            # Typical size (diameter) of cells
size_nuclei = 50            # Typical size (diameter) of nuclei

# Call segmentation function
utils_cellpose.segment_cells_nuclei_indiv(path_scan=path_scan, 
                                strings=(str_cyto, str_nuclei), 
                                img_ext=img_ext, 
                                new_size=new_size,
                                sizes=(size_cells, size_nuclei), 
                                models=('cyto','nuclei'),
                                path_save=path_save)

