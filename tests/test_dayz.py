"""
Test the assignment that was originally used to develop this project.
"""

from pathlib import Path
import unittest

from conscience import build_config, setup_config, witness
from conscience.suite import ConscienceSuite


class TestDayZ(unittest.TestCase):
    def test_dayz(self):
        suite = ConscienceSuite()
        config = build_config(is_gradescope=True)
        setup_config(
            config,
            suite,
            tests=[Path("tests/dayz/features")],
            steps_dir=Path("../steps"),
            environment_file=Path("environment.py"),
        )
        witness(config, Path("tests/dayz/dayz.py"))


if __name__ == "__main__":
    unittest.main()
