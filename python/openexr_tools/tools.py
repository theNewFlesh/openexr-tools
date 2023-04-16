from numpy.typing import DTypeLike, NDArray  # noqa F401
from typing import Tuple, Union  # noqa F401

from pathlib import Path

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
