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
        with self.assertRaisesRegex(EnforceError, expected):
            ImageCodec.from_exr_code('bar')

        expected = 'EXR code 99 has no legal ImageCodec type. '
        expected += 'Legal EXR codes: .*'
        with self.assertRaisesRegex(EnforceError, expected):
            ImageCodec.from_exr_code(99)

    def test_from_string(self):
        self.assertEqual(ImageCodec.from_string('b44'), ImageCodec.B44)
        self.assertEqual(ImageCodec.from_string('b44a'), ImageCodec.B44A)
        self.assertEqual(ImageCodec.from_string('dwaa'), ImageCodec.DWAA)
        self.assertEqual(ImageCodec.from_string('dwab'), ImageCodec.DWAB)
        self.assertEqual(ImageCodec.from_string('piz'), ImageCodec.PIZ)
        self.assertEqual(ImageCodec.from_string('pxr24'), ImageCodec.PXR24)
        self.assertEqual(ImageCodec.from_string('rle'), ImageCodec.RLE)
        self.assertEqual(ImageCodec.from_string('uncompressed'), ImageCodec.UNCOMPRESSED)
        self.assertEqual(ImageCodec.from_string('zip'), ImageCodec.ZIP)
        self.assertEqual(ImageCodec.from_string('zips'), ImageCodec.ZIPS)

    def test_from_string_errors(self):
        expected = 'Value given is not a string. 77 !=.*str'
        with self.assertRaisesRegex(EnforceError, expected):
            ImageCodec.from_string(77)

        expected = '"taco" has no legal ImageCodec type. '
        expected += 'Legal codec strings: .*'
        with self.assertRaisesRegex(EnforceError, expected):
            ImageCodec.from_string('taco')
