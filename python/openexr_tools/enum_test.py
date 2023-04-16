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
