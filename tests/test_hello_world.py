"""
Test a very simple GUI.
"""

from pathlib import Path

import unittest

from conscience import build_config, setup_config, witness
from conscience.suite import ConscienceSuite


class TestHelloWorld(unittest.TestCase):
    def test_hello_world(self):
        suite = ConscienceSuite()
        config = build_config(is_gradescope=False)
        setup_config(
            config,
            suite,
            tests=[Path("tests/hello_world_tests")],
            steps_dir=Path("steps"),
            environment_file=Path("environment.py"),
        )
        results = witness(config, Path("tests/hello_world/hello_world_gui.py"))


class TestHelloWorldGradeScope(unittest.TestCase):
    def test_hello_world(self):
        suite = ConscienceSuite()
        config = build_config(is_gradescope=True)
        setup_config(
            config,
            suite,
            tests=[Path("tests/hello_world_tests")],
            steps_dir=Path("steps"),
            environment_file=Path("environment.py"),
        )
        results = witness(config, Path("tests/hello_world/hello_world_gui.py"))
        print(results)


if __name__ == "__main__":
    unittest.main()
