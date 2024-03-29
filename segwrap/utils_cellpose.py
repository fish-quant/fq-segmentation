# Imports 
import numpy as np
from tqdm import tqdm
import time
import matplotlib.pyplot as plt
import pathlib
from pathlib import Path
import json
import cv2

# Imports of CellPose specific libraries
from cellpose import models, io, plot
from segwrap.utils_general import log_message, create_output_path

# Call predict function
def cellpose_predict(data, config, path_save, callback_log=None):
    """ Perform prediction with CellPose. 

    Parameters
    ----------
    data : dict
        Contains data on which prediction should be performed. 
    config : dict
        Configuration of CellPose prediction. 
    path_save : pathline Path object
        Path where results will be saved. 
    """

    # Get data
    imgs = data['imgs']
    file_names = data['file_names']
    channels = data['channels']
    obj_name = data['obj_name']
    sizes_orginal = data['sizes_orginal']
    new_size = data['new_size']
    
    # Get config
    model_type = config['model_type']
    diameter = config['diameter']
    net_avg = config['net_avg']
    resample = config['resample']   

    log_message(f'\nPerforming segmentation of {obj_name}\n', callback_fun=callback_log)

    start_time = time.time()

    if not path_save.is_dir():
        path_save.mkdir()

    # Perform segmentation with CellPose
    model = models.Cellpose(gpu=False, model_type=model_type)  # model_type can be 'cyto' or 'nuclei'
    masks, flows, styles, diams = model.eval(imgs, diameter=diameter, channels=channels, net_avg=net_avg, resample=resample)

    # Display and save results
    log_message(f'\n Creating outputs ...\n', callback_fun=callback_log)
    n_img = len(imgs)

    for idx in tqdm(range(n_img)):
        
        # Get images and file-name
        file_name = file_names[idx]
        maski = masks[idx]
        flowi = flows[idx][0]
        imgi = imgs[idx]
        
        # Rescale each channel separately
        imgi_norm = imgi.copy()
        for idim in range(3):
            imgdum = imgi[:, :, idim]
            
            # Renormalize to 8bit between 1 and 99 percentile
            pa = np.percentile(imgdum, 0.5)
            pb = np.percentile(imgdum, 99.5)
            
            if pb > pa:
                imgi_norm[:, :, idim] = 255 * (imgdum - pa) / (pb - pa)

        # Save flow
        io.imsave(str(path_save / f'{file_name.stem}__flow__{obj_name}.png'), flowi)

        # Resize masks if necessary 
        if new_size:
            mask_full = resize_mask(maski, sizes_orginal[idx])

            io.imsave(str(path_save / f'{file_name.stem}__mask__{obj_name}.png'), mask_full)
            io.imsave(str(path_save / f'{file_name.stem}__mask_resize__{obj_name}.png'), maski)

        else:
            io.imsave(str(path_save / f'{file_name.stem}__mask__{obj_name}.png'), maski)

        # Save mask and flow images
        #f_mask = str(path_save / f'{file_name.stem}__mask__{obj_name}.png')
        #log_message(f'\nMask saved to file: {f_mask}\n', callback_fun=callback_log)

        #io.imsave(str(path_save / f'{file_name.stem}__mask__{obj_name}.png'), maski)


        # Save overview image
        fig = plt.figure(figsize=(12,3))
        plot.show_segmentation(fig, imgi_norm.astype('uint8'), maski, flowi)
        plt.tight_layout()
        fig.savefig(str(path_save / f'{file_name.stem}__seg__{obj_name}.png'), dpi=300)
        plt.close(fig)

    log_message(f"\nSegmentation of provided images finished ({(time.time() - start_time)}s)", callback_fun=callback_log)


def clean_par_dict(par_dict):
    """
    Cleam up dictionary containing all parameters such that it can
    be written into a json file.
    """
    par_dict['path_scan'] = str(par_dict['path_scan'])
    par_dict['path_save'] = str(par_dict['path_save'])
    par_dict['callback_log'] = str(par_dict['callback_log'])
    par_dict['callback_progress'] = str(par_dict['callback_progress'])
    par_dict['callback_status'] = str(par_dict['callback_status'])
    return par_dict


# Function to load and segment objects individually 
def segment_obj_indiv(path_scan, obj_name, str_channel, img_ext, new_size, model_type, diameter, net_avg, resample, path_save,  input_subfolder=None, callback_log=None, callback_status=None, callback_progress=None):
    """ Will recursively search folder for images to be analyzed!

    Parameters
    ----------
    path_scan : [type]
        [description]
    str_nuclei : [type]
        [description]
    img_ext : [type]
        [description]
    diameter : [type]
        [description]
    model_type : [type]
        [description]
    path_save : pathlib object or string
        Path to save results,
        - If Pathlib object, then this absolute path is used.
        - If 'string' a replacement operation on the provided name of the data path will be applied (see create_output_path).
    input_subfolder : str
        Name of subfolder that contains results. If specified ONLY files in this folder will be processed.
    callback_log : [type], optional
        [description], by default None
    callback_status : [type], optional
        [description], by default None
    callback_progress : [type], optional
        [description], by default None

    Returns
    -------
    [type]
        [description]
    """

    # Print all input parameters
    par_dict = locals()
    par_dict = clean_par_dict(par_dict)
    log_message(f"Function (segment_obj_indiv) called with: {str(par_dict)} ", callback_fun=callback_log)

    # Configurations
    config = {'model_type': model_type,
              'diameter': diameter,
              'net_avg': net_avg,
              'resample': resample}

    channels = [0, 1]

    # Use provided absolute user-path to save images.
    if isinstance(path_save, pathlib.PurePath):
        path_save_results = path_save
        if not path_save_results.is_dir():
            path_save_results.mkdir(parents=True)

    else:
        path_save_str_replace = path_save

    if not path_scan.is_dir():
        log_message(f'Path {path_scan} does not exist.', callback_fun=callback_log) 
        return

    # Search for file to be analyzed
    log_message(f'\nLoading images and segment them on the fly', callback_fun=callback_log)
    files_proc = []
    for path_img in path_scan.rglob(f'*{str_channel}*{img_ext}'):
        if input_subfolder:
            if path_img.parts[-2] == input_subfolder:
                files_proc.append(path_img)
        else:
            files_proc.append(path_img)
    n_imgs = len(files_proc)

    if n_imgs == 0:
        log_message(f'NO IMAGES FOUND. Check your settings.', callback_fun=callback_log)
        return

    # Process files
    for idx, path_img in enumerate(files_proc):
        imgs = []
        files = []
        sizes_orginal = []

        log_message(f'Segmenting image : {path_img.name}', callback_fun=callback_log)

        if callback_status:
            callback_status(f'Segmenting image : {path_img.name}')

        if callback_progress:
            progress = float((idx+1)/n_imgs)
            callback_progress(progress)

        # Read images
        img = io.imread(str(path_img))
        if img.ndim != 2:
            log_message(f'\nERROR\n  Input image has to be 2D. Current image is {img.ndim}D', callback_fun=callback_log)
            continue
        
        
        # IMPORTANT: CV2 resize is defined as (width, height)
        print('>>> process file')
        print(f'input file (size): {img.shape}')

        sizes_orginal.append(img.shape)

        # Resize
        if new_size:

            # New size can also be defined as a scalar factor
            if len(new_size) == 1:
                scale_factor = new_size[0]
                img_size = img.shape
                new_size = tuple(int(ti/scale_factor) for ti in img_size)
                
            # IMPORTANT: CV2 resize is defined as (width, height)    
            dsize = (new_size[1], new_size[0])             
            img = cv2.resize(img, dsize)
            
        print(f'resized file (size): {img.shape}')
        
            
        # For object segmentation
        img_zeros = np.zeros(img.shape)
        img_3d_dpi = np.dstack([img_zeros, img_zeros, img])
        imgs.append(img_3d_dpi)
        files.append(path_img)

        # >>> Call function for prediction
        data = {'imgs': imgs,
                'file_names': files,
                'channels': channels,
                'obj_name': obj_name,
                'sizes_orginal': sizes_orginal,
                'new_size': new_size}

        # Create new output path if specified
        if not isinstance(path_save, pathlib.PurePath):
            path_save_results = create_output_path(path_img.parent, path_save_str_replace, subfolder='', create_path=True)
            path_save_settings = path_save_results

        cellpose_predict(data, config, path_save=path_save_results, callback_log=callback_log)

    # Save settings
    if len(imgs) > 0:
        fp = open(str(path_save_results / f'segmentation_settings__{obj_name}.json'), "w")
        json.dump(par_dict, fp, indent=4, sort_keys=True)
        fp.close()

    log_message(f'\n BATCH SEGMENTATION finished', callback_fun=callback_log)


# Function to load and segment cells and nuclei images individually 
def segment_cells_nuclei_indiv(path_scan, str_channels, img_ext, new_size, model_types, diameters, net_avg, resample, path_save, input_subfolder=None, callback_log=None, callback_status=None, callback_progress=None): 
    """[summary] segment cells and nuclei in bulk, e.g. first all images are loaded and then segmented. 
    TODO: specify parameters
    Parameters
    ----------
    path_scan : [type]
        [description]
    strings : [type]
        [description]
    img_ext : [type]
        [description]
    new_size : tuple
        Defines resizing of image. If two elements, new size of image. If one element, resizing factor. 
        If emtpy, no resizing.
    sizes : [type]
        [description]
    models : [type]
        [description]
    path_save : pathlin object or string
        Path to save results,
        - If Pathlib object, then this absolute path is used.
        - If 'string' a replacement operation on the provided name of the data path will be applied (see create_output_path).
          And results will be stored in subfolder 'segmentation-input'
    callback_log : [type], optional
        [description], by default None
    callback_status : [type], optional
        [description], by default None
    callback_progress : [type], optional
        [description], by default None
    """

    par_dict = locals()
    par_dict = clean_par_dict(par_dict)
    log_message(f"Function (segment_obj_indiv) called with: {str(par_dict)} ", callback_fun=callback_log)

    # Get parameters
    (str_cyto, str_nuclei) = str_channels
    (diameter_cells, diameter_nuclei) = diameters
    (model_type_cells, model_type_nuclei) = model_types

    # Use provided absolute user-path to save images.
    if isinstance(path_save, pathlib.PurePath):
        path_save_results = path_save
        if not path_save_results.is_dir():
            path_save_results.mkdir(parents=True)

    else:
        path_save_str_replace = path_save

    # Configurations
    config_nuclei = {'model_type': model_type_nuclei,
                     'diameter': diameter_nuclei,
                     'net_avg': net_avg,
                     'resample': resample}

    config_cyto = {'model_type': model_type_cells,
                   'diameter': diameter_cells,
                   'net_avg': net_avg,
                   'resample': resample}

    channels_cyto = [1, 3]
    channels_nuclei = [0, 1]

    # Loop over data
    log_message(f'\nLoading image pairs and segment them on the fly', callback_fun=callback_log) 

    if not path_scan.is_dir():
        log_message(f'Path {path_scan} does not exist.', callback_fun=callback_log) 
        return

    # Search for file to be analyzed
    log_message(f'\nLoading images and segment them on the fly', callback_fun=callback_log)
    files_proc = []
    for path_img in path_scan.rglob(f'*{str_cyto}*{img_ext}'):
        if input_subfolder:
            if path_img.parts[-2] == input_subfolder:
                files_proc.append(path_img)
        else:
            files_proc.append(path_img)
    n_imgs = len(files_proc)

    if n_imgs == 0:
        log_message(f'NO IMAGES FOUND. Check your settings.', callback_fun=callback_log)
        return

    # Process files
    for idx, path_cyto in enumerate(files_proc):
        imgs_cyto = []
        imgs_nuclei = []
        files_cyto = []
        files_nuclei = []
        sizes_orginal = []

        log_message(f'Segmenting image : {path_cyto.name}', callback_fun=callback_log)

        if callback_status:
            callback_status(f'Segmenting image : {path_cyto.name}')

        if callback_progress:
            progress = float((idx+1)/n_imgs)
            callback_progress(progress)

        # DAPI image: existing?
        path_nuclei = Path(str(path_cyto).replace(str_cyto, str_nuclei))
        if not path_nuclei.is_file():
            log_message(f'DAPI image not found : {path_nuclei}', callback_fun=callback_log)
            continue

        # Read images
        img_cyto = io.imread(str(path_cyto))
        if img_cyto.ndim != 2:
            log_message(f'\nERROR\n  Input image of cell has to be 2D. Current image is {img_cyto.ndim}D', callback_fun=callback_log)
            continue

        img_nuclei = io.imread(str(path_nuclei))
        if img_nuclei.ndim != 2:
            log_message(f'\nERROR\n  Input image of cell has to be 2D. Current image is {img_nuclei.ndim}D', callback_fun=callback_log)
            continue

        # Resize image before CellPose if specified
        sizes_orginal.append(img_cyto.shape)

        # Resize
        if new_size:

            # New size can also be defined as a scalar factor
            if len(new_size) == 1:
                scale_factor = new_size[0]
                img_size = img_cyto.shape
                new_size = tuple(int(ti/scale_factor) for ti in img_size)

            # IMPORTANT: CV2 resize is defined as (width, height)
            dsize = (new_size[1], new_size[0])  
            img_cyto = cv2.resize(img_cyto, dsize)
            img_nuclei = cv2.resize(img_nuclei, dsize)

        img_zeros = np.zeros(img_cyto.shape)

        # For cell segmentation
        img_3d = np.dstack([img_cyto, img_zeros, img_nuclei])
        imgs_cyto.append(img_3d)
        files_cyto.append(path_cyto)

        # For nuclei segmentation
        img_3d_dpi = np.dstack([img_zeros, img_zeros, img_nuclei])
        imgs_nuclei.append(img_3d_dpi)
        files_nuclei.append(path_nuclei)

        # Create new output path if specified
        if not isinstance(path_save, pathlib.PurePath):
            path_save_results = create_output_path(path_cyto.parent, path_save_str_replace, subfolder='', create_path=True)
            path_save_settings = path_save_results

        # >>> Call function for prediction of cell
        data_cyto = {'imgs': imgs_cyto,
                     'file_names': files_cyto,
                     'sizes_orginal': sizes_orginal,
                     'new_size': new_size,
                     'channels': channels_cyto,
                     'obj_name': 'cells'}

        cellpose_predict(data_cyto, config_cyto, path_save=path_save_results, callback_log=callback_log)

        # >>> Call function for prediction of nuclei
        data_nuclei = {'imgs': imgs_nuclei,
                       'file_names': files_nuclei,
                       'channels': channels_nuclei,
                       'obj_name': 'nuclei',
                       'sizes_orginal': sizes_orginal,
                       'new_size': new_size}

        cellpose_predict(data_nuclei, config_nuclei, path_save=path_save_results, callback_log=callback_log)

    # Save settings
    if len(imgs_cyto) > 0:
        fp = open(str(path_save_results / 'segmentation_settings__cells_nuclei.json'), "w")
        json.dump(par_dict, fp, indent=4, sort_keys=True)
        fp.close()

    log_message(f'\n BATCH SEGMENTATION finished', callback_fun=callback_log)


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

            # IMPORTANT: CV2 resize is defined as (width, height)
            dsize = (size_orginal[1], size_orginal[0])
            img_obj_loop_large = cv2.resize(img_obj_loop, dsize).astype('bool')
            mask_full[img_obj_loop_large] = obj_int

    return mask_full