name = "director"

from os import chdir
import logging
import json
import traceback

logger = logging.getLogger(__package__)
import importlib.util

from behave.__main__ import run_behave
from behave.__main__ import Configuration

from .formats import register_formats
from .mocking import MixinBase, LogMixin, RelayLog, MockMixin
from .mocking import VacantLog, RelayLog, MockLog
from .identify import WidgetSelector, find_widgets
from director.formatters import GradescopeFormatter


def setup(context):
    context.under_test = context.config.under_test
    register_formats()


def load_under_test(path):
    spec = importlib.util.spec_from_file_location("under_test", path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo


def test(tests, target, working_directory=".", gradescope=False):
    extra_args = [] if not gradescope else ["--no-summary"]
    config = Configuration(command_args=[tests, "--no-source", "--no-timings"] + extra_args)
    config.steps_dir = "."

    try:
        config.under_test = load_under_test(target)
    except SyntaxError as e:
        if not gradescope:
            raise e
        
        print(json.dumps({
            "score": 0,
            "output": traceback.format_exc()
        }))
        return

    if gradescope:
        config.default_format = "gradescope"
        config.more_formatters = {"gradescope": GradescopeFormatter}
        config.setup_formats()

    chdir(working_directory)

    run_behave(config)        


__export__ = [MixinBase, LogMixin, RelayLog, MockMixin, VacantLog, RelayLog, MockLog, WidgetSelector, setup]
__test__ = {obj.__name__ : obj for obj in __export__}
__all__ = [cls.__name__ for cls in __export__] + ["logger", "find_widgets"]
