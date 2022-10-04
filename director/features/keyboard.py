from collections import defaultdict


class Event:
    def __init__(self, char, keysym, keycode):
        self.char = char
        self.keysym = keysym
        self.keycode = keycode

    def __repr__(self):
        return f"Event({self.char})"


class Events:
    LEFT = Event("\uf702", "Left", 2063660802)
    UP = Event("\uf700", "Up", 2113992448)
    RIGHT = Event("\uf704", "Right", 2080438019)
    DOWN = Event("\uf701", "Down", 2097215233)
    W = Event("w", "w", 222298199)
    A = Event("a", "a", 4194369)
    S = Event("s", "s", 20971603)
    D = Event("d", "d", 37748804)
    SPACE = Event(" ", "space", 0)
    RETURN = Event(" ", "return", 0)


def keypress_func(key_binds):
    # gather all bound functions that should always be invoked
    always_call = []
    for events in ("<KeyPress>", "<Any-KeyPress>", "<Key>", "<KeyRelease>"):
        kp = key_binds.get(events)
        if kp is not None:
            always_call.append(kp)

    # build a mapping of keys to all the possible variations of their binding
    key_calls = defaultdict(list)
    for key in ("w", "a", "s", "d"):
        for keybind in (key, key.upper(), key.capitalize(),
                        f"<{key}>", f"<{key.upper()}>", f"<{key.capitalize()}>",
                        f"<Key-{key}>", f"<Key-{key.upper()}>", f"<Key-{key.capitalize()}>",
                        f"<KeyRelease-{key}>", f"<KeyRelease-{key.upper()}>", f"<KeyRelease-{key.capitalize()}>",
                        f"<KeyPress-{key}>", f"<KeyPress-{key.upper()}>", f"<KeyPress-{key.capitalize()}>"):
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
            assert False, f"unable to find an appropriate keyboard binding to call for {event.keysym.lower()}"
    
    return callback

def press(context, key):
    if len(context.key_binds.logs) == 0:
        assert False, "no calls made to the tkinter bind method, see: https://web.archive.org/web/20171112175007/http://www.effbot.org/tkinterbook/widget.htm#Tkinter.Widget.bind-method"

    method_calls = context.key_binds.logs

    key_binds = {}
    for call in method_calls:
        positional_arguments = call[0]

        if len(positional_arguments) < 2:
            assert False, f"call to bind does not specify a key and a callback, got: bind({', '.join(positional_arguments)})"
        
        key_bind = positional_arguments[0]
        callback = positional_arguments[1]

        key_binds[key_bind] = callback

    keypress_func(key_binds)(key)

