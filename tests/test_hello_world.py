"""
Test a very simple GUI.
"""
import sys
import logging
logger = logging.getLogger("director")
# logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

import unittest

from director import test


class TestHelloWorld(unittest.TestCase):
    def test_hello_world(self):
        test("tests/hello_world_tests", "tests/hello_world/hello_world_gui.py")


if __name__ == '__main__':
    unittest.main()
