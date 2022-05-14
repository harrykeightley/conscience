import json
import csv
import re
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
    tags = map(lambda tag: tag[len(tag_name):].strip("()"), tags)
    tags = filter(lambda tag: tag.lstrip("-").isdigit(), tags)

    return int(next(tags, default))


def has_tag(scenario: Scenario, tag_name: str) -> bool:
    tags = filter(lambda tag: tag == tag_name, scenario.tags)
    
    return bool(next(tags, None))


class GradescopeFormatter(Formatter):
    # def feature(self, feature):
    #     print(feature)

    def __init__(self, stream_opener, config):
        super().__init__(stream_opener, config)

        self._tests = []
        self._results = {
            "tests": self._tests
        }

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
                student_email = entry['email']
                if submission_email != student_email:
                    continue

                self.type = entry
        
        if self.type is None:
            log = f"Unable to find submission metadata for {submission_email}"
        else:
            log = f"Submission metadata\n{self.type}"

        self._tests.append({
            "score": 0,
            "max_score": 0,
            "name": f"Metadata Debug",
            "output": log,
            "visibility": "hidden",
        })

    def reset(self, scenario):
        self._current_scenario: Scenario = scenario
        self._passed = True
        self._output = ""

    def _make_test(self):
        weight = parse_tag_value(self._current_scenario, "weight", default=1)
        visible = has_tag(self._current_scenario, "visible")
        if self.type is not None:
            postgrad = self.type.get("postgrad", False)
            if postgrad:
                adjustment = parse_tag_value(self._current_scenario, "postgradAdjust", 0)
                weight += adjustment

        if self._current_scenario.status == Status.skipped or self._current_scenario.feature.status == Status.skipped:
            reason = self._current_scenario.skip_reason or self._current_scenario.feature.skip_reason
            return {
                "score": 0,
                "max_score": weight,
                "name": f"Feature: {self._current_scenario.feature.name} - Scenario: {self._current_scenario.name} (skipped)",
                "output": reason,
                "visibility": visible and "visible" or "hidden",
            }
        
        return {
            "score": weight if self._passed else 0,
            "max_score": weight,
            "name": f"Feature: {self._current_scenario.feature.name} - Scenario: {self._current_scenario.name}",
            "output": self._output,
            "visibility": "visible" if visible else "after_published",
        }
    
    def scenario(self, scenario: Scenario):
        if self._current_scenario is not None:
            self._tests.append(self._make_test())
        self.reset(scenario)

    def result(self, step: Step):
        if step.status == Status.passed:
            self._output += f"{step.keyword} {step.name}\n"
            return

        self._passed = False

        if step.status == Status.skipped:
            self._output += f"{step.keyword} {step.name} (skipped)\n"
            return

        self._output += f"""{step.keyword} {step.name}
    status: {step.status}
    {step.error_message}

    output: {step.captured.output}
"""

        

    def eof(self):
        pass

    def close(self):
        if self._current_scenario is not None:
            self._tests.append(self._make_test())
        self.stream.write(json.dumps(self._results))
        super().close()

    # def step(self, step):
    #     print(step)
