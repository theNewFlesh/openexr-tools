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

    def __repr__(self):
        # type: () -> str
        return f'''
<ImageCodec.{self.name.upper()}>
  string: {self.string}
exr_code: {self.exr_code}'''[1:]

    @staticmethod
    def from_exr_code(code):
        # type: (int) -> ImageCodec
        '''
        Constructs a ImageCodec instance from a given EXR code.

        Args:
            code (int): EXR compression code.

        Raises:
            EnforceError: If value given is not an integer.
            EnforceError: If no ImageCodec type can be found for given code.

        Returns:
            ImageCodec: ImageCodec instance.
        '''
        msg = 'Value given is not an integer. {a} != {b}.'
        Enforce(code, 'instance of', int, message=msg)

        lut = {x.exr_code: x for x in ImageCodec.__members__.values()}

        msg = 'EXR code {a} has no legal ImageCodec type. '
        msg += f'Legal EXR codes: {sorted(lut.keys())}.'
        Enforce(code, 'in', lut.keys(), message=msg)

        return lut[code]

    @staticmethod
    def from_string(string):
        # type: (str) -> ImageCodec
        '''
        Constructs a ImageCodec instance from a given string.

        Args:
            string (int): ImageCodec string.

        Raises:
            EnforceError: If value given is not a string.
            EnforceError: If no ImageCodec type can be found for given string.

        Returns:
            ImageCodec: ImageCodec instance.
        '''
        msg = 'Value given is not a string. {a} != {b}.'
        Enforce(string, 'instance of', str, message=msg)

        lut = {x.string: x for x in ImageCodec.__members__.values()}

        string = string.lower()
        msg = '"{a}" has no legal ImageCodec type. '
        msg += f'Legal codec strings: {sorted(lut.keys())}.'
        Enforce(string, 'in', lut.keys(), message=msg)

        return lut[string]
