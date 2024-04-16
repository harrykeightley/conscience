from io import BytesIO
import sys
import json
from logging import error
from typing import Literal, NotRequired, TypedDict

TestStatus = Literal["passed", "failed"]
OutputFormat = Literal["text", "html", "simple_format", "md", "ansi"]
Visibility = Literal["visible", "hidden", "after_due_date", "after_published"]


class TestScore(TypedDict):
    """A dictionary representing the results of running a single test"""

    score: float
    max_score: NotRequired[float]
    name: NotRequired[str]
    name_format: NotRequired[OutputFormat]
    status: NotRequired[TestStatus]
    output: NotRequired[str]
    output_format: NotRequired[OutputFormat]
    tags: NotRequired[list[str]]
    visibility: NotRequired[Visibility]
    number: NotRequired[str]
    extra_data: NotRequired[dict]


class GradescopeResults(TypedDict):
    """A dictionary representing the results of running all tests for one student submission.

    See https://gradescope-autograders.readthedocs.io/en/latest/specs/"""

    score: NotRequired[float]
    execution_time: NotRequired[int]
    output: NotRequired[str]
    output_format: NotRequired[OutputFormat]
    test_output_format: NotRequired[OutputFormat]
    test_name_format: NotRequired[OutputFormat]
    visibility: NotRequired[Visibility]
    stdout_visibility: NotRequired[Visibility]
    extra_data: NotRequired[dict]
    tests: NotRequired[list[TestScore]]


EMPTY_SCORE: TestScore = {
    "score": 0,
    "output": "Empty Test Score",
    "max_score": 1,  # make implicit that the test failed
}


def error_results(msg: str) -> GradescopeResults:
    return {"score": 0, "output": msg}


def read_results_from_stream(stream: BytesIO) -> GradescopeResults:
    try:
        stream.seek(0)
        return json.load(stream)
    except json.JSONDecodeError:
        stream.seek(0)
        return error_results(stream.read().decode())


def aggregate_tests(*results: GradescopeResults) -> list[TestScore]:
    scores = []

    for result in results:
        if "tests" in result:
            scores += result["tests"]

    return scores


def aggregate_results(
    result: GradescopeResults, *results: GradescopeResults
) -> GradescopeResults:
    tests = aggregate_tests(result, *results)

    result = result.copy()
    result["tests"] = tests
    return result


def export_results(results: GradescopeResults, output=sys.stdout):
    output.write(json.dumps(results, indent=4, ensure_ascii=False))
