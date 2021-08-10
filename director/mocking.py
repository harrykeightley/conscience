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


class MixinBase(object):
    """
    Core mocking functionality, allows calls to methods to be replaced with
    no-op behaviour.

    Examples:
    >>> class MockMe:
    ...     def do_it(self):
    ...         print("called")
    >>> mockme = MockMe()
    >>> mockme.do_it()
    called
    >>> mock = MixinBase(MockMe, "do_it")
    >>> mockme.do_it()
    >>> mock.restore()
    >>> mockme.do_it()
    called
    """
    def __init__(self, context, reference) -> None:
        assert hasattr(context, reference)
        self._commands = []
        callable = getattr(context, reference)
        self._original = copy_function(callable)
        self._context, self._reference = context, reference
        setattr(self._context, self._reference, self._call)

        for mixin in self.__class__.__mro__:
            if mixin == self.__class__:
                continue
            if hasattr(mixin, "setup"):
                mixin.setup(self)

    def _call(self, *args, **kwargs):
        for mixin in self.__class__.__mro__:
            if mixin == self.__class__:
                continue
            if hasattr(mixin, "inject"):
                mixin.inject(self, *args, **kwargs)
    
    def restore(self):
        setattr(self._context, self._reference, self._original)


class LogMixin(MixinBase):
    """
    Log calls to mocked references.

    >>> class Logger(LogMixin):
    ...     pass
    >>> class MockMe:
    ...     def do_it(self, *args, **kwargs):
    ...         print("called")
    >>> mockme = MockMe()
    >>> mockme.do_it()
    called
    >>> mock = Logger(MockMe, "do_it")
    >>> mockme.do_it("life", answer=42)
    >>> mockme.do_it()
    >>> mock.restore()
    >>> mockme.do_it()
    called
    >>> mock.logs
    [(('life',), {'answer': 42}), ((), {})]
    """
    def setup(self) -> None:
        self._records = []

    @property
    def logs(self):
        return self._records[:]

    def inject(self, *args, **kwargs):
        self._records.append((args, kwargs))


class MockMixin(MixinBase):
    """
    Inject arbitrary calls to a mocked reference.

    >>> class Injection(MockMixin):
    ...     pass
    >>> class MockMe:
    ...     def do_it(self, *args, **kwargs):
    ...         print("called")
    >>> mockme = MockMe()
    >>> mockme.do_it()
    called
    >>> mock = Injection(MockMe, "do_it")
    >>> mock.register(lambda *a, **kw: print("mocked", a, kw))
    >>> mockme.do_it("life", answer=42)
    mocked ('life',) {'answer': 42}
    >>> mockme.do_it()
    mocked () {}
    >>> mock.restore()
    >>> mockme.do_it()
    called
    """
    def setup(self) -> None:
        self._mocks = []

    def register(self, mock):
        self._mocks.append(mock)
        
    def inject(self, *args, **kwargs):
        for mock in self._mocks:
            mock(*args, **kwargs)


class RelayMixin(MixinBase):
    """
    Relay mocked calls to the original reference.

    >>> class Relay(RelayMixin):
    ...     pass
    >>> class MockMe:
    ...     def do_it(self, *args, **kwargs):
    ...         print("called")
    >>> mockme = MockMe()
    >>> mockme.do_it()
    called
    >>> mock = Relay(MockMe, "do_it")
    >>> mockme.do_it("life", answer=42)
    called
    >>> mockme.do_it()
    called
    >>> mock.restore()
    >>> mockme.do_it()
    called
    >>> mock.logs
    [(('life',), {'answer': 42}), ((), {})]
    """
    def inject(self, *args, **kwargs):
        self._original(self, *args, **kwargs)


# a couple of useful example mocking classes

class VacantLog(LogMixin):
    pass


class RelayLog(LogMixin, RelayMixin):
    pass


class MockLog(LogMixin, MockMixin):
    pass
