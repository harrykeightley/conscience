from behave import *
from .identify import *
from .formats import register_formats

register_formats()


@then("I see text displaying, roughly, \"{text:Text}\"")
def rough_text(context, text):
    search_for = text.lower().strip()
    widgets = find_widgets(WidgetSelector.by_rough_text(search_for), context.window)
    assert len(widgets) == 1, f"cannot find exactly one widget roughly matching the text \"{text}\", found {widgets}"


@then("I see text displaying, exactly, {text:Text}")
def exact_text(context, text):
    widgets = find_widgets(WidgetSelector.by_text(text), context.window)
    assert len(widgets) == 1, f"cannot find exactly one widget exactly matching the text \"{text}\", found {widgets}"
