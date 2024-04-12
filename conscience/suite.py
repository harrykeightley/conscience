"""
suite = DirectorSuite()
suite.seed = 10017030
suite.overwrite("TASK", 1)

mocker = Mocker()
mocker.mock(tk.Tk, "mainloop")
mocker.mock(tk.Tk, "after")
mocker.mock(tk.Tk, "bind")
suite.mocker = mocker

after = suite.enable("after")
binds = suite.enable("bind")
images = suite.enable("images")

warnings = suite.warnings
warnings.Tk_destroy = "you should not close the window with .destroy - reset the model and redraw the view instead"
warnings.Widget_destroy = "you should not use the .destroy method - gracefully reconfigure the updated widgets using the .config method"
"""

from dataclasses import dataclass, field
import random
import tkinter as tk
import traceback
from typing import Any, Optional

from loguru import logger


def warn(message):
    def inner(*args, **kwargs):
        stack = traceback.format_stack()
        stack = filter(lambda log: "a3.py" in log, stack)
        logger.warning("".join(stack))
        logger.warning(message)

    return inner


# NOTE: omitting lobe type to avoid circular dependency


@dataclass
class DirectorSuite:
    seed: Optional[int] = None
    _overwrites: dict[str, Any] = field(default_factory=dict)
    _warnings: list[tuple[Any, Any, str]] = field(default_factory=list)
    _lobes: list = field(default_factory=list)

    def enable(self, feature):
        self._lobes.append(feature)

    def overwrite(self, variable, value):
        self._overwrites[variable] = value

    def warn_on(self, clz, method, message: str):
        self._warnings.append((clz, method, message))

    def load(self):
        for lobe in self._lobes:
            lobe.on_load(self)

    def on_fail(self, scenario, step):
        message = ""
        for feature in self._lobes:
            feature_message = feature.failure_message(scenario, step)
            if feature_message is not None:
                message += feature_message

        return message or None

    def start(self, context):
        if self.seed is not None:
            random.seed(self.seed)

        for variable, value in self._overwrites.items():
            setattr(context.under_test, variable, value)

        for clz, method, message in self._warnings:
            setattr(clz, method, warn(message))

        for feature in self._lobes:
            feature.on_start(context, self)

        self.window = tk.Tk()
