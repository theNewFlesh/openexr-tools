import unittest

from lunchbox.enforce import EnforceError

from openexr_tools.enum import ImageCodec
# ------------------------------------------------------------------------------


class ImageCodecTests(unittest.TestCase):
    def test_repr(self):
        x = ImageCodec.PXR24
        result = repr(x)
        expected = '''
<ImageCodec.PXR24>
  string: pxr24
exr_code: 5'''[1:]
        self.assertEqual(result, expected)

    def test_from_exr_code(self):
        self.assertEqual(ImageCodec.from_exr_code(0), ImageCodec.UNCOMPRESSED)
        self.assertEqual(ImageCodec.from_exr_code(1), ImageCodec.RLE)
        self.assertEqual(ImageCodec.from_exr_code(2), ImageCodec.ZIPS)
        self.assertEqual(ImageCodec.from_exr_code(3), ImageCodec.ZIP)
        self.assertEqual(ImageCodec.from_exr_code(4), ImageCodec.PIZ)
        self.assertEqual(ImageCodec.from_exr_code(5), ImageCodec.PXR24)
        self.assertEqual(ImageCodec.from_exr_code(6), ImageCodec.B44)
        self.assertEqual(ImageCodec.from_exr_code(7), ImageCodec.B44A)
        self.assertEqual(ImageCodec.from_exr_code(8), ImageCodec.DWAA)
        self.assertEqual(ImageCodec.from_exr_code(9), ImageCodec.DWAB)

    def test_from_exr_code_errors(self):
        expected = 'Value given is not an integer. bar !=.*int'
        with self.assertRaisesRegexp(EnforceError, expected):
            ImageCodec.from_exr_code('bar')

        expected = 'EXR code 99 has no legal ImageCodec type. '
        expected += 'Legal EXR codes: .*'
        with self.assertRaisesRegexp(EnforceError, expected):
            ImageCodec.from_exr_code(99)
