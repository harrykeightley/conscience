"""
Test a very simple GUI.
"""

from pathlib import Path
import sys
from loguru import logger
from conscience.main import setup

from conscience.suite import ConscienceSuite

logger.add(sys.stdout)

import unittest

from conscience import run_tests, build_config, setup_config, setup


class TestHelloWorld(unittest.TestCase):
    def test_hello_world(self):
        suite = ConscienceSuite()
        config = build_config()
        setup_config(config, suite, tests=[Path("tests/hello_world_tests")])
        run_tests(config, Path("tests/hello_world/hello_world_gui.py"))


if __name__ == "__main__":
    unittest.main()
