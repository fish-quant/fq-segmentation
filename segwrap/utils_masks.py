# Imports
from skimage.io import imread, imsave
from skimage.measure import regionprops
import numpy as np
from tqdm import tqdm
from scipy import ndimage
from pathlib import Path
import pathlib

from segwrap.utils_general import log_message, create_output_path

# Calculate images summarizing distance to objects
def create_img_closest_obj(path_scan, str_label, strs_save, path_save=None, search_recursive=False, truncate_distance=None, callback_log=None, callback_status=None, callback_progress=None):
    """   Function to process label images and facilitate assignment to closest segmented object.
    Will create two 2D images with the same size as the label image. Pixel values in either image
    encode 
    1. Distance to the closted object, e.g. nuclei.
    2. Index of clostest object.

    Parameters
    ----------
    path_scan : pathlib Path object
        Path to scan for label images.
    str_label : str
        Unique string contained in label iamge to be saved.
    strs_save : tuple of strings
        Strings defining how to save the result images, either string will replace str_save.
    path_save : pathlib Path object
        Path to save results,
        - If Pathlib object, then this absolute path is used.
        - If 'string' a replacement operation path containing the analyzed mask will be applied (see create_output_path).
    truncate_distance : int
        Distance above which distances will be truncated. Using a value of 255 has the advantage
        that the saved image is 8bit and thus small.
    callback_log : callback, optional
        Callback function to provide function log. If none, print will be used.
        For more details see segwrap.utils_general.log_message
    """

    # Check scan directory
    if not path_scan.is_dir():
        log_message(f'Path {path_scan} does not exist.', callback_fun=callback_log) 
        return

    # Path to save results
    if isinstance(path_save, pathlib.PurePath):
        path_save_results = path_save
        if not path_save_results.is_dir():
            path_save_results.mkdir(parents=True)
        path_save_settings = path_save_results

    else:
        path_save_str_replace = path_save

    # Search files: recursively or not
    files_proc = []
    if search_recursive:
        for path_mask in path_scan.rglob(f'*{str_label}*'):
            files_proc.append(path_mask)
    else:
        for path_mask in path_scan.glob(f'*{str_label}*'):
            files_proc.append(path_mask)

    # Process files
    n_files = len(files_proc)
    for idx, file_label in enumerate(files_proc):

        log_message(f'\n>>> Processing file: {file_label}', callback_fun=callback_status)

    #    if callback_progress:
    #        progress = float((idx+1)/n_files)
    #        callback_progress(progress)
    #return
    
    # Look for all segmentation masks
    #for file_label in path_scan.glob(f'*{str_label}*'):

    #    log_message(f'Analyzing file {file_label}', callback_fun=callback_log)
    
        # >>> Create path to save data if necessary
        if not isinstance(path_save, pathlib.PurePath):
            path_save_results = create_output_path(file_label.parent, path_save_str_replace, subfolder=None, create_path=True)
            log_message(f'Results will be save here : {path_save_results}', callback_fun=callback_status)

        # >>>> Read label image
        img_labels = imread(file_label)
        props = regionprops(img_labels)
        labels = np.array([prop.label for prop in props])
        n_objs = len(labels)

        # Loop over all nuclei and create create distance map
        log_message(' Creating distance maps. This can take a while ...', callback_fun=callback_log)
        dist_mat = np.zeros((img_labels.shape[0], img_labels.shape[1], n_objs))
        mask_fill_indiv = np.zeros((img_labels.shape[0], img_labels.shape[1], n_objs))

        for indx, obj_int in enumerate(tqdm(np.nditer(labels), total=n_objs)):

            # Create binary mask for current object and find contour
            img_label_loop = np.zeros((img_labels.shape[0], img_labels.shape[1]))
            img_label_loop[img_labels == obj_int] = 1
            mask_fill_indiv[:, :, indx] = img_label_loop

            dist_obj = ndimage.distance_transform_edt(np.logical_not(img_label_loop))
            if truncate_distance:
                dist_obj[dist_obj > truncate_distance] = truncate_distance
            dist_mat[:, :, indx] = dist_obj

        # >>> Condense distmap in two matrixes: index and distance to closest object
        dist_obj_ind_3D = np.argsort(dist_mat, axis=2)
        dist_obj_dist_3D = np.take_along_axis(dist_mat, dist_obj_ind_3D, axis=2)

        # For index: replace Python matrix index with actual index from label image
        ind_obj_closest = np.zeros((img_labels.shape[0], img_labels.shape[1]))
        dist_obj_ind_2D = np.copy(dist_obj_ind_3D[:, :, 0])

        for indx, obj_int in enumerate(np.nditer(labels)):
            ind_obj_closest[dist_obj_ind_2D == indx] = obj_int


        # Save index of closest object
        name_save_ind = path_save_results / f'{file_label.stem.replace(str_label, strs_save[0])}.png'
        if str(name_save_ind) != str(file_label):
            imsave(name_save_ind, ind_obj_closest.astype('uint16'), check_contrast=False)
        else:
            log_message(f'Name to save index matrix could not be established: {name_save_ind}', callback_fun=callback_log)

        # Save distances to closest object
        name_save_dist = path_save_results / f'{file_label.stem.replace(str_label, strs_save[1])}.png'
        if str(name_save_dist) != str(file_label):
            imsave(name_save_dist, dist_obj_dist_3D[:, :, 0].astype('uint16'), check_contrast=False)
        else:
            log_message(f'Name to save index matrix could not be established: {name_save_dist}', callback_fun=callback_log)


