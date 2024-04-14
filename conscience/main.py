import sys
from os import chdir
from pathlib import Path
import json

from behave.runner import Context
from conscience.config import ConscienceConfiguration

import importlib.util

from behave.__main__ import run_behave

from conscience.parsers import register_parsers


def setup(context: Context):
    context.under_test = context.config.under_test
    context.suite = context.config.suite
    register_parsers()


def load_under_test(path: Path):
    """Loads the supplied path as the `Software Under Test`, as behave.py requires the
    libary to be loaded already.
    Parameters:
        path: The path to the file to load.
    """
    spec = importlib.util.spec_from_file_location("under_test", path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo


def witness(
    config: ConscienceConfiguration,
    target: Path,
):
    if config.working_directory:
        chdir(config.working_directory)

    if config.suite:
        config.suite.load()

    config.setup_formats()
    config.reset_outputs()

    # Attempt to load the software under test (target)
    try:
        config.load_target(target)
    except Exception as e:
        return config.handle_load_failure(e)

    run_behave(config)
    return config.read_score()


def run_tests(config: ConscienceConfiguration, target: Path, output=sys.stdout):
    score = witness(config, target).to_aggregated_tests()
    output.write(json.dumps(score, indent=4, ensure_ascii=False))


# OLD STUFF FOR SAFEKEEPING

# def test(
#     tests: Path | list[Path],
#     target: Path,
#     working_directory: Path = Path("."),
#     gradescope=False,
#     metadata: Optional[GradeScopeMetadata] = None,
#     suite: Optional[ConscienceSuite] = None,
#     environment_file: Path = Path("../environment.py"),
# ):
#     extra_args = [] if not gradescope else ["--no-summary"]
#     config = Configuration(command_args=["--no-source", "--no-timings"] + extra_args)
#     config.steps_dir = "."
#     config.paths = tests
#     config.environment_file = environment_file
#
#     config.log_capture = False
#
#     output_stream = BytesIO()
#     config.outputs = [] if not gradescope else [StreamOpener(stream=output_stream)]
#
#     config.suite = suite
#
#     try:
#         config.under_test = load_under_test(target)
#     except Exception as e:
#         if not gradescope:
#             raise e
#
#         return {"score": 0, "output": traceback.format_exc()}
#
#     if gradescope:
#         if metadata is not None:
#             config.student_categories = metadata["student_categories"]
#             config.student_metadata = metadata["student_metadata"]
#         else:
#             config.student_categories = None
#             config.student_metadata = None
#         config.default_format = "gradescope"
#         config.more_formatters = {"gradescope": GradescopeFormatter}
#         config.setup_formats()
#
#     chdir(working_directory)
#
#     suite.load()
#     run_behave(config)
#
#     if not gradescope:
#         return {}
#
#     try:
#         output_stream.seek(0)
#         return json.load(output_stream)
#     except json.JSONDecodeError:
#         output_stream.seek(0)
#         return {"score": 0, "output": output_stream.read()}


# def aggregate_tests(tests):
#     """
#     Combine the results of multiple tests into a single result.
#     """
#     result = {"tests": []}
#     for test in tests:
#         if "tests" in test:
#             result["tests"] += test["tests"]
#     return result

# def old_run_tests(path, suite=ConscienceSuite, output=sys.stdout):
#     tests = [
#         test(
#             [f"scenarios/{scenario}.feature" for scenario in SCENARIOS],
#             path,
#             gradescope=GRADESCOPE,
#             suite=suite,
#         )
#     ]
#
#     aggregated = aggregate_tests(tests)
#     if len(aggregated["tests"]) == 0 and "output" in tests[0]:
#         output.write(json.dumps(tests[0], indent=4))
#     elif len(aggregated["tests"]) == 0:
#         output.write(
#             json.dumps(
#                 {
#                     "output": "Unknown error occurred please email the helpdesk: csse1001@helpdesk.eait.uq.edu.au",
#                     "score": 0,
#                     "max_score": 1,
#                 },
#                 indent=4,
#             )
#         )
#     else:
#         output.write(json.dumps(aggregated, indent=4, ensure_ascii=False))
#
#     debug_log.seek(0)
#     info_log.seek(0)
#     print(debug_log.read())
#     print(info_log.read())
