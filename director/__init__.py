name = "director"

from os import chdir
import logging
logger = logging.getLogger(__package__)
import importlib.util

from behave.__main__ import run_behave
from behave.__main__ import Configuration

from .formats import register_formats
from .mocking import MixinBase, LogMixin, RelayLog, MockMixin
from .mocking import VacantLog, RelayLog, MockLog
from .identify import WidgetSelector, find_widgets


def setup(context):
    context.under_test = context.config.under_test
    register_formats()


def load_under_test(path):
    spec = importlib.util.spec_from_file_location("under_test", path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo


def test(tests, target, working_directory="."):
    config = Configuration(tests)
    config.steps_dir = "."
    config.under_test = load_under_test(target)
    chdir(working_directory)
    run_behave(config)


__export__ = [MixinBase, LogMixin, RelayLog, MockMixin, VacantLog, RelayLog, MockLog, WidgetSelector, setup]
__test__ = {obj.__name__ : obj for obj in __export__}
__all__ = [cls.__name__ for cls in __export__] + ["logger", "find_widgets"]
