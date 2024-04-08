import tkinter as tk

from behave.runner import Context
from behave import *

from director.lib.mocking import MockLog
from director.lobes.lobe import Lobe


class MockAfter(Lobe):
    def on_start(self, context, suite):
        context.after = AfterSimulator()
        after_mock = MockLog(tk.Tk, "after")
        after_mock.register(context.after.after)
        after_mock = MockLog(tk.Widget, "after")
        after_mock.register(context.after.after)

        after_cancel_mock = MockLog(tk.Tk, "after_cancel")
        after_cancel_mock.register(context.after.after_cancel)
        after_cancel_mock = MockLog(tk.Widget, "after_cancel")
        after_cancel_mock.register(context.after.after_cancel)

        @when("one second passes")
        def one_second_passes(context: Context):
            context.after.step(1000)

        @when("{seconds:d} seconds pass")
        def seconds_passes(context: Context, seconds: float):
            context.after.step(seconds * 1000)


class AfterSimulator:
    """Simulates .after bindings in tkinter"""

    def __init__(self) -> None:
        self._bind_id = 0
        self._bindings = []
        self._step = 0

    def step(self, step=1):
        if len(self._bindings) == 0:
            print("no calls to after")
        for i in range(1, step + 1):
            for _, time, callback in self._bindings[:]:
                if time == self._step + 1:
                    callback()
                    self._bindings.pop(0)
            self._step += 1

    def after(self, time, callback):
        self._bind_id += 1
        self._bindings.append((self._bind_id, self._step + time, callback))
        return self._bind_id

    def after_cancel(self, bind_id, *args):
        to_remove = []
        for i, (_id, _, _callback) in enumerate(self._bindings):
            if _id == bind_id:
                to_remove.append(i)

        for i in to_remove:
            removed = self._bindings.pop(i)
