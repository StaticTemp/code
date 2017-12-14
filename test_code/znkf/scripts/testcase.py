import unittest
import sys

sys.path.append("..")

from scripts.test_management import *
from scripts.pachong import *


class TestCase(unittest.TestCase):
    def setUp(self):
        self.test = TestManagement()

    def tearDown(self):
        pass

    def test_repository_add(self):
        self.test.repository_add()

    def test_repository_delete(self):
        self.test.repository_delete()


if __name__ == "__main__":
    ts = unittest.TestSuite()
    ts.addTest(TestCase('test_repository_add'))
    ts.addTest(TestCase('test_repository_delete'))
    runner = unittest.TextTestRunner()
    runner.run(ts)
