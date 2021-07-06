"""
Ensure a correct environment has been established
"""
import unittest

class TestEnvironment(unittest.TestCase):

    def test_behave(self):
        """test the behave library is installed"""
        try:
            import behave
        except ImportError as e:
            self.fail("behave library is not available")

    def test_tkinter(self):
        """test the tkinter library is installed"""
        try:
            import tkinter
        except ImportError as e:
            self.fail("tkinter library is not available")

    def test_directory(self):
        """test the directory library is accessible"""
        try:
            import director
        except ImportError as e:
            self.fail("directory library is not accessible")


if __name__ == '__main__':
    unittest.main()