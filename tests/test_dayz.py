"""
Test the assignment that was originally used to develop this project.
"""
from director.mocking import MixinBase
import unittest
from behave.__main__ import main as run_behave

class TestCoreMock(unittest.TestCase):
    def test_dayz(self):
        run_behave(["tests/dayz"])


if __name__ == '__main__':
    unittest.main()