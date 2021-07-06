"""
Ensure a correct environment has been established
"""
import unittest

class TestEnvironment(unittest.TestCase):

    def test_behave(self):
        try:
            import behave
        except ImportError as e:
            self.fail("behave library is not available")

    def test_tkinter(self):
        try:
            import tkinter
        except ImportError as e:
            self.fail("tkinter library is not available")


if __name__ == '__main__':
    unittest.main()