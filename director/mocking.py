"""
Mock core components of the tkinter library.

Allows for automated GUI events, such as key presses or
time steps, to be triggered.
"""
import types
import functools
import inspect


def copy_function(f):
    """
    Perform a deep copy of a python function.
    
    Based on http://stackoverflow.com/a/6528148/190597 (Glenn Maynard)
    """
    g = types.FunctionType(f.__code__, f.__globals__, name=f.__name__,
                           argdefs=f.__defaults__,
                           closure=f.__closure__)
    g = functools.update_wrapper(g, f)
    g.__kwdefaults__ = f.__kwdefaults__
    return g


class CoreMock:
    def __init__(self, context, reference) -> None:
        assert hasattr(context, reference)
        self._commands = []
        callable = getattr(context, reference)
        self._original = copy_function(callable)
        self._context, self._reference = context, reference
        setattr(self._context, self._reference, self._call)

    def _call(self, *args, **kwargs):
        pass
    
    def restore(self):
        setattr(self._context, self._reference, self._original)

class MockAndLog:
    pass


class Log:
    pass


class Mock:
    pass