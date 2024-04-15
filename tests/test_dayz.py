"""
Test the assignment that was originally used to develop this project.
"""

from pathlib import Path
import unittest

from conscience import run_tests, build_config, setup_config
from conscience.suite import ConscienceSuite


class TestDayZ(unittest.TestCase):
    def test_dayz(self):

        suite = ConscienceSuite()
        config = build_config()
        setup_config(config, 
                     suite, 
                     tests=[Path("tests/dayz/features")], 
                     environment_file=Path("tests/dayz/features/environment.py"))
        run_tests(config, Path("tests/dayz/dayz.py"))


if __name__ == "__main__":
    unittest.main()
