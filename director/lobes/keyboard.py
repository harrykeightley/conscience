from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
import tkinter as tk

from behave.runner import Context
from behave import *

from director.lib.mocking import VacantLog, MockLog
from director.lobes.lobe import Lobe

KEY_EVENT_TYPES = ("<KeyPress>", "<Any-KeyPress>", "<Key>", "<KeyRelease>")
KEY_FORMATS = (
    "{}",
    "<{}>",
    "<Key-{}>",
    "<KeyRelease-{}>",
    "<KeyPress-{}>",
)


class TrackKeypresses(Lobe):
    def on_start(self, context, suite):
        TrackKeypresses._enabled = True
        context.key_binds = VacantLog(tk.Tk, "bind")

        bind_all_mock = MockLog(tk.Tk, "bind_all")
        bind_all_mock.register(
            lambda *args, **kwargs: print(
                "bind_all is not supported in all Tkinter distributions. Please use bind instead."
            )
        )

        @when("I press {key}")
        def press_key(context: Context, key: str):
            event = Events[key.upper()].value
            press(context, event)


def all_key_formats(key: str) -> list[str]:
    result = []
    for form in key, key.upper(), key.capitalize():
        result.extend([x.format(form) for x in KEY_FORMATS])

    return result


@dataclass
class KeyEvent:
    char: str
    keysym: str
    keycode: int

    def __repr__(self):
        return f"Event({self.char})"


class Events(Enum):
    LEFT = KeyEvent("\uf702", "Left", 2063660802)
    UP = KeyEvent("\uf700", "Up", 2113992448)
    RIGHT = KeyEvent("\uf704", "Right", 2080438019)
    DOWN = KeyEvent("\uf701", "Down", 2097215233)
    W = KeyEvent("w", "w", 222298199)
    A = KeyEvent("a", "a", 4194369)
    S = KeyEvent("s", "s", 20971603)
    D = KeyEvent("d", "d", 37748804)
    SPACE = KeyEvent(" ", "space", 0)
    RETURN = KeyEvent(" ", "return", 0)


def keypress_func(key_binds):
    # gather all bound functions that should always be invoked
    always_call = []
    for events in KEY_EVENT_TYPES:
        kp = key_binds.get(events)
        if kp is not None:
            always_call.append(kp)

    # build a mapping of keys to all the possible variations of their binding
    key_calls = defaultdict(list)
    for key in ("w", "a", "s", "d"):
        for keybind in all_key_formats(key):
            keycb = key_binds.get(keybind)
            if keycb is not None:
                key_calls[key].append(keycb)

    def callback(event):
        found_call = False
        # try the generic
        for call in always_call:
            found_call = True
            call(event)

        # try the specific
        keycb = key_calls[event.keysym.lower()]
        for call in keycb:
            found_call = True
            call(event)

        # fail if no call was found
        if not found_call:
            print(key_binds)
            assert (
                False
            ), f"unable to find an appropriate keyboard binding to call for {event.keysym.lower()}"

    return callback


def press(context, key):
    if len(context.key_binds.logs) == 0:
        assert (
            False
        ), "no calls made to the tkinter bind method, see: https://web.archive.org/web/20171112175007/http://www.effbot.org/tkinterbook/widget.htm#Tkinter.Widget.bind-method"

    method_calls = context.key_binds.logs

    key_binds = {}
    for call in method_calls:
        positional_arguments = call[0]

        if len(positional_arguments) < 2:
            assert (
                False
            ), f"call to bind does not specify a key and a callback, got: bind({', '.join(positional_arguments)})"

        key_bind = positional_arguments[0]
        callback = positional_arguments[1]

        key_binds[key_bind] = callback

    keypress_func(key_binds)(key)
