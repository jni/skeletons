import sys

from ij import IJ


def ij_binary_skeletonize(impath_in, impath_out):
    """Load image `impath`, skeletonize it, and save it to the same file.

    Parameters
    ----------
    impath_in : string
        Path to a 3D image file.
    impath_out : string
        Path to which to write the skeleton image file.

    Returns
    -------
    None
    """
    imp = IJ.openImage(impath_in)
    IJ.run(imp, "Skeletonize (2D/3D)", "")
    IJ.saveAs(imp, "Tiff", impath_out)
    imp.close()


if __name__ == '__main__':
    print sys.argv
    ij_binary_skeletonize(sys.argv[1], sys.argv[2])

