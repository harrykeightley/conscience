import tkinter as tk
from behave import *
from . import *
from .features.keyboard import Events, press
from .features.design import load_design_tests
from .features.after import AfterSimulator

class Feature:
    def on_load(self, suite):
        pass

    def on_start(self, context, suite):
        pass


class CodeDesign(Feature):
    def on_load(self, suite):
        load_design_tests()


class PreventMainloop(Feature):
    def on_start(self, context, suite):
        VacantLog(tk.Tk, "mainloop")


class TrackKeypresses(Feature):
    def on_start(self, context, suite):
        TrackKeypresses._enabled = True
        context.key_binds = VacantLog(tk.Tk, "bind")

        @when("I press {key}")
        def press_key(context, key):
            event = getattr(Events, key.upper())
            press(context, event)


class MockAfter(Feature):
    def on_start(self, context, suite):
        context.after = AfterSimulator()
        after_mock = MockLog(tk.Tk, "after")
        after_mock.register(context.after.after)
        after_mock = MockLog(tk.Widget, "after")
        after_mock.register(context.after.after)
        after_canel_mock = MockLog(tk.Tk, "after_cancel")
        after_canel_mock.register(context.after.after_cancel)
        after_canel_mock = MockLog(tk.Widget, "after_cancel")
        after_canel_mock.register(context.after.after_cancel)

        @when("one second passes")
        def one_second_passes(context):
            context.after.step(1000)

        @when("{seconds:d} seconds pass")
        def seconds_passes(context, seconds):
            context.after.step(seconds * 1000)
            
