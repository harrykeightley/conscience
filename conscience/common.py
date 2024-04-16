from difflib import ndiff
from functools import partial
from behave import *
import tkinter as tk

from behave.runner import Context

from conscience.lib.identify import WidgetSelector, CanvasSelector, find_widgets
from conscience.parsers import RelativePosition, register_parsers
from conscience.lobes.keyboard import press, Events

register_parsers()


def assertEquals(expected: str, actual: str):
    assert actual == expected, "\n" + "".join(
        ndiff(actual.splitlines(keepends=True), expected.splitlines(keepends=True))
    )


@then('the window title is "{title:Text}"')
def window_title(context: Context, title: str):
    assert (
        context.window.title() == title
    ), f'expected window title to be "{title}", but it was "{context.window.title}"'


@then('I see text displaying, roughly, "{text:Text}"')
def rough_text(context: Context, text: str):
    search_for = text.lower().strip()
    widgets = find_widgets(WidgetSelector.by_rough_text(search_for), context.window)
    assert (
        len(widgets) == 1
    ), f'cannot find exactly one widget roughly matching the text "{text}", found {widgets}'
    context.last = widgets[0]


@then("I see text displaying, exactly, {text:Text}")
def exact_text(context: Context, text: str):
    widgets = find_widgets(WidgetSelector.by_text(text), context.window)
    assert (
        len(widgets) == 1
    ), f'cannot find exactly one widget exactly matching the text "{text}", found {widgets}'
    context.last = widgets[0]


@then("it is {position:RelativePosition} all other widgets")
def relative_to_all(context: Context, position: RelativePosition):
    widgets = find_widgets(WidgetSelector.all(), context.window)
    it: tk.Widget = context.last
    last_x, last_y = it.winfo_x(), it.winfo_y()

    for widget in widgets:
        x, y = widget.winfo_x(), widget.winfo_y()
        if position == RelativePosition.Left:
            assert last_x <= x, f"{widget} is further left than {it}"
        elif position == RelativePosition.Right:
            assert last_x >= x, f"{widget} is further right than {it}"
        elif position == RelativePosition.Above:
            assert last_y <= y, f"{widget} is above {it}"
        elif position == RelativePosition.Below:
            assert last_y >= y, f"{widget} is below {it}"


def assert_widget_height(widget: tk.Widget, pixels: int, tolerance: int = 0) -> None:
    height = widget.winfo_height()
    error = abs(height - int(pixels))
    assert error <= tolerance, f"Widget height is {height} pixels, not {pixels} pixels."


def assert_widget_width(widget: tk.Widget, pixels: int, tolerance: int = 0) -> None:
    width = widget.winfo_width()
    error = abs(width - int(pixels))
    assert error <= tolerance, f"Widget width is {width} pixels, not {pixels} pixels."


@then("it is {pixels} pixels wide")
def last_width(context: Context, pixels: int) -> None:
    assert_widget_width(context.last, pixels, 20)


@then("it is {pixels} pixels tall")
def last_height(context: Context, pixels: int) -> None:
    assert_widget_height(context.last, pixels, 20)


def assert_single_widget_of_class(context: Context, clazz: str):
    widgets = find_widgets(WidgetSelector.by_class_name(clazz), context.window)
    assert len(widgets) != 0, f"No widget of class {clazz} found in GUI"
    assert len(widgets) == 1, f"More than one widget of class {clazz} found in GUI"


def get_first_widget_of_class(context: Context, clazz: str) -> tk.Widget:
    widgets = find_widgets(WidgetSelector.by_class_name(clazz), context.window)
    return widgets[0]


@then("a {clazz} instance should be packed within the GUI")
def single_class_packed(context: Context, clazz: str):
    assert_single_widget_of_class(context, clazz)
    context.last = get_first_widget_of_class(context, clazz)


@then("an {clazz} instance should be packed within the GUI")
def single_an_class_packed(context: Context, clazz: str):
    return single_class_packed(context, clazz)


@then("{count:d} {clazz} instances should be packed within the GUI")
def multiple_classes_packed(context: Context, count: int, clazz: str):
    widgets = find_widgets(WidgetSelector.by_class_name(clazz), context.window)
    assert (
        len(widgets) == count
    ), f"Expected {count} {clazz} instances, but found {len(widgets)}"


@then("the {clazz} should have a background color of {color}")
def widget_background_color(context: Context, clazz: str, color: str):
    widget = get_first_widget_of_class(context, clazz)
    assert (
        widget.cget("bg") == color
    ), f"Widget background color is {widget.cget('bg')}, not {color}"


@then("the {clazz} should have {count:d} text items")
def widget_text_count(context: Context, clazz: str, count: int):
    widget = get_first_widget_of_class(context, clazz)
    children = find_widgets(WidgetSelector.by_class_name(clazz), widget)
    text_count = sum(1 for item in children if widget.winfo_name() == "text")
    assert text_count == count, f"Widget has {text_count} text items, expected {count}"


# I think it's broken
# @then("that text item should have a text of {text}")
# def widget_text_content(context, text):
#     widget = get_widget(context, "GameGrid")
#     assert (
#         widget.itemcget(context.that, "text") == text
#     ), f"Text item has text {widget.itemcget(context.that, 'text')}, not {text}"


@when("I press the {key} key, {count:d} times")
def when_i_press_n(context: Context, key: str, count: int):
    key = key.strip()
    for _ in range(count):
        event = getattr(Events, key.upper())
        press(context, event)


@when("I repeat the sequence of keys {sequence} {count:d} times")
def repeat_key_sequence(context: Context, sequence: str, count: int):
    moves = sequence.strip()

    for _ in range(count):
        for move in moves:
            event = getattr(Events, move.upper())
            press(context, event)
            context.after.step(2000)
            context.window.update()


def click(widget: tk.Widget, button=1):
    widget.event_generate(
        f"<ButtonPress-{button}>", x=widget.winfo_x(), y=widget.winfo_y()
    )
