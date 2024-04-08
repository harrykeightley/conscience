import tkinter as tk
from director.lobes.lobe import Lobe
from director.mocking import VacantLog, copy_function

from behave import *


class PreventMainloop(Lobe):
    def on_start(self, context, suite):
        VacantLog(tk.Tk, "mainloop")
        VacantLog(tk.Widget, "mainloop")


class MockDestroy(Lobe):
    old_destroy = copy_function(tk.Tk.destroy)

    def on_start(self, context, suite):
        context.destroyed = []

        def inject_destroy(self):
            MockDestroy.old_destroy(self)
            context.destroyed.append(self)

        setattr(tk.Tk, "destroy", inject_destroy)

        @then("the window should be closed")
        def window_closed(context):
            assert (
                len(context.destroyed) == 1
            ), f"found {len(context.destroyed)} calls to destroy (needed 1): {context.destroyed}"

        @then("the window should not be closed")
        def window_not_closed(context):
            assert (
                len(context.destroyed) == 0
            ), f"found {len(context.destroyed)} calls to destroy (needed 0): {context.destroyed}"


class ExceptionURL(Lobe):
    def __init__(self, exception, url):
        self._exception = exception
        self._url = url

    def failure_message(self, scenario, step):
        if self._exception in step.error_message:
            return f"{self._exception} was raised\nThe following EdStem post may be helpful:\n\t{self._url}"
