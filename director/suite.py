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

from director.lobes import Lobe
from director import logger


def warn(message):
    def inner(*args, **kwargs):
        stack = traceback.format_stack()
        stack = filter(lambda log: "a3.py" in log, stack)
        logger.warn("".join(stack))
        logger.warn(message)

    return inner


@dataclass
class DirectorSuite:
    seed: Optional[int] = None
    _overwrites: dict[str, Any] = field(default_factory=dict)
    _warnings: list[tuple[Any, Any, str]] = field(default_factory=list)
    _features: list[Lobe] = field(default_factory=list)

    def enable(self, feature: Lobe):
        self._features.append(feature)

    def overwrite(self, variable, value):
        self._overwrites[variable] = value

    def warn_on(self, clz, method, message: str):
        self._warnings.append((clz, method, message))

    def load(self):
        for feature in self._features:
            feature.on_load(self)

    def on_fail(self, scenario, step):
        message = ""
        for feature in self._features:
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

        for feature in self._features:
            feature.on_start(context, self)

        self.window = tk.Tk()
