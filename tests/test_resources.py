import unittest

from wiggler.core.resources import Resources
from wiggler.core.datastructures import OverlayDict


class BasicTest(unittest.TestCase):

    def setUp(self):
        self.resources = Resources()

    def runTest(self):
        with open("/tmp/log", 'w') as f:
            f.write(str(type(self.resources.sheets)))
        self.assertIs(type(self.resources.sheets), OverlayDict)


if __name__ == '__main__':
    unittest.main()
