"""
Test the assignment that was originally used to develop this project.
"""
import unittest
from behave.__main__ import main as run_behave


class TestDayZ(unittest.TestCase):
    def test_dayz(self):
        run_behave(["tests/dayz"])


if __name__ == '__main__':
    unittest.main()
