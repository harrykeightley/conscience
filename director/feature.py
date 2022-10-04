import tkinter as tk
from behave import *
from . import *
from .features.keyboard import Events, press
from .features.design import load_design_tests

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
