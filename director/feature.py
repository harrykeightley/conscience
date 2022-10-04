import tkinter as tk
from tkinter import messagebox
from tkinter.commondialog import Dialog
from tkinter.simpledialog import _QueryDialog
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
            

class MockMessagebox(Feature):
    def on_load(self, suite):
        @when("I get prompted I will say \"{answer:Text}\"")
        def set_response(context, answer):
            old_messagebox = copy_function(messagebox._show)
            def inject_messagebox(title=None, message=None, _icon=None, _type=None, **options):
                return answer
            setattr(messagebox, "_show", inject_messagebox)

            old_dialog = copy_function(Dialog.show)
            def inject_dialog(self, **options):
                return answer
            setattr(Dialog, "show", inject_dialog)

            def inject_query_dialog(self, *args, **kwargs):
                setattr(self, "getresult", lambda self: answer)
            setattr(_QueryDialog, "__init__", inject_query_dialog)

    def on_start(self, context, suite):
        context.message_boxes = VacantLog(messagebox, "_show")
        context.dialog = VacantLog(Dialog, "show")

        @then("no messageboxes have been displayed")
        def no_messageboxes(context):
            assert len(context.message_boxes.logs) == 0,\
                    f"found {len(context.message_boxes.logs)} calls create messageboxes: {context.message_boxes.logs}"
            assert len(context.dialog.logs) == 0,\
                    f"found {len(context.dialog.logs)} calls create dialogs: {context.dialog.logs}"

        @then("a messagebox should be displayed")
        def messagebox_displayed(context):
            potential_calls = context.message_boxes.logs + context.dialog.logs
            assert len(potential_calls) == 1,\
                    f"found {len(potential_calls)} calls create messageboxes: {potential_calls}"
            
        @then("the messagebox should say \"{text}\"")
        def messagebox_text(context, text):
            potential_calls = context.message_boxes.logs + context.dialog.logs
            assert len(potential_calls) == 1,\
                    f"found {len(potential_calls)} calls create messageboxes: {potential_calls}"

            found = False
            for positional, keywords in potential_calls:
                if text in positional or text in keywords.values():
                    found = True
                    break
            
            assert found, f"did not find messagebox with text {text} in {potential_calls}"

