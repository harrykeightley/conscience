"""
Identify GUI widgets based on the functional characteristics
within an existing model.

Allows testing to occur in an environment where no knowledge
is known about the implementation details of the GUI.
"""
import tkinter as tk
from typing import List
from . import logger


def _widget_selector(parent, selector):
    if selector(parent):
        yield parent
    for child in parent.children.values():
    #for child in parent.winfo_children(): doesn't work as students override self._root
        yield from _widget_selector(child, selector)


def find_widgets(selector, widget) -> List[tk.Widget]:
    return list(_widget_selector(widget, selector))


class WidgetSelector:
    @staticmethod
    def aggregate(*selectors):
        def cb(widget):
            for selector in selectors:
                if not selector(widget):
                    return False
            return True

        return cb

    @staticmethod
    def by_text(expected):
        def f(widget):
            try:
                actual = widget.cget("text")
                return actual == expected
            except tk.TclError:
                return False
        
        return f

    @staticmethod
    def by_rough_text(expected):
        def f(widget):
            try:
                actual = widget.cget("text").lower().strip()
                return actual == expected
            except tk.TclError:
                return False
        
        return f

    @staticmethod
    def get_canvas_text(widget, expected):
        found = []
        for item in widget.find_all():
            config = widget.itemconfig(item)
            if "text" in config:
                if config["text"][4] == expected:
                    found.append(item)
        return found

    @staticmethod
    def get_canvas_image(registry, widget, expected):
        found = []
        for item in widget.find_all():
            config = widget.itemconfig(item)
            if "image" in config:
                image_id = config["image"][4]
                if image_id in registry:
                    image_type = registry[image_id]
                    if image_type == expected:
                        found.append(item)
        return found

    @staticmethod
    def by_label(expected):
        def f(widget):
            try:
                actual = widget.cget("label").lower()
                print(actual)
                return expected in actual
            except tk.TclError:
                return False

        return f

    @staticmethod
    def has_text():
        def f(widget):
            try:
                widget.cget("text")
                return True
            except tk.TclError:
                return False
        return f

    @staticmethod
    def by_type(expected):
        def f(widget):
            return isinstance(widget, expected)
        return f

    @staticmethod
    def by_class_name(expected):
        def f(widget):
            return widget.__class__.__name__ == expected
        return f

    @staticmethod
    def is_leaf():
        def f(widget):
            return not widget.children
        return f

    @staticmethod
    def all():
        def f(widget):
            return True
        return f
