import os
from pathlib import Path
from tempfile import TemporaryDirectory

import Imath as imath
import numpy as np
import OpenEXR as openexr
import skimage.io
import unittest

from openexr_tools.enum import ImageCodec
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

    def test_read_exr_channels(self):
        with TemporaryDirectory() as root:
            expected = sorted(['foo', 'bar', 'baz'])
            src = self.write_exr(root, np.float32, channels=expected)
            image, metadata = tools.read_exr(src)
            self.assertEqual(metadata['channels'], expected)

            channels = ['foo', 'bar', 'baz'] + list('rgba')
            src = self.write_exr(root, np.float32, channels=channels)
            image, metadata = tools.read_exr(src)
            expected = list('rgba') + sorted(['foo', 'bar', 'baz'])
            self.assertEqual(metadata['channels'], expected)

    def test_clean_exr_metadadata_channels(self):
        image = np.zeros((10, 10), dtype=np.float32)
        metadata = {}
        result = tools.clean_exr_metadadata(image, metadata)
        self.assertEqual(result['channels'], ['l'])

        image = np.zeros((10, 10, 7), dtype=np.float32)
        metadata = {}
        result = tools.clean_exr_metadadata(image, metadata)
        expected = [f'aux_{i:04d}' for i in range(7)]
        self.assertEqual(result['channels'], expected)

        channels = list('rgba') + ['foo']
        metadata = dict(channels=channels)
        result = tools.clean_exr_metadadata(image, metadata)
        expected = channels
        expected += [f'aux_{i:04d}' for i in range(2)]
        self.assertEqual(result['channels'], expected)

    def test_clean_exr_metadadata_forbidden(self):
        image = np.zeros((10, 10), dtype=np.float32)
        forbidden = dict(
            compression='foo',
            dataWindow='foo',
            displayWindow='foo',
            lineOrder='foo',
            pixelAspectRatio='foo',
            screenWindowCenter='foo',
            screenWindowWidth='foo',
        )
        metadata = dict(foo='bar')
        metadata.update(forbidden)
        result = tools.clean_exr_metadadata(image, metadata)
        for key in forbidden:
            self.assertNotIn(key, result)

        self.assertEqual(metadata['foo'], 'bar')

    def test_write_exr(self):
        with TemporaryDirectory() as root:
            target = Path(root, 'test_exr.exr')
            image = np.zeros((10, 5, 4), dtype=np.float16)
            tools.write_exr(target, image, {})
            self.assertTrue(os.path.exists(target))

    def test_write_exr_two_channel(self):
        with TemporaryDirectory() as root:
            target = Path(root, 'test_exr.exr')
            image = np.zeros((10, 5), dtype=np.float16)
            tools.write_exr(target, image, {})
            self.assertTrue(os.path.exists(target))

    def test_write_exr_error(self):
        with TemporaryDirectory() as root:
            target = Path(root, 'test_exr.exr')
            image = np.zeros((10, 5), dtype=np.uint8)

            expected = 'EXR cannot be saved with array of dtype: uint8.'
            with self.assertRaisesRegex(TypeError, expected):
                tools.write_exr(target, image, {})

    def test_write_exr_metadata(self):
        with TemporaryDirectory() as root:
            target = Path(root, 'test_exr.exr')
            image = np.zeros((10, 5, 4), dtype=np.float32)
            tools.write_exr(target, image, {})

            expected = dict(
                channels=list('rgba'),
                foo='bar',
                compression='tacocat'
            )
            tools.write_exr(target, image, expected)
            _, result = tools.read_exr(target)
            self.assertEqual(result['channels'], expected['channels'])
            self.assertEqual(result['foo'], expected['foo'])
            self.assertNotEqual(
                str(result['compression']),
                expected['compression']
            )

    def test_write_exr_data(self):
        with TemporaryDirectory() as root:
            target = Path(root, 'test_exr.exr')

            expected = np.zeros((10, 5, 4), dtype=np.float16)
            expected[:, :, 0] *= 0.1
            expected[:, :, 1] *= 0.2
            expected[:, :, 2] *= 0.3
            expected[:, :, 3] *= 0.4

            tools.write_exr(target, expected, {})
            result, _ = tools.read_exr(target)
            self.assertEqual(result[:, :, 0].mean(), expected[:, :, 0].mean())
            self.assertEqual(result[:, :, 0].mean(), expected[:, :, 0].mean())
            self.assertEqual(result[:, :, 0].mean(), expected[:, :, 0].mean())
            self.assertEqual(result[:, :, 0].mean(), expected[:, :, 0].mean())

    def test_write_exr_compression(self):
        with TemporaryDirectory() as root:
            target = Path(root, 'test_exr.exr')
            image = np.zeros((10, 5, 4), dtype=np.float32)
            expected = ImageCodec.DWAB
            tools.write_exr(target, image, {}, codec=expected)
            _, result = tools.read_exr(target)
            self.assertEqual(result['compression'], expected)
