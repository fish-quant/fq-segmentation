# Imports
from pathlib import Path
import json
from skimage.io import imread, imsave
from skimage.transform import resize
import numpy as np


# Functions
def folder_prepare_prediction(path_process, search_type, channel_ident, path_save, projection_type):
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
    for file_proc in files_proc:

        print(f'Processing file: {file_proc}')
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
                    print(f'File already exists. will be overwritten {name_save}')
                imsave(name_save, img[i, :, :])

        else:

            if projection_type == 'mean':
                img_proj = img.mean(axis=0)

            elif projection_type == 'max':
                img_proj = img.mean(axis=0)

            name_save = path_save / f'{name_base}.png'

            if name_save.is_file():
                print(f'File already exists. will be overwritten {name_save}')
            imsave(name_save, img_proj)


def resize_mask(mask_small, size_orginal):
    """ Resize a label image.

    Parameters
    ----------
    mask_small : [type]
        [description]
    size_orginal : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """

    mask_full = np.zeros(size_orginal).astype('uint16')
    maski_template = np.zeros(mask_small.shape).astype('uint8')

    ind_objs = np.unique(mask_small)
    ind_objs = np.delete(ind_objs, np.where(ind_objs == 0))

    if ind_objs.size > 0:

        for obj_int in np.nditer(ind_objs):

            # Create binary mask for current object and find contour
            img_obj_loop = np.copy(maski_template)
            img_obj_loop[mask_small == obj_int] = 1

            img_obj_loop_large = resize(img_obj_loop, size_orginal, order=1).astype('bool')
            mask_full[img_obj_loop_large] = obj_int

    return mask_full