from behave import *
from conscience.lib.mocking import VacantLog
from conscience import load_common_steps

import tkinter as tk

load_common_steps()


@given("I start the application")
def startup(context):
    VacantLog(tk.Tk, "mainloop")

    root = tk.Tk()
    context.window = root

    context.under_test.setup_display(root)
    print(root.winfo_id())

    root.mainloop()
