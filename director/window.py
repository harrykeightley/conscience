from behave import *
from .formats import register_formats

register_formats()

@then("the window title is \"{title:Text}\"")
def window_title(context, title):
    assert context.window.title() == title, f"expected window title to be \"{title}\", but it was \"{context.window.title}\""

