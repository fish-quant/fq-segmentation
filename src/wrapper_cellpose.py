# Test cellpose
# Run in cellpose environment
# Slow on full size images
# You can either the images before predictionm, but this requires resizing the mask.
# Compare to see which option is faster.

# Imports of general purpose libraries
from skimage.transform import resize
from skimage.io import imread, imsave
import numpy as np
from tqdm import tqdm
import time
import sys
import mxnet as mx
import matplotlib.pyplot as plt
from pathlib import Path

# Imports of CellPose specific libraries
from cellpose import models, utils
from cellpose import plot, transforms
from utils_segmentation import resize_mask


# Function to load and segment nuclei images
def segment_cells_nuclei(path_scan, strings, img_ext, new_size, sizes, models, path_save): 
    """ TODO: write docs
    
    Parameters
    ----------
    path_scan : [type]
        [description]
    strings : [type]
        [description]
    img_ext : [type]
        [description]
    new_size : [type]
        [description]
    sizes : [type]
        [description]
    models : [type]
        [description]
    path_save : [type]
        [description]
    """
    
    # Print all input parameters
    print("Function (segment_cells_nuclei) called with: ", locals())

    # Get parameters
    (str_cyto, str_nuclei) = strings
    (size_cells, size_nuclei) = sizes
    (model_cells, model_nuclei) = models
    
    # Which device to use
    device = check_device()

    # Load data
    imgs_cyto, imgs_nuclei, files_cyto, files_nuclei, channels_cyto, channels_nuclei, sizes_orginal = load_imgs_ctyo_nuclei(
                                                            path_scan=path_scan, 
                                                            str_cyto=str_cyto,     
                                                            str_nuclei=str_nuclei,
                                                            img_ext=img_ext, 
                                                            new_size=new_size)

    # %% Call function for prediction of cell
    config = {'model_type': model_cells, 
            'obj_size': size_cells,
            'device': device}

    data = { 'imgs': imgs_cyto,
            'file_names': files_cyto, 
            'sizes_orginal': sizes_orginal,
            'channels': channels_cyto,
            'new_size': new_size,
            'obj_name':'cells'
    }
                
    cellpose_predict(data, config, path_save = path_save )
        
    # Call function for prediction of nuclei
    config = {'model_type': model_nuclei, 
            'obj_size': size_nuclei,
            'device': device}

    data = { 'imgs': imgs_nuclei,
            'file_names': files_nuclei, 
            'sizes_orginal': sizes_orginal,
            'channels': channels_nuclei,
            'new_size': new_size,
            'obj_name':'nuclei'
    }
                
    cellpose_predict(data, config, path_save = path_save )



# Function to load and segment nuclei images
def segment_nuclei(path_scan, str_dapi, img_ext, new_size, size_nuclei, model, path_save):
    """ Wrapper function to load and segment nuclei in 2D images. 
    
    Parameters
    ----------
    path_scan : pathline Path object
        Folder to scan for images that will be segmented.
    str_dapi : str
        String that has be contained in the file-name in order to be added to loaded.
    img_ext : str
        Image file extension. 
    new_size : tuple
        New size of image if image should be resized. Empty tuple for no resizing. 
    size_nuclei : int
        Typical diameter of nuclei in image
    model : str
        CellPose model that should be used for segmentation ('cyto' or 'nuclei').
        The cytoplasmic model works also well for nuclei, especially in densly 
        packed regions. 
    """
    
        
    # Print all input parameters
    print("Function (segment_cells_nuclei) called with: ", locals())
    
    # Which device to use
    device = check_device()
    
    # Load data
    imgs, files, channels, sizes_orginal = load_imgs_nuclei(path_scan=path_scan, 
                                                            str_dapi=str_dapi,
                                                            img_ext=img_ext, 
                                                            new_size=new_size)

    # Call function for prediction
    config = {'model_type': model, 
            'obj_size': size_nuclei,
            'device': device}

    data = { 'imgs': imgs,
            'file_names': files, 
            'sizes_orginal': sizes_orginal,
            'channels': channels,
            'new_size': new_size,
            'obj_name':'nuclei'
    }
                
    cellpose_predict(data, config, 
                    path_save = path_save )


# Function: check if GPU working, and if so use it
def check_device(gpu_number=0):
    """ Check on which device (GPU or CPU) CellPose will be running. 
     
    Parameters
    ----------
    gpu_number : int, optional
        Index of GPU to be tested, by default 0
    """
    use_gpu = utils.use_gpu(gpu_number=gpu_number)
    if use_gpu:
        print('CellPose will be USING GPU')
        device = mx.gpu()
    else:
        print('CellPose will be USING CPU')
        device = mx.cpu()

    return device

# Path to save results 
def cellpose_predict(data, config, path_save):
    """Perform prediction with CellPose. 
    
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
    sizes_orginal = data['sizes_orginal']
    channels = data['channels']
    new_size = data['new_size']
    obj_name = data['obj_name']
    
    # Get config
    model_type = config['model_type']
    obj_size = config['obj_size']
    device = config['device']
    
    print(f'\n\nPerforming segmentation of {obj_name}\n')
    
    start_time = time.time()
    
    if not path_save.is_dir():
        path_save.mkdir()
        
    # Perform segmentation with CellPose
    
    model = models.Cellpose(device, model_type=model_type )  # model_type can be 'cyto' or 'nuclei'
    masks, flows, styles, diams = model.eval(imgs, rescale=30./obj_size, channels=channels, net_avg=False, threshold=0.4)

    # Display and save 
    print(f' ... creating outputs ...\n')
    n_img = len(imgs)
    
    for idx in tqdm(range(n_img)):
        img = transforms.reshape(imgs[idx], channels)
        file_name = file_names[idx]

        img = plot.rgb_image(img)
        maski = masks[idx]
        flowi = flows[idx][0]

        # Save overview image
        fig = plt.figure(figsize=(12, 3))
        plot.show_segmentation(fig, img, maski, flowi)
        plt.tight_layout()

        plt.savefig(path_save / f'segmentation__{obj_name}__{file_name.stem}.png', dpi=600)
        plt.close()

        # Save mask and flow images
        imsave(path_save / f'flow__{obj_name}__{file_name.stem}.png', flowi, check_contrast=False)

        if new_size:
            mask_full = resize_mask(maski, sizes_orginal[idx])

            imsave(path_save / f'mask__{obj_name}__{file_name.stem}.tif', mask_full.astype('uint16'), check_contrast=False)
            imsave(path_save / f'mask_resize__{obj_name}__{file_name.stem}.tif', maski.astype('uint16'), check_contrast=False)
        else:
            imsave(path_save / f'mask__{obj_name}__{file_name.stem}.tif', maski.astype('uint16'), check_contrast=False)


        
    print("SEGMENTATION FINISHED")
    print("\n--- %s seconds ---" % (time.time() - start_time))


def load_imgs_nuclei(path_scan, str_dapi, img_ext, new_size):
    """[summary]
    
    Parameters
    ----------
    path_scan : pathline Path object
        Folder to scan for images that will be segmented.
    str_dapi : str
        String that has be contained in the file-name in order to be added to loaded.
    img_ext : str
        Image file extension. 
    new_size : tuple
        New size of image if image should be resized. Empty tuple for no resizing. 
    
    Returns
    -------
    [type]
        [description]
    """
    # Create processing lists
    channels_nuclei = [0, 1]
    imgs_nuclei = []
    files_nuclei = []
    sizes_orginal = []
    print(f'Loading images and creating processing list')

    for path_dapi in path_scan.glob(f'*{str_dapi}*{img_ext}'):

        # Load image and resize if specified
        img_dapi = imread(str(path_dapi))
        sizes_orginal.append(img_dapi.shape)
        
        if new_size:
            img_dapi = resize(img_dapi, new_size)
        img_zeros = np.zeros(img_dapi.shape)

        # For nuclei segmentation
        img_3d_dpi = np.dstack([img_zeros, img_zeros, img_dapi])
        imgs_nuclei.append(img_3d_dpi)
        files_nuclei.append(path_dapi)
        
    print(f' ... prepared {len(imgs_nuclei)} images for segmentation ...\n')
    
    return imgs_nuclei, files_nuclei, channels_nuclei, sizes_orginal


# Load data for nuclei and cyto segmentation
def load_imgs_ctyo_nuclei(path_scan, str_cyto, str_nuclei, img_ext, new_size ):
    """[summary]
    
    Parameters
    ----------

    path_scan : pathline Path object
        Folder to scan for images that will be segmented.
    str_cyto : str
        String that has be contained in the file-name in order to be added to loaded.
    str_nuclei : str
        String that has be contained in the file-name in order to be added to loaded.
    img_ext : str
        Image file extension. 
    new_size : tuple
        New size of image if image should be resized. Empty tuple for no resizing. 
        
    Returns
    -------
    [type]
        [description]
    """
    imgs_cyto = []
    imgs_nuclei = []
    files_cyto = []
    files_nuclei = []
    sizes_orginal = []
    print(f'Loading images and creating processing list')
    
    # Create processing lists
    channels_cyto = [1, 3]
    channels_nuclei = [0, 1]
    
    if not path_scan.is_dir():
        print(f'Path {path_scan} does not exist.')
        return

    for path_cyto in path_scan.glob(f'*{str_cyto}*{img_ext}'):
        # DAPI image: existing?
        path_nuclei = Path(str(path_cyto).replace(str_cyto, str_nuclei))
        if not path_nuclei.is_file():
            print(f'DAPI image not found : {path_nuclei}')
            continue

        # Read images
        img_cyto = imread(str(path_cyto))
        img_nuclei = imread(str(path_nuclei))
        sizes_orginal.append(img_cyto.shape)

        # Resize
        if new_size:
            img_cyto = resize(img_cyto, new_size)
            img_nuclei = resize(img_nuclei, new_size)

        img_zeros = np.zeros(img_cyto.shape)

        # For cell segmentation
        img_3d = np.dstack([img_cyto, img_zeros, img_nuclei])
        imgs_cyto.append(img_3d)
        files_cyto.append(path_cyto)

        # For nuclei segmentation
        img_3d_dpi = np.dstack([img_zeros, img_zeros, img_nuclei])
        imgs_nuclei.append(img_3d_dpi)
        files_nuclei.append(path_nuclei)

    print(f' ... prepared {len(imgs_nuclei)} images for segmentation ...\n')
    
    return  imgs_cyto, imgs_nuclei, files_cyto, files_nuclei, channels_cyto, channels_nuclei, sizes_orginal
