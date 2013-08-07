import sys

from imagej import IJ


def ij_binary_skeletonize(impath):
    """Load image `impath`, skeletonize it, and save it to the same file.

    Parameters
    ----------
    impath : string
        Path to a 3D image file.

    Returns
    -------
    None
    """
    imp = IJ.openImage("/Volumes/Projects/skeleton/binary_label.tif")
    IJ.run(imp, "Skeletonize (2D/3D)", "")
    IJ.saveAs(imp, "Tiff", "/Volumes/Projects/skeleton/binary_label.tif")
    imp.close()


if __name__ == '__main__':
    ij_binary_skeletonize(sys.argv[1])

