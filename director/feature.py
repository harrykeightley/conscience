from . import *
import tkinter as tk

class Feature:
    def on_start(self, context, suite):
        pass


class PreventMainloop(Feature):
    def on_start(self, context, suite):
        VacantLog(tk.Tk, "mainloop")

