"""
Identify GUI widgets based on the functional characteristics
within an existing model.

Allows testing to occur in an environment where no knowledge
is known about the implementation details of the GUI.
"""

import tkinter as tk
from typing import Callable, List, TypeVar

from PIL import ImageTk

T = TypeVar("T")
Selector = Callable[[tk.Widget], bool]
Accessor = Callable[[tk.Widget], T]


def _widget_selector(parent: tk.Widget, selector: Selector):
    """Recursively generates all widgets in the tree from the parent node which match the selector"""
    if selector(parent):
        yield parent
    for child in parent.children.values():
        # for child in parent.winfo_children(): doesn't work as students override self._root
        yield from _widget_selector(child, selector)


def find_widgets(selector: Selector, widget: tk.Widget) -> List[tk.Widget]:
    """Find all widgets which match the supplied selector"""
    return list(_widget_selector(widget, selector))


# Helper method for generating selectors
def _build_selector[T](accessor: Accessor[T], expected: T) -> Selector:
    def selector(widget: tk.Widget):
        try:
            actual = accessor(widget)
            return actual == expected
        except tk.TclError:
            return False

    return selector


class WidgetSelector:
    """A class whose static methods identify GUI widgets based on the functional characteristics
    within an existing model."""

    @staticmethod
    def aggregate(*selectors: Selector) -> Selector:
        """Returns a composite selector which returns true iff all of its passed selectors return true."""

        def cb(widget):
            for selector in selectors:
                if not selector(widget):
                    return False
            return True

        return cb

    @staticmethod
    def by_text(expected: str) -> Selector:
        """A selector which returns true iff the supplied text exists on the widget"""
        return _build_selector(lambda widget: widget.cget("text"), expected)

    @staticmethod
    def by_rough_text(expected: str) -> Selector:
        """A selector which returns true iff the supplied text approximately exists on the widget."""

        def relax(text: str) -> str:
            return text.lower().strip()

        return _build_selector(lambda widget: relax(widget.cget("text")), expected)

    @staticmethod
    def by_label(expected: str) -> Selector:
        """A selector which returns true iff the expected string is found within a label"""
        return _build_selector(lambda widget: widget.cget("label").lower(), expected)

    @staticmethod
    def by_image[T](registry: dict[str, T], expected: T):
        """A selector which returns true iff the expected image is encountered and exists
        within the supplied registry."""

        def accessor(widget: tk.Widget) -> T | None:
            image_id = widget.cget("image")
            return registry.get(image_id)

        return _build_selector(accessor, expected)

    @staticmethod
    def by_image_name(cache: dict[str, ImageTk.PhotoImage], name: str):
        """A selector which returns true iff the expected image is encountered and exists
        within the supplied registry."""

        # for some reason tkinter stores only the strings of the image?
        return _build_selector(
            lambda widget: widget.cget("image"), str(cache.get(name))
        )

    @staticmethod
    def has_text():
        """A selector which returns true iff the supplied widget has text"""

        def f(widget):
            try:
                widget.cget("text")
                return True
            except tk.TclError:
                return False

        return f

    @staticmethod
    def by_type(expected):
        """A selector which returns true iff the encountered widget matches the supplied type"""

        def f(widget: tk.Widget):
            return isinstance(widget, expected)

        return f

    @staticmethod
    def by_class_name(expected: str):
        """A selector which matches all leaf nodes"""

        def f(widget):
            return widget.__class__.__name__ == expected

        return f

    @staticmethod
    def is_leaf():
        """A selector which matches all leaf nodes"""

        def f(widget):
            return not widget.children

        return f

    @staticmethod
    def all():
        """A selector which matches all widgets"""
        return lambda widget: True


class CanvasSelector:
    """A class whose static methods identify elements on a canvas based on the functional characteristics
    within an existing model."""

    @staticmethod
    def get_canvas_text(widget: tk.Canvas, expected: str) -> list[int]:
        """Finds all text elements on the canvas that match the given string.

        Returns:
            A list of the element ids on the canvas
        """
        found = []
        for item in widget.find_all():
            config = widget.itemconfig(item)
            if config is None:
                continue

            if "text" not in config:
                continue

            # TODO: why 4?
            if config["text"][4] == expected:
                found.append(item)

        return found

    @staticmethod
    def get_canvas_images[
        T
    ](registry: dict[str, T], canvas: tk.Canvas, expected: T,) -> list[int]:
        """Finds all image elements on the canvas that match the given type.

        Returns:
            A list of the element ids on the canvas
        """
        found = []
        for item in canvas.find_all():
            config = canvas.itemconfig(item)
            if config is None:
                continue

            if "image" not in config:
                continue

            # TODO: why 4?
            image_id = config["image"][4]
            if image_id not in registry:
                continue

            image_type = registry[image_id]
            if image_type == expected:
                found.append(item)

        return found
