
# %% Imports 
from pathlib import Path
import utils_segmentation  # Either on sys path or pip installed



# %% Function call

# Parameters
path_process = Path(r'D:\Documents\Data\test-data\cell-pose\jupyter-tests\example_data\acquisition')
path_save = Path(r'D:\Documents\Data\test-data\cell-pose\jupyter-tests\example_data\analysis\segmentation-input-workflow')
channel_ident = 'dapi'          # Identifier of channel that should be pre-processed 
projection_type = 'max'         # Projection type (mean, max, indiv)

# Call pre-processing function
utils_segmentation.folder_prepare_prediction(
                    path_process=path_process,
                    search_type=None,
                    channel_ident=channel_ident,
                    projection_type=projection_type,
                    path_save=path_save,
                    callback_log=None)
