import tkinter as tk
from tkinter import messagebox
from tkinter.commondialog import Dialog
from tkinter.simpledialog import _QueryDialog

from behave import *

from director.lobes.lobe import Lobe
from director.mocking import VacantLog, copy_function


class MockMessagebox(Lobe):
    def on_load(self, suite):
        @when('I get prompted I will say "{answer:Text}"')
        def set_response(context, answer):
            old_messagebox = copy_function(messagebox._show)

            def inject_messagebox(
                title=None, message=None, _icon=None, _type=None, **options
            ):
                return answer

            setattr(messagebox, "_show", inject_messagebox)

            old_dialog = copy_function(Dialog.show)

            def inject_dialog(self, **options):
                return answer

            setattr(Dialog, "show", inject_dialog)

            def inject_query_dialog(self, *args, **kwargs):
                setattr(self, "getresult", lambda self: answer)

            setattr(_QueryDialog, "__init__", inject_query_dialog)

        @when("I get prompted I will answer in the affirmative")
        def set_response_positive(context):
            old_messagebox = copy_function(messagebox._show)

            def inject_messagebox(
                title=None, message=None, _icon=None, _type=None, **options
            ):
                return "yes"

            setattr(messagebox, "_show", inject_messagebox)

            old_dialog = copy_function(Dialog.show)

            def inject_dialog(self, **options):
                return "yes"

            setattr(Dialog, "show", inject_dialog)

            def inject_query_dialog(self, *args, **kwargs):
                setattr(self, "getresult", lambda self: "yes")

            setattr(_QueryDialog, "__init__", inject_query_dialog)

        @when("I get prompted I will answer in the negative")
        def set_response_negative(context):
            old_messagebox = copy_function(messagebox._show)

            def inject_messagebox(
                title=None, message=None, _icon=None, _type=None, **options
            ):
                return "no"

            setattr(messagebox, "_show", inject_messagebox)

            old_dialog = copy_function(Dialog.show)

            def inject_dialog(self, **options):
                return "no"

            setattr(Dialog, "show", inject_dialog)

            def inject_query_dialog(self, *args, **kwargs):
                setattr(self, "getresult", lambda self: "no")

            setattr(_QueryDialog, "__init__", inject_query_dialog)

    def on_start(self, context, suite):
        context.message_boxes = VacantLog(messagebox, "_show")
        context.dialog = VacantLog(Dialog, "show")

        @then("no messageboxes have been displayed")
        def no_messageboxes(context):
            assert (
                len(context.message_boxes.logs) == 0
            ), f"found {len(context.message_boxes.logs)} calls create messageboxes: {context.message_boxes.logs}"
            assert (
                len(context.dialog.logs) == 0
            ), f"found {len(context.dialog.logs)} calls create dialogs: {context.dialog.logs}"

        @then("a messagebox should be displayed")
        def messagebox_displayed(context):
            potential_calls = context.message_boxes.logs + context.dialog.logs
            assert (
                len(potential_calls) == 1
            ), f"found {len(potential_calls)} calls create messageboxes: {potential_calls}"

        @then('the messagebox should say "{text}"')
        def messagebox_text(context, text):
            potential_calls = context.message_boxes.logs + context.dialog.logs
            assert (
                len(potential_calls) == 1
            ), f"found {len(potential_calls)} calls create messageboxes: {potential_calls}"

            found = False
            for positional, keywords in potential_calls:
                if text in positional or text in keywords.values():
                    found = True
                    break

            assert (
                found
            ), f"did not find messagebox with text {text} in {potential_calls}"
