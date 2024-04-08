import json
import csv
from typing import List, Optional, TypedDict
from enum import Enum
from behave.formatter.base import Formatter
from behave.model import Scenario, Step
from behave.model_core import Status


# type hints borrowed from MikeLint
class GradescopeAssignmentMetadata(TypedDict):
    due_date: str
    group_size: Optional[int]
    group_submission: bool
    id: int
    course_id: int
    late_due_date: Optional[str]
    release_data: str
    title: str
    total_point: str


class GradescopeSubmissionMethod(str, Enum):
    github = "GitHub"
    upload = "upload"
    bitbucket = "Bitbucket"


class GradescopeUser(TypedDict):
    email: str
    id: int
    name: str


class GradescopeSubmissionMetadata(TypedDict):
    id: int
    created_at: str
    assignment: GradescopeAssignmentMetadata
    submission_method: GradescopeSubmissionMethod
    users: List[GradescopeUser]


def parse_tag_value(scenario: Scenario, tag_name: str, default=None):
    tags = filter(lambda tag: tag.startswith(tag_name), scenario.tags)
    tags = map(lambda tag: tag[len(tag_name) :].strip("()"), tags)
    tags = filter(lambda tag: tag.lstrip("-").replace(".", "", 1).isdigit(), tags)

    return float(next(tags, default))


def has_tag(scenario: Scenario, tag_name: str) -> bool:
    tags = filter(lambda tag: tag == tag_name, scenario.tags)

    return bool(next(tags, None))


class GradescopeFormatter(Formatter):
    # def feature(self, feature):
    #     print(feature)

    def __init__(self, stream_opener, config):
        super().__init__(stream_opener, config)

        self._tests = []
        self._results = {"tests": self._tests}

        self._determine_student_type()
        self.reset(None)

    def _determine_student_type(self):
        self.type = None

        if self.config.student_metadata is None:
            return

        if self.config.student_categories is None:
            return

        with open(self.config.student_metadata) as f:
            metadata: GradescopeSubmissionMetadata = json.load(f)

        submission_email = metadata["users"][0]["email"]
        with open(self.config.student_categories) as f:
            category_data = csv.DictReader(f)
            for entry in category_data:
                student_email = entry["email"]
                if submission_email != student_email:
                    continue

                self.type = entry

        if self.type is None:
            log = f"Unable to find submission metadata for {submission_email}"
        else:
            log = f"Submission metadata\n{self.type}"

        self._tests.append(
            {
                "score": 0,
                "max_score": 0,
                "name": f"Metadata Debug",
                "output": log,
                "visibility": "hidden",
            }
        )

    def _format_test_name(self, scenario: Scenario):
        return f"{scenario.name} ({scenario.feature.name})"

    def _format_step_name(self, step: Step):
        status = {
            Status.passed.value: "✅",
            Status.failed.value: "❌",
            Status.skipped.value: "⏭ ",
        }.get(step.status.value, "")
        prepend = {Status.skipped.value: " (skipped)"}.get(step.status.value, "")

        result = f"{status} {step.keyword} {step.name}{prepend}"
        if step.text:
            indented_text = "\n".join(f"   {line}" for line in step.text.split("\n"))
            result += f"\n{indented_text}"

        return result

    def reset(self, scenario: Scenario):
        self._current_scenario: Scenario = scenario
        self._passed = True
        self._output = ""

    def _make_test(self):
        weight = parse_tag_value(self._current_scenario, "weight", default=1)
        visible = has_tag(self._current_scenario, "visible")
        if self.type is not None:
            postgrad = self.type.get("postgrad", False)
            if postgrad:
                adjustment = parse_tag_value(
                    self._current_scenario, "postgradAdjust", 0
                )
                weight += adjustment

        if (
            self._current_scenario.status == Status.skipped
            or self._current_scenario.feature.status == Status.skipped
        ):
            reason = (
                self._current_scenario.skip_reason
                or self._current_scenario.feature.skip_reason
            )
            return {
                "score": 0,
                "max_score": weight,
                "name": self._format_test_name(self._current_scenario),
                "output": f"⏭  {reason}",
                "visibility": "visible" if visible else "after_published",
            }

        return {
            "score": weight if self._passed else 0,
            "max_score": weight,
            "name": self._format_test_name(self._current_scenario),
            "output": self._output,
            "visibility": "visible" if visible else "after_published",
        }

    def scenario(self, scenario: Scenario):
        if self._current_scenario is not None:
            self._tests.append(self._make_test())
        self.reset(scenario)

    def help_tags(self, scenario: Scenario):
        helpers = []
        for tag in scenario.tags:
            if tag.startswith("help"):
                helpers.append(tag[5:].strip("()"))
        return helpers

    def result(self, step: Step):
        if step.status == Status.passed:
            self._output += f"{self._format_step_name(step)}\n"
            return

        self._passed = False

        if step.status == Status.skipped:
            self._output += f"{self._format_step_name(step)}\n"
            return

        raw_output = (
            f"output: {step.captured.output}\n"
            if len(step.captured.output.strip()) > 0
            else ""
        )
        self._output += f"""{self._format_step_name(step)}
    {step.error_message}
"""
        help_tags = self.help_tags(self._current_scenario)
        if len(help_tags) > 0:
            self._output += f"    Try these EdStem posts:\n"
            for tag in help_tags:
                self._output += f"        {tag}\n"

        message = self.config.suite.on_fail(self._current_scenario, step)
        if message is not None:
            self._output += f"    {message}\n"

    def eof(self):
        pass

    def close(self):
        if self._current_scenario is not None:
            self._tests.append(self._make_test())
        self.stream.write(json.dumps(self._results, ensure_ascii=False).encode("utf8"))
        super().close()

    # def step(self, step):
    #     print(step)
