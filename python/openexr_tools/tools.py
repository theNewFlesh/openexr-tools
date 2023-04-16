from numpy.typing import DTypeLike, NDArray  # noqa F401
from typing import Tuple, Union  # noqa F401

from copy import deepcopy
from pathlib import Path

import Imath as imath
import numpy as np
import OpenEXR as openexr

from openexr_tools.enum import ImageCodec
# ------------------------------------------------------------------------------


def read_exr(fullpath):
    # type: (Union[str, Path]) -> Tuple[NDArray, dict]
    '''
    Reads an OpenEXR image file.

    Args:
        fullpath (str or Path): Image file path.

    Raises:
        IOError: If given filepath is not an EXR file.

    Returns:
        tuple[numpy.NDArray, dict]: Image and metadata.
    '''
    if isinstance(fullpath, Path):
        fullpath = fullpath.absolute().as_posix()

    if not openexr.isOpenExrFile(fullpath):
        msg = f'{fullpath} is not an EXR file.'
        raise IOError(msg)

    img = openexr.InputFile(fullpath)
    metadata = img.header()
    win = metadata['dataWindow']
    x = (win.max.x - win.min.x) + 1
    y = (win.max.y - win.min.y) + 1

    # EXR headers store channel data in a map, so there can be no suuport for
    # arbitrary channel order persistence.
    image_stack = []
    temp = sorted(metadata['channels'].keys())
    channels = []
    for chan in list('RGBA'):
        if chan in temp:
            channels.append(chan)
            temp.remove(chan)
    for chan in temp:
        channels.append(chan)

    for chan in channels:
        data = metadata['channels'][chan]
        temp_img = img.channel(chan, data.type)

        # FLOAT is float32, HALF is float16
        dtype = np.float32  # type: DTypeLike
        if str(data.type) == 'HALF':
            dtype = np.float16

        temp_img = np.frombuffer(temp_img, dtype).reshape((y, x))
        image_stack.append(temp_img)

    image = np.dstack(image_stack)  # type: np.ndarray
    metadata['channels'] = [x.lower() for x in channels]
    metadata['num_channels'] = len(channels)

    # convert to compression enum
    comp = metadata['compression']
    metadata['compression'] = ImageCodec.from_exr_code(comp.v)

    for key, val in metadata.items():
        if isinstance(val, bytes):
            metadata[key] = val.decode('utf-8')

    return image, metadata


def clean_exr_metadadata(image, metadata):
    # type: (NDArray, dict) -> dict
    '''
    Uses given image and metadata dictionary to create EXR metadata for use in
    writing EXRs.

    Args:
        image (numpy.NDArray): Image.
        metadata (dict): Metadata dictionary.

    Returns:
        dict: Clean metadata.
    '''
    metadata = deepcopy(metadata)

    # ensure length of channels is the same length as image's channel dimension
    num_channels = 1
    if len(image.shape) > 2:
        num_channels = image.shape[2]

    channels = []
    if 'channels' in metadata:
        channels = metadata['channels']

    # do not assume rgba channel names for unnamed channels
    delta = num_channels - len(channels)
    for i in range(delta):
        channels.append(f'aux_{i:04d}')

    # use l channel name for grayscale images
    if len(channels) == 1 and channels[0] == 'aux_0000':
        channels = ['l']

    metadata['channels'] = channels

    # remove forbidden keys
    forbidden = [
        'compression',
        'dataWindow',
        'displayWindow',
        'lineOrder',
        'pixelAspectRatio',
        'screenWindowCenter',
        'screenWindowWidth',
    ]
    intersect = set(metadata.keys()).intersection(forbidden)
    for key in intersect:
        del metadata[key]

    return metadata


def write_exr(fullpath, image, metadata, codec=ImageCodec.PIZ):
    # type: (Union[str, Path], NDArray, dict, ImageCodec) -> None
    '''
    Writes image data and metadata as EXR to given file path.

    Args:
        fullpath (str or Path): Path to EXR file.
        image (numpy.NDArray): Image data.
        metadata (dict): Dictionary of EXR metadata.
        codec (ImageCodec, optional): Image codec. Default: ImageCodec.PIZ.

    Raises:
        TypeError: If image is not float16 or float32.
    '''
    dtype = image.dtype
    if dtype not in [np.float16, np.float32]:
        msg = f'EXR cannot be saved with array of dtype: {dtype}.'
        raise TypeError(msg)

    # determine bit depth of EXR
    ctype = imath.Channel(imath.PixelType(imath.PixelType.FLOAT))
    if dtype == np.float16:
        ctype = imath.Channel(imath.PixelType(imath.PixelType.HALF))

    # ensure metadata is clean
    metadata = clean_exr_metadadata(image, metadata)

    # ensure image has a channel axis
    if len(image.shape) < 3:
        shape = list(image.shape) + [1]
        image = image.reshape(shape)

    # create EXR data and channels objects
    channels = {}
    data = {}
    for i, chan in enumerate(metadata['channels']):
        chan = str(chan)
        if chan in list('lrgba'):
            chan = chan.upper()
        data[chan] = image[:, :, i].tobytes()
        channels[chan] = ctype

    # create EXR header
    y, x = image.shape[:2]
    header = openexr.Header(x, y)

    # all strings must be bytes
    for key, val in metadata.items():
        if isinstance(val, str):
            val = val.encode('utf-8')
        header[key] = val

    header['channels'] = channels
    header['compression'] = imath.Compression(codec.exr_code)

    # write EXR data
    if isinstance(fullpath, Path):
        fullpath = fullpath.absolute().as_posix()

    output = openexr.OutputFile(fullpath, header)
    output.writePixels(data)
