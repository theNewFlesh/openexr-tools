from enum import Enum

from lunchbox.enforce import Enforce
# ------------------------------------------------------------------------------


'''
The enum module contains enum classes for working with EXR image codes.
'''


class ImageCodec(Enum):
    '''
    Legal EXR image codecs.

    Includes:

        * B44
        * B44A
        * DWAA
        * DWAB
        * PIZ
        * PXR24
        * RLE
        * UNCOMPRESSED
        * ZIP
        * ZIPS
    '''
    B44 = ('b44', 6)                    # Imath.Compression.B44_COMPRESSION
    B44A = ('b44a', 7)                  # Imath.Compression.B44A_COMPRESSION
    DWAA = ('dwaa', 8)                  # Imath.Compression.DWAA_COMPRESSION
    DWAB = ('dwab', 9)                  # Imath.Compression.DWAB_COMPRESSION
    PIZ = ('piz', 4)                    # Imath.Compression.PIZ_COMPRESSION
    PXR24 = ('pxr24', 5)                # Imath.Compression.PXR24_COMPRESSION
    RLE = ('rle', 1)                    # Imath.Compression.RLE_COMPRESSION
    UNCOMPRESSED = ('uncompressed', 0)  # Imath.Compression.NO_COMPRESSION
    ZIP = ('zip', 3)                    # Imath.Compression.ZIP_COMPRESSION
    ZIPS = ('zips', 2)                  # Imath.Compression.ZIPS_COMPRESSION

    def __init__(self, string, exr_code):
        # type: (str, int) -> None
        '''
        Args:
            string (str): String representation of codec.
            exr_code (int): EXR compression code.
        '''
        self.string = string  # type: ignore
        self.exr_code = exr_code
