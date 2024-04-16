import sys
from os import chdir
from pathlib import Path
import json

from behave.runner import Context
from conscience.config import ConscienceConfiguration

from behave.__main__ import run_behave
from conscience.parsers import register_parsers
from conscience.score import GradescopeResults, TestScore


def setup(context: Context):
    """Setup the context for testing with behave

    Pulls the software under test (SUT) and the DirectorSuite
    on level up within the context."""
    context.under_test = context.config.under_test
    context.suite = context.config.suite
    register_parsers()


def witness(
    config: ConscienceConfiguration,
    target: Path,
) -> GradescopeResults:
    """Tests a target assessment file with the supplied configuration.

    Parameters:
        config: The configuration class to run. Assumes that the passed
            configuration is already setup (see `conscience.config.setup_config`).
        target: The target file to run the tests on.

    Returns:
        The score representing how the student did on the tests.
        If the Configuration passed in is not a GradescopeConfiguration, returns
        a dummy score.
    """
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
    return config.read_results()


def export_results(results: GradescopeResults, output=sys.stdout):
    output.write(json.dumps(results, indent=4, ensure_ascii=False))


def aggregate_tests(*results: GradescopeResults) -> list[TestScore]:
    scores = []

    for result in results:
        if "tests" in result:
            scores += result["tests"]

    return scores


def load_common_steps():
    """Allows behave to see the steps defined in conscience.common.

    This exists to make explicit, the implicit behaviour of importing the module.
    """
    import conscience.common


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
