"""
Test a very simple GUI.
"""

import sys
from loguru import logger

from conscience.suite import DirectorSuite

logger.add(sys.stdout)

import unittest

from conscience import test as ponder


class TestHelloWorld(unittest.TestCase):
    def test_hello_world(self):
        suite = DirectorSuite()
        ponder(
            "tests/hello_world_tests",
            "tests/hello_world/hello_world_gui.py",
            suite=suite,
        )


if __name__ == "__main__":
    unittest.main()
