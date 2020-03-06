# Imports
import pathlib
from pathlib import Path
import json
import re
from skimage.io import imread, imsave
from skimage.transform import resize
import numpy as np


def log_message(msg, callback_fun=None):
    """ Display log, either terminal or any callback accepting a string as input.

    Parameters
    ----------
    msg : [string]
        [description]
    callback_fun : [type], optional
        [description], by default None
    """
    if callback_fun:
        callback_fun(msg)
    else:
        print(msg)

# Create new output path
def create_output_path(path_orig, str_replace, subfolder='', create_path=True, callback_log=None):
    """ Allows to create new path object by replacing a string in a provided path object.
    
    Parameters
    ----------
    path_orig : pathlib object
        Original file-name.
    str_replace : str
        str defining the replacement operation: 'str_orig>>str_new',
        where 'str_orig' is the orginal string, 'str_new' is the new string.
        For example, 'acquisition>>analysis'.
    subfolder : str or pathlib object
        Subfolder that should be added to new file-name
    create_path : bool
        Create new path if it doesn't exist.
    callback_log : str
        Callback function to be used. If None, then system print will be used.
    
    Returns
    -------
    pathlib object
        New path.
    """
    
    log_message("Creating name to path to store data.", callback_fun = callback_log)
    
    if (re.search(">>", str_replace)):
        str_orig = re.search(r'^(.*)>>(.*)$', str_replace).group(1)
        str_rep = re.search(r'^(.*)>>(.*)$', str_replace).group(2)

        path_replace = Path(str(path_orig).replace(str_orig,str_rep))
        path_replace = path_replace / subfolder
        log_message(f'Replacement parameters found: original string: {str_orig}, replacement string: {str_rep}', callback_fun = callback_log)
        log_message(f'Output path: {path_replace}', callback_fun = callback_log)

    else:
      log_message("No match", callback_fun = callback_log)
      return None
    
    # Create default folder to save data if none was defined by the user
    if create_path:
        if not path_replace.is_dir():
            path_replace.mkdir(parents=True)
   
    return path_replace 

# Functions
def folder_prepare_prediction(path_process, channel_ident, img_ext, path_save, projection_type, search_recursive=False, callback_log=None, callback_status=None, callback_progress=None):
    """[summary]
    
    Parameters
    ----------
    path_process : [type]
        [description]
    channel_ident : str
        [description]
    img_ext : str
        Image extension
    path_save : pathlin object or string
        Path to save results, 
        - If Pathlib object, then this absolute path is used.
        - If 'string' a replacement operation on the provided name of the data path will be applied (see create_output_path).
          And results will be stored in subfolder 'segmentation-input'
    projection_type : [type]
        [description]
    search_recursive : bool
        Recursively search folder, default: false. 
    callback_log : [type], optional
        [description], by default None
    callback_status : [type], optional
        [description], by default None
    callback_progress : [type], optional
        [description], by default None
    """


    # Use provided absolute user-path to save images.
    if isinstance(path_save, pathlib.PurePath):
        if not path_save.is_dir():
            path_save.mkdir(parents=True)
        path_save_settings = path_save
    
    else:
        path_save_str_replace =  path_save
        
    # How to look for files
    files_proc = []
    if search_recursive:
        for path_dapi in path_process.rglob(f'*{channel_ident}*{img_ext}'):
            files_proc.append(path_dapi)
    else:
        for path_dapi in path_process.glob(f'*{channel_ident}*{img_ext}'):
            files_proc.append(path_dapi)

    # Process files
    n_files = len(files_proc)
    for idx, file_proc in enumerate(files_proc):

        log_message(f'Processing file: {file_proc}', callback_fun = callback_status)

        if callback_progress:
            progress = float((idx+1)/n_files)
            callback_progress(progress)

        name_base = file_proc.stem

        # Create new output path if specified
        if not isinstance(path_save, pathlib.PurePath):
            path_save = create_output_path(file_proc.parent, path_save_str_replace, subfolder='segmentation-input', create_path=True)
            path_save_settings = path_save
            
        # Create subfolder when processing individual images
        if projection_type == 'indiv':
            path_save_indiv = path_save / name_base
            
            if not path_save_indiv.is_dir():
                path_save_indiv.mkdir(parents=True)
                path_save_settings = path_save_indiv
                
        # Open image
        print(file_proc)
        img = imread(str(file_proc))

        img_properties = {
                            "file_process": str(file_proc),
                            "img_name": file_proc.name,
                            "img_path": str(file_proc.parent),
                            "channel_ident": channel_ident,
                            "projection_type": projection_type
        }

        name_json = path_save_settings / f'img-prop__{name_base}.json'
        with open(name_json, 'w') as fp:
            json.dump(img_properties, fp, sort_keys=True, indent=4)

        # Process depending specified option
        if projection_type == 'indiv':

            for i in range(img.shape[0]):
                name_save = path_save_indiv / f'{name_base}_Z{str(i+1).zfill(3)}.png'
                if name_save.is_file():
                    log_message(f'File already exists. will be overwritten {name_save}', callback_fun = callback_log)
                imsave(name_save, img[i, :, :])

        else:

            if projection_type == 'mean':
                img_proj = img.mean(axis=0)

            elif projection_type == 'max':
                img_proj = img.mean(axis=0)

            name_save = path_save / f'{name_base}.png'

            if name_save.is_file():
                log_message(f'File already exists. will be overwritten {name_save}', callback_fun = callback_log)
            imsave(name_save, img_proj.astype('uint16'))
