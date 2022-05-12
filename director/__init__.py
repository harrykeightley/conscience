name = "director"

from io import StringIO
from os import chdir
import logging
import json
import traceback
from typing import TypedDict

logger = logging.getLogger(__package__)
debug = logging.getLogger(f"{__package__}.debug")

import importlib.util

from behave.__main__ import run_behave
from behave.__main__ import Configuration
from behave.formatter.base import StreamOpener

from .formats import register_formats
from .mocking import MixinBase, LogMixin, RelayLog, MockMixin, RelayMixin
from .mocking import VacantLog, RelayLog, MockLog
from .identify import WidgetSelector, find_widgets
from director.formatters import GradescopeFormatter


def setup(context):
    context.under_test = context.config.under_test
    context.suite = context.config.suite
    register_formats()


def load_under_test(path):
    spec = importlib.util.spec_from_file_location("under_test", path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo


class GradeScopeMetadata(TypedDict):
    student_categories: str
    student_metadata: str


def test(tests, target, working_directory=".", gradescope=False,
         metadata: GradeScopeMetadata=None, suite=None):
    extra_args = [] if not gradescope else ["--no-summary"]
    config = Configuration(command_args=["--no-source", "--no-timings"] + extra_args)
    config.steps_dir = "."
    config.paths = tests
    config.environment_file = "../environment.py"

    config.log_capture = False

    output_stream = StringIO()
    config.outputs = [StreamOpener(stream=output_stream)]

    config.suite = suite

    try:
        config.under_test = load_under_test(target)
    except Exception as e:
        if not gradescope:
            raise e
        
        return {
            "score": 0,
            "output": traceback.format_exc()
        }

    if gradescope:
        if metadata is not None:
            config.student_categories = metadata["student_categories"]
            config.student_metadata = metadata["student_metadata"]
        else:
            config.student_categories = None
            config.student_metadata = None
        config.default_format = "gradescope"
        config.more_formatters = {"gradescope": GradescopeFormatter}
        config.setup_formats()

    chdir(working_directory)

    run_behave(config)

    try:
        output_stream.seek(0)
        return json.load(output_stream)
    except json.JSONDecodeError:
        output_stream.seek(0)
        return {
            "score": 0,
            "output": output_stream.read()
        }


__export__ = [MixinBase, LogMixin, RelayMixin, MockMixin, VacantLog, RelayLog, MockLog, WidgetSelector, setup]
__test__ = {obj.__name__ : obj for obj in __export__}
__all__ = [cls.__name__ for cls in __export__] + ["logger", "find_widgets"]
