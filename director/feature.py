import tkinter as tk
from behave import *
from . import *
from .keyboard import Events, press

class Feature:
    def on_start(self, context, suite):
        pass


class PreventMainloop(Feature):
    def on_start(self, context, suite):
        VacantLog(tk.Tk, "mainloop")


class TrackKeypresses(Feature):
    def on_start(self, context, suite):
        TrackKeypresses._enabled = True
        context.key_binds = VacantLog(tk.Tk, "bind")

    @when("I press {key}")
    @staticmethod
    def press_key(context, key):
        if not hasattr(TrackKeypresses, "_enabled"):
            raise Exception("TrackKeypresses feature has not been enabled")
        event = getattr(Events, key.upper())
        press(context, event)
