from behave import *
from .identify import *
from .formats import RelativePosition, register_formats

register_formats()


@then("I see text displaying, roughly, \"{text:Text}\"")
def rough_text(context, text):
    search_for = text.lower().strip()
    widgets = find_widgets(WidgetSelector.by_rough_text(search_for), context.window)
    assert len(widgets) == 1, f"cannot find exactly one widget roughly matching the text \"{text}\", found {widgets}"
    context.last = widgets[0]


@then("I see text displaying, exactly, {text:Text}")
def exact_text(context, text):
    widgets = find_widgets(WidgetSelector.by_text(text), context.window)
    assert len(widgets) == 1, f"cannot find exactly one widget exactly matching the text \"{text}\", found {widgets}"
    context.last = widgets[0]


@then("it is {position:RelativePosition} all other widgets")
def relative_to_all(context, position):
    widgets = find_widgets(WidgetSelector.all(), context.window)
    it: tk.Widget = context.last
    its_position = it.winfo_x(), it.winfo_y()

    for widget in widgets:
        position = widget.winfo_x(), it.winfo_y()
        if position == RelativePosition.Left:
            assert its_position[0] < position[0], f"{widget} is further left than {it}"
        elif position == RelativePosition.Right:
            assert its_position[0] > position[0], f"{widget} is further right than {it}"
        elif position == RelativePosition.Above:
            assert its_position[1] < position[1], f"{widget} is above {it}"
        elif position == RelativePosition.Below:
            assert its_position[1] > position[1], f"{widget} is below {it}"
