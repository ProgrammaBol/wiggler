import unittest

from wiggler.core.resources import Resources


class BasicTest(unittest.TestCase):

    def setUp(self):
        self.resources = Resources()

    def runTest(self):
        self.assertIsInstance(self.resources.sheets, dict)


if __name__ == '__main__':
    unittest.main()
