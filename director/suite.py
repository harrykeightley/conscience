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
import random
import tkinter as tk
import traceback

from .common import logger


def warn(message):
    def inner(*args, **kwargs):
        stack = traceback.format_stack()
        stack = filter(lambda log: "a3.py" in log, stack)
        logger.warn("".join(stack))
        logger.warn(message)

    return inner

class DirectorSuite:
    def __init__(self, seed=None):
        self.seed = seed
        self._overwrites = {}
        self._warnings = []

    def overwrite(self, variable, value):
        self._overwrites[variable] = value
    
    def warn_on(self, clz, method, message):
        self._warnings.append((clz, method, message))
    
    def start(self, context):
        if self.seed is not None:
            random.seed(self.seed)

        for variable, value in self._overwrites.items():
            setattr(context.under_test, variable, value)

        for clz, method, message in self._warnings:
            setattr(clz, method, warn(message))

        self.window = tk.Tk()
