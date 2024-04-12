from io import BytesIO, StringIO
from os import chdir
from pathlib import Path
import json
import traceback
from typing import Optional, TypedDict

from behave.runner import Context

from conscience.suite import DirectorSuite

import importlib.util

from behave.__main__ import run_behave
from behave.__main__ import Configuration
from behave.formatter.base import StreamOpener

from conscience.parsers import register_parsers
from conscience.lib.identify import WidgetSelector, find_widgets
from conscience.formatters import GradescopeFormatter


def setup(context: Context):
    context.under_test = context.config.under_test
    context.suite = context.config.suite
    register_parsers()


def load_under_test(path: Path):
    # NOTE: What the *** does this do @Brae?
    spec = importlib.util.spec_from_file_location("under_test", path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo


class GradeScopeMetadata(TypedDict):
    student_categories: str
    student_metadata: str


def test(
    tests: Path | list[Path],
    target: Path,
    working_directory: Path = Path("."),
    gradescope=False,
    metadata: Optional[GradeScopeMetadata] = None,
    suite: Optional[DirectorSuite] = None,
    environment_file: Path = Path("../environment.py"),
):
    extra_args = [] if not gradescope else ["--no-summary"]
    config = Configuration(command_args=["--no-source", "--no-timings"] + extra_args)
    config.steps_dir = "."
    config.paths = tests
    config.environment_file = environment_file

    config.log_capture = False

    output_stream = BytesIO()
    config.outputs = [] if not gradescope else [StreamOpener(stream=output_stream)]

    config.suite = suite

    try:
        config.under_test = load_under_test(target)
    except Exception as e:
        if not gradescope:
            raise e

        return {"score": 0, "output": traceback.format_exc()}

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

    suite.load()
    run_behave(config)

    if not gradescope:
        return {}

    try:
        output_stream.seek(0)
        return json.load(output_stream)
    except json.JSONDecodeError:
        output_stream.seek(0)
        return {"score": 0, "output": output_stream.read()}
