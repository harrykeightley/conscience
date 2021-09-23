"""
Test a very simple GUI.
"""
import sys
import logging
logger = logging.getLogger("director")
# logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

import unittest
from behave.__main__ import run_behave
from behave.__main__ import Configuration

import importlib.util


def load_under_test(path):
    spec = importlib.util.spec_from_file_location("under_test", path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo

class TestHelloWorld(unittest.TestCase):
    def test_hello_world(self):
        config = Configuration("tests/test_hello_world")
        config.steps_dir = "."
        config.under_test = load_under_test("tests/hello_world/hello_world_gui.py")
        run_behave(config)


if __name__ == '__main__':
    unittest.main()
