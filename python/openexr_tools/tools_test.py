from pathlib import Path
from tempfile import TemporaryDirectory

import Imath as imath
import numpy as np
import OpenEXR as openexr
import skimage.io
import unittest

import openexr_tools.tools as tools
# ------------------------------------------------------------------------------


class ToolsTests(unittest.TestCase):
    def write_png(self, root):
        target = Path(root, 'test.png')
        skimage.io.imsave(
            target, np.zeros((10, 10), dtype=np.uint8), check_contrast=False
        )
        return target

    def write_exr(self, root, dtype, channels=list('RGBA')):
        ctype = imath.Channel(imath.PixelType(imath.PixelType.FLOAT))
        if dtype == np.float16:
            ctype = imath.Channel(imath.PixelType(imath.PixelType.HALF))

        target = Path(root, 'test.exr').absolute().as_posix()
        data = {}
        chans = {}
        for c in channels:
            chan = c.upper()
            data[chan] = np.zeros((5, 10), dtype=dtype).tobytes()
            chans[chan] = ctype

        header = openexr.Header(10, 5)
        header['channels'] = chans

        file_ = openexr.OutputFile(target, header)
        file_.writePixels(data)

        return target

    def test_read_exr_error(self):
        with TemporaryDirectory() as root:
            src = self.write_png(root)
            expected = f'{src} is not an EXR file.'
            with self.assertRaisesRegex(IOError, expected):
                tools.read_exr(src)

    def test_read_exr(self):
        with TemporaryDirectory() as root:
            src = self.write_exr(root, np.float16)
            image, metadata = tools.read_exr(src)
            self.assertEqual(image.dtype, np.float16)
            self.assertEqual(image.sum(), 0)
            self.assertEqual(image.shape, (5, 10, 4))
            self.assertEqual(image.shape[2], len(metadata['channels']))
            self.assertEqual(metadata['channels'], list('rgba'))
            self.assertEqual(metadata['num_channels'], 4)

            src = self.write_exr(root, np.float32)
            image, metadata = tools.read_exr(src)
            self.assertEqual(image.dtype, np.float32)
            self.assertEqual(image.sum(), 0)
            self.assertEqual(image.shape, (5, 10, 4))
            self.assertEqual(image.shape[2], len(metadata['channels']))
            self.assertEqual(metadata['channels'], list('rgba'))
            self.assertEqual(metadata['num_channels'], 4)
