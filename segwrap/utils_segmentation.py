# Imports
from pathlib import Path
import json
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


# Functions
def folder_prepare_prediction(path_process, search_type, channel_ident, path_save, projection_type, callback_log=None, callback_status=None, callback_progress=None):
    """[summary]

    Parameters
    ----------
    path_process : [type]
        [description]
    channel_ident : [type]
        [description]
    path_save : [type]
        [description]
    projection_type : [type]
        [description]
    """

    # Create default folder to save data if none was defined by the user
    if not path_save.is_dir():
        path_save.mkdir(parents=True)
    path_save_settings = path_save

    # How to look for files
    files_proc = []
    if search_type == "recursive":
        for path_dapi in path_process.rglob(f'*{channel_ident}*'):
            files_proc.append(path_dapi)
    else:
        for path_dapi in path_process.glob(f'*{channel_ident}*'):
            files_proc.append(path_dapi)

    # Process files
    n_files = len(files_proc)
    for idx, file_proc in enumerate(files_proc):

        log_message(f'Processing file: {file_proc}', callback_fun = callback_status)

        if callback_progress:
            progress = float((idx+1)/n_files)
            callback_progress(progress)

        name_base = file_proc.stem

        if projection_type == 'indiv':
            path_save_indiv = path_save / name_base
            
            if not path_save_indiv.is_dir():
                path_save_indiv.mkdir(parents=True)
                path_save_settings = path_save_indiv
        # Open image
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
            imsave(name_save, img_proj)
