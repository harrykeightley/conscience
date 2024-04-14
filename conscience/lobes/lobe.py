import tkinter as tk
from typing import Optional

from behave.model import Scenario
from behave.runner import Context

from conscience.suite import ConscienceSuite


class Lobe:
    """A module which enhances the "Conscience" test suite with particular functionality.

    Historical: Changed name from Feature to avoid conflicts with 'behaviour.py' Features
    """

    def on_load(self, suite: ConscienceSuite) -> None:
        pass

    def on_start(self, context: Context, suite: ConscienceSuite) -> None:
        pass

    def failure_message(self, scenario: Scenario, step) -> Optional[str]:
        pass
