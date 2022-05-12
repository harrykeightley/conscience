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


class DirectorSuite:
    def __init__(self, seed=None):
        self.seed = seed
        self._overwrites = {}

    def overwrite(self, variable, value):
        self._overwrites[variable] = value
    
    def start(self, context):
        if self.seed is not None:
            random.seed(self.seed)

        for variable, value in self._overwrites.items():
            setattr(context.under_test, variable, value)

        self.window = tk.Tk()
