
import subprocess as sp
import sys
import os

sys.path.append(os.path.expanduser('~/projects/gala'))
from gala import morpho

from scipy import ndimage as nd
import numpy as np
from skimage import io, draw

from tifffile import imsave, imread

fiji_path = ''
if sys.platform == 'darwin':
    fiji_path = '/Applications/Fiji.app/Contents/MacOS/fiji-macosx'
elif sys.platform == 'linux2':
    fiji_path = '~/Downloads/Fiji.app/fiji-linux'


def draw_line_3d(p1, p2):
    """Draw a singe-voxel-wide line between two points.

    Parameters
    ----------
    p1, p2 : 3-tuples of int
        The coordinates of the two input points.

    Returns
    -------
    line_coords : tuple of ndarray
        Coordinates of points on the line between p1 and p2.
    """
    p1, p2 = np.array(p1, np.int), np.array(p2, np.int)
    distance = p2 - p1
    n_points = np.max(distance)
    raise NotImplementedError("draw_line_3d is not yet implemented.")
    return n_points


def erode(im):
    """`scipy.ndimage.grey_erosion` with size set to 3 on each axis.

    Parameters
    ----------
    im : np.ndarray, arbitrary type and shape.
        The input image.

    Returns
    -------
    out : np.ndarray, same type and shape as `im`
        The eroded image.
    """
    return nd.grey_erosion(im, size=[3] * im.ndim)


def dilate(im):
    """`scipy.ndimage.grey_dilation` with size set to 3 on each axis.

    Parameters
    ----------
    im : np.ndarray, arbitrary type and shape.
        The input image.

    Returns
    -------
    out : np.ndarray, same type and shape as `im`
        The dilated image.
    """
    return nd.grey_dilation(im, size=[3] * im.ndim)


def line_skeletons(label_image):
    """Compute a simulated traced skeleton with the distance transform.

    Parameters
    ----------
    label_image : np.ndarray of int, 2D or 3D
        A volume segmentation.

    Returns
    -------
    skeleton_image : np.ndarray, same shape and type as `label_image`
        The image of the computed skeletons.
    """
    segment_interiors = (dilate(label_image) == erode(label_image))
    distance_from_boundary = nd.distance_transform_edt(segment_interiors)
    skeleton_joints = morpho.regional_minima(distance_from_boundary)
    raise NotImplementedError("line_skeletons is not yet implemented.")
    for label in label_image:
        compute_distance_transform()
        find_peaks()
        connect_peaks()


def fiji_skeletonize_3d(label_image, temp_fout='binary_label.tif',
                        temp_fin='binary_skeleton.tif'):
    """Compute the skeleton of every nonzero object in the input image.

    Parameters
    ----------
    label_image : 3D np.ndarray of int
        The input segmentation.
    temp_fout : string, optional
        The file in which to store binary images before skeletonizing.
    temp_fin : string, optional
        The file Fiji should store the skeletons in.

    Returns
    -------
    skeletons : 3D np.ndarray of int
        The skeleton maps of each segment.
    """
    temp_fout = os.path.abspath(temp_fout)
    temp_fin = os.path.abspath(temp_fin)
    labels = np.unique(label_image)
    if labels[0] == 0:
        labels = labels[1:]
    skeletons = np.zeros_like(label_image)
    for i, label in enumerate(labels):
        binary_segment = 255 * (label_image == label).astype(np.uint8)
        imsave(temp_fout, binary_segment)
        try:
            # fiji doesn't automatically overwrite (apparently), so remove
            # skeleton file.
            os.remove(temp_fin)
        except OSError:
            pass
        ret = sp.call([fiji_path, '--headless',
                       'fiji_skeleton_macro.py', temp_fout, temp_fin])
        if ret != 0:
            print "error with label %d." % label
        else:
            binary_skeleton = imread(temp_fin).astype(bool)
            skeletons[binary_skeleton] = label
            print "label %d completed." % label
        if i % 10 == 1:
            imsave('temp-skeletons-file.tif', skeletons)
    return skeletons

