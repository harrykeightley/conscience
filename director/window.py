from behave import *
from .parsers import register_parsers

register_parsers()


@then('the window title is "{title:Text}"')
def window_title(context, title):
    assert (
        context.window.title() == title
    ), f'expected window title to be "{title}", but it was "{context.window.title}"'
